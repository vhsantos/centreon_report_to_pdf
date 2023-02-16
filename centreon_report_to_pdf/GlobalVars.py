# Global variables and parameters

# [CENTREON_SERVER]
server_url = None
AutoLogin_URL = None
username = None
password = None

# [REPORT]
period = 'yesterday'
custom_period_start = None
custom_period_end = None
pdf_output_file = 'centreon_report.pdf'
csv_download_filepath = '/tmp/centreon.csv'
sort_data_by_name = True
column_size_host = 'auto'
column_size_service = 'auto'

# [REPORTS_ID]
hosts_groups = [0]
services_groups = [0]

# [SMTP]
send_pdf_by_email = False
email_from = None
email_to = None
email_subject = 'Centreon PDF Report'
email_body_txt_file = 'email_body.txt'
email_server = 'localhost'
email_ssl_or_tls = 'tls'
email_port = 25
email_authentication = False
email_username = None
email_password = None

# [COVER]
include_cover_page = False
cover_logo_file = ''
cover_logo_size_x = 100
cover_logo_size_y = 50
cover_title_1 = 'Availability Report'
cover_title_2 = ''
cover_text_1 = ''
cover_text_2 = ''
cover_extra_info = True
cover_date_format = '%d/%B/%Y'
