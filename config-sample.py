config = {
    'ldap': {
        'server': '',
        'base': '',  # dc=mycompany,dc=en
        'base_group': '',  # ou=groups,dc=mycompany,dc=en
        'filter': '',  # (&(departmentNumber=SALES)(enabled=TRUE))
        'userid_field': '',  # uid
        'lastname_field': '',  # sn
        'firstname_field': '',  # givenName
        'email_field': '',  # mail
        'group_common_name_field': '',  # cn
        'group_member_field': '',  # memberUid
    },
    'rocket': {
        'server': '',
        'ldap_role_id': ''  # Specific role must be created in rocketChat before
    },
    'rocket_remaining_user_action': 'delete'  # delete, disable, none
}