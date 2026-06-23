from pathlib import Path
import hashlib
import os
import dbmanage
import Encryption

KeyPassword = ""
salt = ''
if not Path.exists("secure.db"):
    dbmanage.init_database()
    password = ""
    Second = "1"
    print("First time running")
    while password != Second:
        password = input("Please input Password: ")
        Second = input("Please reinput Password (THEY MUST MATCH): ")
    
    salt = os.urandom(16)
    key = Encryption.regenerateKey(password, salt)
    hash = hashlib.sha256((key+salt)).digest()

    dbmanage.set_salt_hash(salt, hash)

def verify(password):
    hash = dbmanage.get_passhash()
    salt = dbmanage.get_salt()
    return Encryption.verifyKeyHash(hash, password, salt)


def input_pair(name, password):
    salt = dbmanage.get_salt()
    Key = Encryption.regenerateKey(KeyPassword, salt)
    
    name = Encryption.encrypt(Key, name)
    password = Encryption.encrypt(Key, password)

    dbmanage.add_password(name, password)
    return True

def get_list():
    sol = []
    salt = dbmanage.get_salt()
    Key = Encryption.regenerateKey(KeyPassword, salt)
    for nmps in dbmanage.get_passwordtable():
        name = Encryption.decrypt(Key, nmps[1])
        password = Encryption.decrypt(Key, nmps[2])
        sol.append((name,password))
    return sol


def main_loop():
    print("Input: 1(get password lists), 2(input name/password pair), 3(search for a password), 4(quit): ")
    num = int(input())
    
    match num:
        case 4:
            return False
        case 3:
            print("not implemented")
        case 2:
            Name = input("What for? ")
            Password = input("Password? ")
            input_pair(Name, Password)
        case 1:
            for j in get_list():
                print(j)
        case _:
            print("nan")



    return True


KeyPassword = input("Imput Password to gain access to CLI: ")
salt = dbmanage.get_salt()

if verify(KeyPassword):
    while main_loop():
        pass