import configparser
import sys
import os
import datetime
from datetime import datetime as dt
from dateutil.parser import parse
import requests

config = configparser.ConfigParser(allow_no_value=True)
config.read('config.ini')

# Global variables and parameters
#SG_IDs = []
#HG_IDs = []
csv_filepath = "/tmp/centreon.csv"
#pdf_output_file = "/tmp/centreon_report.pdf"
report_type = "x"
report_type_name = "x"


########################################
########################################
# Get the HostGroup IDs from ID section
def get_HG_IDs_from_config():
    """Get the HostGroup ID wiht space and convert it to a list"""
    # check if all HG_IDs are integers.
    try:
        hg_list = config.get('REPORTS_ID', 'HostGroups').replace(' ', '').split(',')
        # Check if values are only integers
        try:
            hg_list = [int(x) for x in hg_list]
        except:
            return 0
    except:
        print ("Can't get the Host Groups IDs from the configuration file.")
        quit()
        
    return hg_list


########################################
########################################
# Get the HostGroup IDs from ID section
def get_SG_IDs_from_config():
    """Get the HostGroup ID wiht space and convert it to a list"""
    # check if all HG_IDs are integers.
    try:
        hg_list = config.get('REPORTS_ID', 'ServicesGroups').replace(' ', '').split(',')
        # Check if values are only integers
        try:
            hg_list = [int(x) for x in hg_list]
        except:
            return 0
    except:
        print ("Can't get the Services Groups IDs from the configuration file.")
        quit()
        
    return hg_list


