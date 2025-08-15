import os
from database import con, cur

def create_user():
    os.system('clear')
    fname = input('Enter your firtsname: ')
    lname = input('Enter your lastname: ')
    ide_num = input('Enter your ident number: ')
    email = input('Enter your email: ')
    new_data = f'''
        INSERT INTO users (firstname, lastname, ide_number, email)
        VALUES ('{fname}', '{lname}', '{ide_num}', '{email}')
    '''
    con.execute(new_data)
    con.commit()
    print(':::  User has been created successfully!  :::')
#create_user()

def list_users():
    os.system('clear')
    users_data_query = '''
        SELECT 
            id,
            firstname,
            lastname,
            email,
            ide_number,
            case when status = 1 then 'Active' else 'Inactive' end as status
        FROM 
            users
    '''
    cur.execute(users_data_query)
    data = cur.fetchall()
    print(data)
list_users()
