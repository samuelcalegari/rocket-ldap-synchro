from ldap3 import Server, Connection, SAFE_SYNC
from rocketchat_API.rocketchat import RocketChat
import json
from credentials import credentials
from config import config

# Rocket
rocket = RocketChat(credentials['rocket']['user'],
                    credentials['rocket']['pass'],
                    server_url=config['rocket']['server'])

# LDAP Search
ldapServer = Server(config['ldap']['server'])

conn = Connection(ldapServer,
                  credentials['ldap']['user'],
                  credentials['ldap']['pass'],
                  client_strategy=SAFE_SYNC,
                  auto_bind=True)


f = open('users-card.json')
data = json.load(f)

# Fetch Channels Card
for key in data.keys():

    ldapMembers = []
    rocketCardRoles = []

    # Retrieve members from LDAP
    status, result, response, _ = conn.search(config['ldap']['base_group'],
                                              '(' + config['ldap']['group_common_name_field'] + '=' + key + ')',
                                              attributes=[
                                                  config['ldap']['group_common_name_field'],
                                                  config['ldap']['group_member_field']
                                              ])

    if status:
        # Fetch all LDAP groups and get unique members
        for entry in response:
            ldapMembers = list(set(ldapMembers + entry['attributes']['memberUid']))


    if type(data[key]) == str:
        rocketCardRoles = [data[key]]
    else:
        rocketCardRoles = data[key]

    for rocketCardRole in rocketCardRoles:
        for ldapMember in ldapMembers:
            # Add role to member
            rocket.roles_add_user_to_role(rocketCardRole, ldapMember)
            print('Ajout du rôle ' + rocketCardRole + ' à l\'utilisateur ' + ldapMember)




