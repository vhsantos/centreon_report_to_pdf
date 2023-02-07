import smtplib
from email.message import EmailMessage

import GlobalVars
import sys


def sent_pdf_by_email():

    email_from = GlobalVars.email_from
    email_to = GlobalVars.email_to
    email_subject = GlobalVars.email_subject

    # check the connection to SMTP server
    try:
        # Check if connection is SSL or TLS from configuration file
        if GlobalVars.email_ssl_or_tls.lower() == "ssl":
            server = smtplib.SMTP_SSL(
                GlobalVars.email_server, GlobalVars.email_port)
        else:
            server = smtplib.SMTP(GlobalVars.email_server,
                                  GlobalVars.email_port)

        # Disable debug messages
        server.set_debuglevel(False)

        # try one ehlo if not a helo
        server.ehlo_or_helo_if_needed()

        # check if server have STARTTLs enable
        if server.has_extn('STARTTLS'):
            # If yes, starttls connection
            server.starttls()
            server.ehlo()

        # If username and password are set, use it to login
        if GlobalVars.email_authentication is True:
            try:
                server.login(GlobalVars.email_from, GlobalVars.email_password)
            except Exception as e:
                # If have any problem, print the error
                server.quit()
                print(e)
                sys.exit()

    except Exception as e:
        # If have any problem..
        print("ERROR: can't connect with the SMTP server")
        print(e)
        sys.exit()

    # Create the email message
    msg = EmailMessage()

    # Configure some headers
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
        msg.add_attachment(content, maintype='application/pdf',
                           subtype='pdf', filename=pdf_filename)

    # Sent the email to all destinations
    try:
        server.sendmail(email_from, email_to, msg.as_string())
    except Exception as e:
        print("ERROR: Problem sending the email")
        print(e)
        server.quit()
        sys.exit()

    finally:
        server.quit
