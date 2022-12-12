from ldap3 import Server, Connection, SAFE_SYNC
from rocketchat_API.rocketchat import RocketChat
import json
from credentials import credentials
from config import config

# Rocket
rocket = RocketChat(credentials['rocket']['user'],
                    credentials['rocket']['pass'],
                    server_url=config['rocket']['server'])

# Get All Rocket Groups
rocketAllGroups = {}
rocketOwnerAllGroups = {}
groups = rocket.groups_list_all().json().get('groups')
for group in groups:
    rocketAllGroups[group['name']] = group['_id']
    rocketOwnerAllGroups[group['name']] = group['u']['username']

# Get All Rocket Users
rocketAllUsers = {}
users = rocket.users_list(count=0).json().get('users')
for user in users:
    rocketAllUsers[user['username']] = user['_id']

# LDAP Search
ldapServer = Server(config['ldap']['server'])

conn = Connection(ldapServer,
                  credentials['ldap']['user'],
                  credentials['ldap']['pass'],
                  client_strategy=SAFE_SYNC,
                  auto_bind=True)


f = open('channels-card.json')
data = json.load(f)

# Fetch Channels Card
for key in data.keys():

    ldapMembers = []
    rocketCardGroups = []

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
        rocketCardGroups = [data[key]]
    else:
        rocketCardGroups = data[key]

    for rocketCardGroup in rocketCardGroups:

        # Create group in Rocket if not exists
        if rocketCardGroup not in rocketAllGroups.keys():
            rocket.groups_create(name=rocketCardGroup, members=ldapMembers)
            print('Création du groupe: ' + rocketCardGroup)
        # Update if Rocket group exits
        else:
            # Get members from Rocket Group
            rocketMembers = {}
            response = rocket.groups_members(group=rocketCardGroup).json()
            for entry in response['members']:
                rocketMembers[entry['username']] = entry['_id']

            tmp = list(rocketMembers.keys())

            # Protect group owner from delete
            tmp.remove(rocketOwnerAllGroups[rocketCardGroup])

            for ldapMember in ldapMembers:
                # Add member if exist in ldap and not in rocket
                if ldapMember not in rocketMembers.keys():
                    if ldapMember not in config['rocket']['exclude_users_for_sync']:
                        rocket.groups_invite(rocketAllGroups[rocketCardGroup], rocketAllUsers[ldapMember])
                        print('Ajout de ' + ldapMember + ' dans le groupe ' + rocketCardGroup)

                tmp.remove(ldapMember)

            # users still in tmp must be removed
            for userToDelete in tmp:
                if userToDelete not in config['rocket']['exclude_users_for_sync']:
                    rocket.groups_kick(rocketAllGroups[rocketCardGroup], rocketAllUsers[userToDelete])
                    print('Suppression de ' + userToDelete + ' dans le groupe ' + rocketCardGroup)
