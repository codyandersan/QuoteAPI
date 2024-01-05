import requests
from env import *
#While copying any of these functions: please add these two lines with their values from env.py:

url = DB_URL
headers = {
        'Content-Type': 'application/json',
        'x-apikey': DB_API
    }

def addUser(name, email, interests, frequency):
    """
    Adds a user to the database.

    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
        interests (str): The interests of the user, separated by commas.
        frequency (str): The frequency at which the user wants to receive updates. Can be 'Daily', 'Weekly', 'Fortnight', or 'Monthly'.
    """
    
    data = {
        'Name': name,
        'Email': email,
        "Interests": interests,
        "Frequency": frequency #Daily/Weekly/Fortnight/Monthly
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 400:
        return "Failed to add user. Error: " + response.text
    else:
        return "User added successfully!"


def delete_user(id):
    userUrl = f'{DB_URL}/{id}'
    
    response = requests.delete(userUrl, headers=headers)

    if response.status_code == 200:
        return "User deleted successfully."
    else:
        return "Failed to delete user."


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

