import requests
from env import *
#While copying any of these functions: please add these two lines with their values from env.py:

url = DB_URL
headers = {
        'Content-Type': 'application/json',
        'x-apikey': DB_API
    }

def addUser():
    
    data = {
        'Name': 'Cody Andersan',
        'Email': 'itscodyandersan@gmail.com',
        "Interests": "Coding,Development,AI,Physics,Programming"
    }

    response =requests.post(url, headers=headers, json=data)
    print("User added successfully!")

def get_users():
    response = requests.get(url, headers=headers).json()
    return response


def emptyDB():
    users = get_users()

    for user in users:
        object_id = user['_id']
        delete_url = f'{url}/{object_id}'
        response = requests.delete(delete_url, headers=headers)

        if response.status_code == 200:
            print(f'Deleted user with object ID: {object_id}')
        else:
            print(f'Failed to delete user with object ID: {object_id}')

if __name__ == "__main__":
    # emptyDB()
    addUser()
    # print(get_users())
