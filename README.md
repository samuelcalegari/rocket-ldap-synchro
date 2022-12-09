# ROCKET-LDAP-SYNCHRO

## Introduction

**rocket-ldap-synchro** is a python program which  : 
- Synchronize LDAP users and RocketChat local users 
- Synchronize LDAP groups and RocketChat private groups
- Synchronize LDAP groups and RocketChat users roles
By using RocketChat API. 

## Installation

    pip install -r requirements.txt

## Configuration
- A new role must be added in RocketChat (example : ldap-user) and set in config.py file.
- Rename config-sample.py to config.py and credentials-sample.py to credentials.py
- Set properties and auth information in the following files : credendials.py and config.py
- Rename channels-card-sample.json to channels-card.json
- Configure mapping in channels-card.json file
- Rename users-card-sample.json to users-card.json
- Configure mapping in users-card.json file

## Usage

    python sync-users.py
    python sync-groups.py
    python sync-roles.py
or
    
    py sync-users.py
    py sync-groups.py
    py sync-roles.py

## Version
Current Version : 1.2 (09122022)

## Licence

Released under the [MIT Licence](https://opensource.org/licenses/MIT)