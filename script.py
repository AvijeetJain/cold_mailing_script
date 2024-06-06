from email import encoders
from email.base64mime import body_decode
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import pandas as pd

emails = pd.read_csv('email.csv')

print(emails)

port = 465  # For SSL
context = ssl.create_default_context()

server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)

server.login("jainavijeet@gmail.com", your_password_here)

for index in range(len(emails)):
    # Create a multipart message container
    message = MIMEMultipart()
    message["From"] = "jainavijeet@gmail.com"
    message["To"] = emails["Emails"][index]
    message["Subject"] = "Application for Internship/SDE Role"

    # Attach the plain text message
    body = f"""\
Dear {emails["Names"][index]},
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

    resume_file_path = "AvijeetJain-Resume.pdf"  
    with open(resume_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=AvijeetJain-Resume.pdf",
        )
        message.attach(part)

    # Send the email inside the loop
    server.sendmail("jainavijeet@gmail.com", emails["Emails"][index], message.as_string())
    print(f"Sent email to {emails['Names'][index]}")

# Close the connection outside the loop
server.quit()