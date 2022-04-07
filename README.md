# ROCKET-LDAP-SYNCHRO

## Introduction

**rocket-ldap-synchro** is a python program which synchronize LDAP users and RocketChat local users by using RocketChat API. 

## Installation

    pip install -r requirements.txt

## Configuration
- A new role must be added in RocketChat (example : ldap-user) and set in config.py file.


- Rename config-sample.py to config.py and credentials-sample.py to credentials.py


- Set properties and auth information in the following files : credendials.py and config.py

## Usage

    python main.py
or
    
    py main.py
## Version
Current Version : 1.0 (23032022)

## Licence

Released under the [MIT Licence](https://opensource.org/licenses/MIT)