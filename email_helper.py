import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from env import *
import requests
from main import create_image

# Not used:
def send_image(receiver, imgPath):
    msg = EmailMessage()
    msg['Subject'] = "Elevate Your Day with Today's Inspirational Quote!"
    msg['From'] = EMAIL_ID
    msg['To'] = receiver
    msg.set_content("Hey, rise and shine! Ready to elevate your daily grind with a burst of inspiration? Attached, just for you, is today's power-packed, uplifting quote to kickstart your day on the most positive note possible. Trust me, it's like a shot of motivation straight to the soul. So, buckle up and let's make today ridiculously amazing together!\n\n\n")
    

    with open(imgPath, 'rb') as f:
        file_data = f.read()
        file_name = f.name
        
    msg.add_attachment(file_data, maintype='image', subtype='jpg', filename=file_name)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASS)
    server.send_message(msg)
    server.quit()



def send_image_with_html(receiver, id, imgPath):
    msg = MIMEMultipart()
    msg['Subject'] = "Elevate Your Day with Today's Inspirational Quote!"
    msg['From'] = EMAIL_ID
    msg['To'] = receiver
    
    # Set the content as HTML
    html_content = (
        f"<p>Hey, rise and shine! Ready to elevate your daily grind with a burst of inspiration? "
        f"and kickstart your day on the most positive note possible. Trust me, it's like a shot of motivation straight to the soul. "
        "So, buckle up and let's make today ridiculously amazing together!</p>"
        f'<br><br><br><br><a href="{HOST_URL}/unsubscribe?id={id}">Unsubscribe</a>'
    )
    msg.attach(MIMEText(html_content, 'html'))

    with open(imgPath, 'rb') as f:
        file_data = f.read()
        file_name = "Quote.jpg"


    image_attachment = MIMEImage(file_data, name=file_name, maintype='image', subtype='jpg')
    msg.attach(image_attachment)

    # msg.add_attachment(file_data, maintype='image', subtype='jpg', filename=file_name)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ID, EMAIL_PASS)
    server.send_message(msg)
    server.quit()


def mail_users(frequency):
    """
    Send personalized images to subscribed users based on their interests.

    Args:
        frequency (str): The frequency at which the images should be sent. Valid values are 'Daily', 'Weekly', 'Fortnight', and 'Monthly'.

    Returns:
        None
    """
        

    headers = {
        'Content-Type': 'application/json',
        'x-apikey': DB_API
    }
    params = {
        'q': f'{{"Frequency":"{frequency}"}}'
    }

    users = requests.get(DB_URL, headers=headers, params=params).json()

    print(f"Total users for {frequency.lower()} mailing: " + str(len(users)))

    if len(users) == 0:
        return "No users found for frequency: " + frequency


    for user in users:
        name = user['Name']
        email = user['Email']
        interests = user['Interests'] #space separated single string
        user_id = user["_id"]
        print("Creating image for: " + name)
        image_path = create_image(interests)

        print("Sending image to: " + email)
        send_image_with_html(email, user_id, image_path)
    return "Emails sent successfully!"
    


# Example usage:

if __name__ == "__main__":
    if input("Wanna mail users? (y/n)") == "y":
        mail_users("Daily") 
        mail_users("Weekly") 
        mail_users("Fortnight") 
        mail_users("Monthly") 