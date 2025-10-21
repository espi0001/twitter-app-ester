import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##############################
def send_verify_email():
    try:
        # Create a gmail fullflaskdemomail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords
        # My key for the twitter: nafd zujo bklo qwnc

        # Email and password of the sender's Gmail account
        sender_email = "espi0001.dummy@gmail.com" # YOUR GMAIL HERE
        password = "nafd zujo bklo qwnc"  #APP PASSWORD HERE # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = "espi0001.dummy@gmail.com" # YOUR GMAIL HERE
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "Twitter"
        message["To"] = receiver_email
        message["Subject"] = "Congrats you have signed up!"

        # Body of the email
        body = f"""Congrats, you have signed up"""
        # body = f"""
        # <html>
        #     <body style="font-family:Arial, sans-serif;">
        #         <h2>Hi {user_first_name},</h2>
        #         <p>Congrats — your signup was successful!</p>
        #         <p>We're happy to have you on board.</p>
        #         <p>– The Twitter Clone Team</p>
        #     </body>
        # </html>
        # """
        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

        return "email sent"
    
    except Exception as ex:
        pass
    finally:
        pass