import pandas as pd
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

# Load the email data from the CSV file
try:
    emails = pd.read_csv('email.csv')
    print(emails)
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# Define email server details
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "jainavijeet@gmail.com"
password = "your_password_here"

# Create a secure SSL context
context = ssl.create_default_context()

# Connect to the email server
try:
    server = smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.login(sender_email, password)
except Exception as e:
    print(f"Error connecting to the email server: {e}")
    exit()

# Loop through the email list and send emails
for index, row in emails.iterrows():
    recipient_email = row["Emails"]
    recipient_name = row["Names"]

    # Create a multipart message container
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Application for Internship/SDE Role"

    # Email body
    body = f"""\
Dear {recipient_name},
I hope this email finds you well.

My name is Avijeet Jain, and I am writing to express my interest in internship and Software Development Engineer (SDE) roles within your organization.

I am passionate about software development and specialize in building robust web applications using the MERN stack (MongoDB, Express, React, and Node.js). 
I have experience with RESTful APIs and front-end development (HTML, CSS, JavaScript). Additionally, I am skilled in UI/UX design, using tools like Adobe XD, 
Figma, and Sketch.

As the Chapter Lead of Google Developers Student Clubs and a core member of Abhigyan Abhikaushalam Students’ Forum, I have organized and led numerous events
and workshops, enhancing my project management and teamwork skills.

I am excited about the opportunity to contribute to your team and grow in a challenging environment. Please find my resume attached for your reference. 
I am available for an interview at your earliest convenience.

Thank you for considering my application. I look forward to discussing how my skills align with your organization's goals.

Sincerely,
Avijeet Jain
"""
    message.attach(MIMEText(body, "plain"))

    # Attach the resume file
    resume_file_path = "AvijeetJain-Resume.pdf"
    try:
        with open(resume_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename=AvijeetJain-Resume.pdf",
            )
            message.attach(part)
    except Exception as e:
        print(f"Error attaching file: {e}")
        continue

    # Send the email
    try:
        server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Sent email to {recipient_name} at {recipient_email}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")

# Close the server connection
server.quit()
