from ldap3 import Server, Connection, SAFE_SYNC
from rocketchat_API.rocketchat import RocketChat
from credentials import credentials
from config import config
import secrets

# Get Existing Users From RocketChat
rocket = RocketChat(credentials['rocket']['user'],
                    credentials['rocket']['pass'],
                    server_url=config['rocket']['server'])

rocketUsers = rocket.users_list(query='{"roles":"' + config['rocket']['ldap_role_id'] + '"}').json().get('users')

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
                                          attributes=[config['ldap']['userid_field'],
                                                      config['ldap']['lastname_field'],
                                                      config['ldap']['firstname_field'],
                                                      config['ldap']['email_field']])
if status:

    total_entries = len(response)
    total_users_created = 0
    total_users_deleted = 0
    total_users_disabled = 0

    # Fetch users from LDAP
    for entry in response:
        username = entry['attributes'][config['ldap']['userid_field']][0]
        email = entry['attributes'][config['ldap']['email_field']][0]
        firstname = entry['attributes'][config['ldap']['firstname_field']][0]
        lastname = entry['attributes'][config['ldap']['lastname_field']][0]
        role = config['rocket']['ldap_role_id']
        if not username in rocketUsersName:
            # User in RocketChat not exists : create it
            rocket.users_create(email,
                                firstname + ' ' + lastname,
                                secrets.token_urlsafe(16),
                                username,
                                roles=['user', role])
            total_users_created = total_users_created + 1
            print('Utilisateur', username, 'cr??e')
        else:
            # User in RocketChat exists : remove from list
            rocketUsersName.remove(username)

    # Delete or disable users who are in the list (user are in RocketChat, but not in LDAP anymore)
    if config['rocket_remaining_user_action'] == 'delete':
        for userName in rocketUsersName:
            u = list(filter(lambda user: user['username'] == userName, rocketUsers))
            if u:
                rocket.users_delete(u[0]['_id'])
                total_users_deleted = total_users_deleted + 1
                print('Utilisateur', userName, 'supprim??')

    if config['rocket_remaining_user_action'] == 'disable':
        for userName in rocketUsersName:
            u = list(filter(lambda user: user['username'] == userName, rocketUsers))
            if u:
                rocket.users_set_active_status(u[0]['_id'], False)
                total_users_disabled = total_users_disabled + 1
                print('Utilisateur', userName, 'd??sactiv??')

    # Display Infos
    print('Total des entr??es :', total_entries)
    print('Total des utilisateurs cr??es :', total_users_created)
    print('Total des utilisateurs supprim??s :', total_users_deleted)
    print('Total des utilisateurs d??sactiv??s :', total_users_disabled)

else:

    print('Une erreur est survenue lors de la connexion au serveur LDAP')
