config = {
    'ldap': {
        'server': '',
        'base': '',  # dc=mycompany,dc=en
        'filter': '',  # (&(departmentNumber=SALES)(enabled=TRUE))
        'userid_field': '',  # uid
        'lastname_field': '',  # sn
        'firstname_field': '',  # givenName
        'email_field': '',  # mail
    },
    'rocket': {
        'server': '',
        'ldap_role_id': ''  # Specific role must be create in rocketChat before
    },
    'rocket_remaining_user_action': 'delete'  # delete, disable, none
}