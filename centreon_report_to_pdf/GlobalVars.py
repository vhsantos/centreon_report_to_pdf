# Global variables and parameters

#[CENTREON_SERVER]
server_url = None
AutoLogin_URL = None
username = None
password = None

#[REPORT]
period='yesterday'
custom_period_start = None
custom_period_end = None
pdf_output_file = 'centreon_report.pdf'
pdf_output_email = None
csv_download_filepath = '/tmp/centreon.csv'

#[REPORTS_ID]
hosts_groups = [0]
services_groups = [0]

#[SMTP]
send_pdf_by_email =  False
email_from = None
email_to = None
email_subject = 'Centreon PDF Report'
email_body_txt_file = 'email_body.txt'
email_server = 'localhost'
email_ssl_or_tls = 'tlsVHS'
email_port = 25
email_authentication = False
email_username = None
email_password = None