########################################
########################################
# Function to get the period from configuration file and convert dates to timestamps.
def get_report_period():
    """Function to get the period from configuration file and convert dates to timestamps."""
    
    # Check if period is defined on configuration file.
    try:
        period = config.get('REPORT', 'period')
    except:
        print ("INFO: Can't determinte the period. Using yesterday")
        period = "yesterday"
    
    # Get the actual date/time.
    now = dt.now()
    
    # select the start and end dates from period.
    if period == "yesterday":
        start_date =  now - datetime.timedelta(days=1)
        end_date = now
    
    elif period == "this_week":
        start_date = now - datetime.timedelta(days=now.weekday())
        end_date = now
    
    elif period == "last_week":
        start_date = now - datetime.timedelta(days=now.weekday(),  weeks=1)
        end_date = now - datetime.timedelta(days=now.weekday())
    
    elif period == "this_month":
        start_date = now.replace(day=1)
        end_date = now
    
    elif period == "last_month":
        last_mont_last_day = now.replace(day=1) - datetime.timedelta(days=1)
        start_date = last_mont_last_day .replace(day=1)
        end_date = now.replace(day=1)
        
    elif period == "this_year":
        start_date = now.replace(day=1, month=1 )
        end_date = now

    elif period == "last_year":
        last_year_last_day = now.replace(day=1,  month=1) - datetime.timedelta(days=1)
        start_date = last_year_last_day.replace(day=1,  month=1)
        end_date = now.replace(day=1, month=1 )

    elif period == "custom":
        try:
            # Get the custom dates from configuration file.
            perido_start = config.get('REPORT', 'custom_period_start')
            perido_end= config.get('REPORT', 'custom_period_end')
            
            # check if the dates are valid.
            try:
                start_date = parse(perido_start)
                end_date = parse(perido_end)
                
            except:
                print ("ERROR: Invalid custom period dates.")
                sys.exit()
                
        except configparser.NoOptionError:
            print ("ERROR: Period_Start or Period_End invalid(s)")
            sys.exit()
    
    # Convert dates to integer/timestamps
    start_date = int(start_date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    end_date = int(end_date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    
    return (start_date,  end_date)


########################################
########################################
# Generate the URL to download based on the configuration file
def prepare_csv_url():
    """Generate the URL to download based on the configuration file"""
    # examples of URLs of download CSV
    #https://SERVER_URL/include/reporting/dashboard/csvExport/csv_HostLogs.php?host=55&start=1580785200&end=1583377200
    #https://SERVER_URL/include/reporting/dashboard/csvExport/csv_HostGroupLogs.php?hostgroup=11&start=1583377200&end=1583463600
    #https://SERVER_URL/include/reporting/dashboard/csvExport/csv_ServiceGroupLogs.php?servicegroup=13&start=1583377200&end=1583463600

    # Check by server_url on the configuration file.
    try:
        # Get the server url from configuration file.
        server_url = config.get('CENTREON_SERVER', 'Server_URL')
            
    except configparser.NoOptionError:
        print ("ERROR: Can't find server_url on configuration file.")
        sys.exit()

    # Get the list of Host Groups, Services Groups and periods from configuration file.
    HG_IDs = get_HG_IDs_from_config()
    SG_IDs = get_SG_IDs_from_config()
    (Period_Start,  Periodo_End) = get_report_period()

    URLs = []
    
    # Make URL to Host Groups IDs
    if HG_IDs != 0:
        for h in HG_IDs:
            URLs.append(server_url + "/include/reporting/dashboard/csvExport/csv_HostGroupLogs.php?hostgroup=" + str(h) + "&start=" + str(Period_Start) + "&end=" + str(Periodo_End))

    # Make URL to Services Groups IDs
    if SG_IDs != 0:
        for s in SG_IDs:
            URLs.append(server_url + "/include/reporting/dashboard/csvExport/csv_ServiceGroupLogs.php?servicegroup=" + str(s) + "&start=" + str(Period_Start) + "&end=" + str(Periodo_End))
    
    return URLs


########################################
########################################
# Get the pdf_output_file from configuration file.
def get_pdf_output_file_path():
    """Get the pdf_output_file from configuration file."""
    
    # check if pdf_output_file exists configuration file.
    try:
        pdf_output_file_path= config.get('REPORT', 'pdf_output_file')
        # Get the directory path
        directory = os.path.dirname(pdf_output_file_path)
        
        # check if directory exists. If not, create it.
        if not os.path.exists(directory):
            os.makedirs(directory)

    except:
        print ("Can't get the PDF_Output_File from the configuration file.")
        quit()
    
    return pdf_output_file_path


########################################
########################################
# Generate the URL to login based on the configuration file
def prepare_login_url():
    """Generate the URL to login based on the configuration file"""

    #Example URL Login with autologin
    # 'https://SERVER_NAME/centreon/main.php?o=c&autologin=1&useralias=USERNAME&token=TOKEN'
    #Example URL Login with username and password
    # 'https://SERVER_NAME/centreon/index.php?useralias=USERNAME&password=PASSWORD&submitLogin=Connect'

    # Check if AutoLogin exist
    try:
        login_url = config.get('CENTREON_SERVER', 'AutoLogin_URL')
        return login_url
    except:
        pass
    
    # If Autologin dont exist, try to get the username and password 
    try:
        server = config.get('CENTREON_SERVER', 'Server_URL')
        user = config.get('CENTREON_SERVER', 'User')
        passwd = config.get('CENTREON_SERVER', 'Password')
        
        login_url = ( server + '/index.php?useralias=' + user + '&password=' + passwd + '&submitLogin=Connect')
        return login_url
        
    # If none is avaliable, exit
    except:
        print ("Can't found AutoLogin or Username and Password in the configuration file.")
        sys.exit()


########################################
########################################
def download_csv(url_csv):
    # GET the URL to login
    LOGIN_URL =  prepare_login_url()
    
    # Login and get the session/cookies.
    centreon_session = requests.session()
    centreon_session.get(LOGIN_URL)
    
    # Download CSV file
    csv_download = centreon_session.get(url_csv)

    # Check if download was OK (200)
    if 'undefined' in (csv_download.text):
        print ('ERROR: Host Group o Service Group ID not found on Centreon server.')
        sys.exit()
    elif csv_download.status_code == 200 and 'Bad Session' not in (csv_download.text):
        # Get the CSV file paht
        csv_path = get_csv_path()
        
        # Write CSV to file
#        csv_download = centreon_session.get(url_csv)
        open(csv_path , 'wb').write(csv_download.content)
    
    else:
        print("Can't authenticate on centreon server.")
        sys.exit()


########################################
########################################
def get_csv_path():
        # Try to get the csv path from configuration file
        try:
            csv_path = config.get('REPORT', 'csv_download_path')
        # If not, use a default
        except:
            csv_path = '/tmp/centreon.csv'
            pass
        
        return csv_path
    
