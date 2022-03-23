from ldap3 import Server, Connection, SAFE_SYNC
from rocketchat_API.rocketchat import RocketChat
from credentials import credentials
from config import config

# Get Existing Users From RocketChat
rocket = RocketChat(credentials['rocket']['user'],
                    credentials['rocket']['pass'],
                    server_url=config['rocket']['server'])

rocketUsers = rocket.users_list(query='{"roles":"' + config['rocket']['ldap_role_id'] + '"}').json().get('users')

u = list(filter(lambda user: user['username'] == 'sgarry', rocketUsers))
print(u[0]['_id'])

rocketUsersName = []
for rocketUser in rocketUsers:
    rocketUsersName.append(rocketUser['username'])

# LDAP Search
ldapServer = Server(config['ldap']['server'])

conn = Connection(ldapServer,
                  credentials['ldap']['user'],
                  credentials['ldap']['pass'],
                  client_strategy=SAFE_SYNC,
                  auto_bind=True)


status, result, response, _ = conn.search(config['ldap']['base'],
                                          config['ldap']['filter'],
                                          attributes=['uid',
                                                      'sn',
                                                      'givenName',
                                                      'mail'])
if status:

    total_entries = len(response)
    total_users_created = 0
    total_users_deleted = 0
    total_users_disabled = 0

    # Fetch users from LDAP
    for entry in response:
        if not entry['attributes']['uid'][0] in rocketUsersName:
            # User in RocketChat not exists : create it
            rocket.users_create(entry['attributes']['mail'][0],
                                entry['attributes']['givenName'][0] + ' ' + entry['attributes']['sn'][0], 'zzzz9999zzzz',
                                entry['attributes']['uid'][0],
                                roles=['user', config['rocket']['ldap_role_id']])
            total_users_created = total_users_created + 1
            print('Utilisateur', entry['attributes']['uid'][0], 'crée')
        else:
            # User in RocketChat exists : remove from list
            rocketUsersName.remove(entry['attributes']['uid'][0])

    # Delete or disable users who are in the list (user are in RocketChat, but not in LDAP anymore)
    if config['rocket_remaining_user_action'] == 'delete':
        for userName in rocketUsersName:
            u = list(filter(lambda user: user['username'] == entry['attributes']['uid'][0], rocketUsers))
            if u:
                rocket.users_delete(u[0]['_id'])
                total_users_deleted = total_users_deleted + 1
                print('Utilisateur', entry['attributes']['uid'][0], 'supprimé')

    if config['rocket_remaining_user_action'] == 'disable':
        for userName in rocketUsersName:
            u = list(filter(lambda user: user['username'] == entry['attributes']['uid'][0], rocketUsers))
            if u:
                rocket.users_set_active_status(u[0]['_id'], False)
                total_users_disabled = total_users_disabled + 1
                print('Utilisateur', entry['attributes']['uid'][0], 'désactivé')

    # Display Infos
    print('Total des entrées :', total_entries)
    print('Total des utilisateurs crées :', total_users_created)
    print('Total des utilisateurs supprimés :', total_users_deleted)

else:

    print('Une erreur est survenue lors de la connexion au serveur LDAP')

