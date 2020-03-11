import smtplib
from email.message import EmailMessage
import GlobalVars 
import sys

def sent_pdf_by_email():

    email_from = GlobalVars.email_from 
    email_to = GlobalVars.email_to
    print (email_to)
    email_subject = GlobalVars.email_subject 

    # check the connection to SMTP server
    try:
        server = smtplib.SMTP(host = GlobalVars.email_server ,port = GlobalVars.email_port )
        
        # If username and password are set, use it to login 
        if GlobalVars.email_authentication is True:
            server.login = (GlobalVars.email_username,  GlobalVars.email_password)
        
        # start tls
        server.starttls()
        
    except Exception as e:
        # If have any problem..
        print ("EROR: can't connect with the SMTP server")
        print (e)
        sys.exit()

    # Configure some headers
    msg = EmailMessage()
    msg['From'] = email_from
    msg['To'] = ','.join(GlobalVars.email_to)
    msg['Subject'] = email_subject


    # Open the plain text file whose name is in textfile for reading.
    with open(GlobalVars.email_body_txt_file) as body:
        msg.set_content(body.read())
        
    
    # Add the PDF File as email attachament
    pdf_filename = GlobalVars.pdf_output_file

    with open(pdf_filename, 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application/pdf', subtype='pdf', filename=pdf_filename)

    # Sent the email to all destinations
    debug = msg.as_string()
    server.sendmail(email_from, email_to, msg.as_string())
    
    server.quit
