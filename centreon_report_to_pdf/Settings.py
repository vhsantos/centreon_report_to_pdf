import argparse
import configparser
import datetime
import os
import requests
import sys
from datetime import datetime as dt
from dateutil.parser import parse
import GlobalVars 



########################################
########################################
# Get the HostGroup IDs from ID section
def get_HG_IDs_from_config():
    """Get the HostGroup ID wiht space and convert it to a list"""
    # check if all HG_IDs are integers.
    try:
        hg_list = config.get('REPORTS_ID', 'Hosts_Groups').replace(' ', '').split(',')
        # Check if values are only integers
        try:
            hg_list = [int(x) for x in hg_list]
        except:
            return [0]
    except:
        print ("Can't get the Host Groups IDs from the configuration file.")
        sys.exit()
        
    return hg_list


########################################
########################################
# Get the HostGroup IDs from ID section
def get_SG_IDs_from_config():
    """Get the HostGroup ID wiht space and convert it to a list"""
    # check if all HG_IDs are integers.
    try:
        hg_list = config.get('REPORTS_ID', 'services_groups').replace(' ', '').split(',')
        # Check if values are only integers
        try:
            hg_list = [int(x) for x in hg_list]
        except:
            return [0]
    except:
        print ("Can't get the Services Groups IDs from the configuration file.")
        sys.exit()
        
    return hg_list


########################################
########################################
# Get the Period from configuration file.
def get_period_from_config():
    """Get the Period from configuration file."""
    # Check if period is defined on configuration file.
    try:
        period = config.get('REPORT', 'period')
    except:
        print ("INFO: Can't determinte the period. Using yesterday")
        period = "yesterday"
        pass
    
    return period


########################################
########################################
# Get the Custom Period start and end from configuration file.
def get_custom_periods_from_config():
    """Get the Custom Period start and end from configuration file."""
    try:
        # Get the custom dates from configuration file.
        custom_period_start = config.get('REPORT', 'custom_period_start')
        custom_period_end= config.get('REPORT', 'custom_period_end')
        
        # check if the dates are valid.
        try:
            custom_period_start = parse(custom_period_start)
            custom_period_end = parse(custom_period_end)
            
        except:
            print ("ERROR: Invalid custom period dates.")
            sys.exit()

    except configparser.NoOptionError:
        print ("ERROR: Period_Start or Period_End invalid(s)")
        sys.exit()

    return custom_period_start,  custom_period_end


########################################
########################################
# Get the Server URL from configuration file.
def get_server_url_from_config():        
    """Get the Server URL from configuration file."""
    try:
        # Get the server url from configuration file.
        server_url = config.get('CENTREON_SERVER', 'Server_URL')
            
    except configparser.NoOptionError:
        print ("ERROR: Can't find server_url on configuration file.")
        sys.exit()

    return server_url


########################################
########################################
# Get the pdf_output_file from configuration file.
def get_pdf_output_file_from_config():
    """Get the pdf_output_file from configuration file."""
    
    # check if pdf_output_file exists configuration file.
    try:
        pdf_output_file_path= config.get('REPORT', 'pdf_output_file')
        # Get the directory path
        directory = os.path.dirname(pdf_output_file_path)
        
        # check if path directory exist, if not, create it.
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                print ("Can't create directory: " + directory)
                sys.exit()
        # If exist, check if it is a directory.
        else:
            if os.path.isdir(directory) is not True:
                print ("Directory path is a file.")
                sys.exit()

    except:
        print ("Can't get the PDF_Output_File from the configuration file.")
        sys.exit()
    
    return pdf_output_file_path


########################################
########################################
# Get the csv_download_path from configuration file.
def get_csv_download_path_from_config():
    """Get the csv_download_path from configuration file."""
    # Try to get the csv path from configuration file
    try:
        csv_path = config.get('REPORT', 'csv_download_path')
    # If not, use a default
    except:
        csv_path = '/tmp/centreon.csv'
        pass

    return csv_path


