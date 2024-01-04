import smtplib
from email.message import EmailMessage
from env import *
import requests
from main import create_image
def send_image(receiver, imgPath):
    msg = EmailMessage()
    msg['Subject'] = "Elevate Your Day with Today's Inspirational Quote 🌟"
    msg['From'] = EMAIL_ID
    msg['To'] = receiver
    msg.set_content("Elevate your daily routine with a splash of inspiration! Attached is today's uplifting quote image to kickstart your day on a positive note.")

    with open(imgPath, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        
    msg.add_attachment(file_data, maintype='image', subtype='jpg', filename=file_name)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASS)
    server.send_message(msg)
    server.quit()

def get_users():

    url = DB_URL
    headers = {
    'Content-Type': 'application/json',
    'x-apikey': DB_API
    }

    response = requests.get(url, headers=headers).json()
    return response

def mail_all_users():
    users = get_users()
    print("Total users: " + str(len(users)))

    for user in users:
        name = user['Name']
        email = user['Email']
        interests = user['Interests'] #space separated single string
        print("Creating image for: " + name)
        image_path = create_image(interests)

        print("Sending image to: " + email)
        send_image(email, image_path)
    

if __name__ == "__main__":
    if input("Wanna send mail? (y/n)") == "y":
        send_image('itscodyandersan@gmail.com', "/tmp/quote_1704362975.jpg")
    print(get_users())

    mail_all_users()