########################################
########################################
# Function to get the period from configuration file and convert dates to timestamps.
def convert_periodo_to_timestamp():
    """Function to get the period from configuration file and convert dates to timestamps."""
    
    # Get the values of periods from GlobalVars.
    period = GlobalVars.period
    custom_period_start = GlobalVars.custom_period_start
    custom_period_end= GlobalVars.custom_period_end
    
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
        start_date = custom_period_start
        end_date = custom_period_end
    
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

    # Get server_url from globalvars
    server_url =  GlobalVars.server_url
    
    # Get the start and end period values.
    (Period_Start,  Periodo_End) = convert_periodo_to_timestamp()

    URLs = []
    
    # Make URL to Host Groups IDs
    for h in GlobalVars.hosts_groups:
        # Not if it is empty
        if h != 0:
            URLs.append(server_url + "/include/reporting/dashboard/csvExport/csv_HostGroupLogs.php?hostgroup=" + str(h) + "&start=" + str(Period_Start) + "&end=" + str(Periodo_End))

    # Make URL to Services Groups IDs
    for s in GlobalVars.services_groups:
        # Not if it is empty
        if s != 0:
            URLs.append(server_url + "/include/reporting/dashboard/csvExport/csv_ServiceGroupLogs.php?servicegroup=" + str(s) + "&start=" + str(Period_Start) + "&end=" + str(Periodo_End))
    
    return URLs


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
        # Get the CSV file path
        csv_path = GlobalVars.csv_download_filepath
        
        # Write CSV to file
        open(csv_path , 'wb').write(csv_download.content)
    
    else:
        print("Can't authenticate on centreon server.")
        sys.exit()

# Create a list of arguments to command line.
def get_command_line_args():
    """Create a list of arguments to command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', action='store',  dest='config_file',  default='config.ini',  help='Configuration file (default = config.ini)')
    parser.add_argument('-o', '--pdf_output', action='store',  dest='pdf_output_file',  default='centreon_report.pdf',  help='PDF file path (default = centreon_report.pdf)')
    parser.add_argument('-p', '--period', action='store',  dest='period',  help='Time Period (default = yesterday)')
    parser.add_argument('--custom_period_start', action='store',  dest='custom_period_start',   help='Custom time period start')
    parser.add_argument('--custom_period_end', action='store',  dest='custom_period_end',   help='Custom time period end')
    parser.add_argument('-H', '--hostgroup', action='append', dest='HG_ID',  default= [], type=int,   help='Hosts Groups IDs (can be used multiples times)')
    parser.add_argument('-S', '--servicegroup', action='append', dest='SG_ID',  default= [], type=int, help='Services Groups IDs (can be used multiples times)')

    args = parser.parse_args()
    
    #Change the configuration file by default if it was set on command line.
    # Default is: config.ini
    global config
    config = configparser.ConfigParser(allow_no_value=True)
    final_config_file = args.config_file
    config.read(final_config_file)
    
    # Set some global variables from configuration file to GlobalVars.
    GlobalVars.server_url = get_server_url_from_config()
    
    
    # Get the default values from configuration files and check if is necesary to overight it by command line arguments
    # Host_Groups IDs
    default_HGs = get_HG_IDs_from_config()
    args_HGs =  args.HG_ID
    GlobalVars.hosts_groups = args_HGs if args_HGs else default_HGs
    
    # Services_Groups IDs
    default_SGs = get_SG_IDs_from_config()
    args_SGs =  args.SG_ID
    GlobalVars.services_groups = args_SGs if args_SGs else default_SGs

    # PDF output filename path
    default_pdf_output_file = get_pdf_output_file_from_config()
    args_pdf_output_file = args.pdf_output_file
    GlobalVars.pdf_output_file = args_pdf_output_file if args_pdf_output_file else default_pdf_output_file
    
    # Period
    default_period = get_period_from_config()
    args_period = args.period
    GlobalVars.period = args_period if args_period else default_period
    print (GlobalVars.period)

    # Custom Period
    default_custom_period_start = None
    default_custom_period_end = None 
    args_custom_period_start = None
    args_custom_period_end = None
    
    # Get the custom period from configuration file.
    if default_period == "custom":
        (default_custom_period_start, default_custom_period_end ) = get_custom_periods_from_config()
        
    # If argument is "-p custom", get the values of start and end custom period.
    if args.period == "custom":
        try:
            args_custom_period_start = args.custom_period_start
            args_custom_period_end = args.custom_period_end
            
            try:
                args_custom_period_start = parse(args_custom_period_start)
                args_custom_period_end = parse(args_custom_period_end)

            except:
                print ("ERROR: Invalid custom period dates.")
                sys.exit()
    
        except:
            print ("ERROR: Period_Start or Period_End invalid(s)")
            sys.exit()
        
    # Put custom periods (from configuration or argument) on the Global Vars    
    GlobalVars.custom_period_start = args_custom_period_start if args_custom_period_start else default_custom_period_start
    GlobalVars.custom_period_end = args_custom_period_end if args_custom_period_end else default_custom_period_end


