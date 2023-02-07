import pandas as pd
import GlobalVars

# Function to get the two first lines from centreon CSV
# data example:
# 1 ServiceGroup;Begin date; End date; Duration
# 2 Service_name;23/02/2020 00:00:00; 01/03/2020 00:00:00; 604800s


def get_centreon_csv_info():
    """Function to get the two first lines from centreon CSV"""

    # Read the CSV File
    # Conserver "begin date" and "end date" to datetime64
    csv_info = pd.read_csv(GlobalVars.csv_download_filepath,
                           sep=";",  nrows=1, parse_dates=[1, 2],  dayfirst=True)

    return csv_info


########################################
########################################
# Function to get the information resumen from centreon CSV between lines 5-11
# The manual head is necesary because a error in the CSV file that add an extra ";" at the end of lines.
# data example:
#  5 Status;Total Time;Mean Time;Alert
#  6 OK;99.94%;99.94%;14;
#  7 Warning;0.01%;0.01%;3;
#  8 Critical;0.05%;0.05%;12;
#  9 Unknown;0%;0%;0;
# 10 Scheduled Downtimes;0%;;;
# 11 Undetermined;0%;;;
def get_centreon_csv_resume():
    """Function to get the information resumen from centreon CSV between lines 5-11"""

    # Define columns to be used
    if GlobalVars.report_type == 'ServiceGroup':
        PD_NROWS = 6
        PD_SKIPROWS = 4
        PD_USECOLS = ["Status", "Total Time",   "Mean Time",  "Alert"]
    elif GlobalVars.report_type == 'Hostgroup':
        PD_NROWS = 5
        PD_SKIPROWS = 3
        PD_USECOLS = ["Status", "Total Time",   "Mean Time",  " Alert"]

    # Read the CSV File
    csv_resume = pd.read_csv(GlobalVars.csv_download_filepath,  sep=";",
                             nrows=PD_NROWS,  skiprows=PD_SKIPROWS,  usecols=PD_USECOLS)

    # Rename columns names that will be in the PDF
    csv_resume.columns = ["Status",  "Total Time",  "Mean Time",  "Alerts"]

    # Clean trash (% or spaces) at numerics columns
    # Convert columns "Total Time" and  "Mean Time" to numbers (strip the %)
    csv_resume['Total Time'] = csv_resume['Total Time'].str.replace('%', '')
    csv_resume['Mean Time'] = csv_resume['Mean Time'].str.replace('%', '')

    # Fill NAN with 0
    csv_resume = csv_resume.fillna(0)

    # convert Alerts to int (BUG at csv_reader)
    csv_resume['Alerts'] = csv_resume['Alerts'].astype(int)

    # Capitalize all strings at colum 0 - BUG diff between CSV
    csv_resume = csv_resume.applymap(
        lambda s: s.capitalize() if type(s) == str else s)

    # Retun the details dataframe
    return csv_resume


########################################
########################################
# Function to get the information details from centreon CSV placed after line 15
# Is necesary to force pandas to process the blank line to know where we need to stop
#
# data example of ServiceGroup
# 15 Host;Service;OK %;OK Mean Time %;OK Alert;Warning %;Warning Mean Time %;Warning Alert;Critical %;Critical Mean Time %;Critical Alert;Unknown %;UnknownMean Time %;Unknown Alert;Scheduled Downtimes %;Undetermined
# 16 server-dhcp;Trafico;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# 17 server-93;check_hp_hardware;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# [...]
# 58 server-4;Load;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# 59
# 60
# 61 Day;Duration;OK Mean Time;OK Alert;Warning Mean Time;Warning Alert;Unknown Mean Time;Unknown Alert;Critical Mean     Time;Critical Alert;Day
# 62 1582945200;55450.7462s;99.96%;2;0.02%;1;0%;0;0.02%;1;2020-02-29 00:00:00;
def get_centreon_csv_details_HG():
    """Function to get the information details from centreon CSV placed after line 12"""
    # Define columns to be used
    COLUMN_DATA = ['Hosts', 'Up %', 'Up Alert', 'Down %', 'Down Alert',
                   'Unreachable %', 'Unreachable Alert', 'Scheduled Downtimes %', 'Undetermined %']

    # read the CSV file after line 15 where the headers start
    # Force dtype to "Unknown Alert" - BUG :-(
    csv_details = pd.read_csv(GlobalVars.csv_download_filepath,  sep=";",  skiprows=11,
                              skip_blank_lines=False,  usecols=COLUMN_DATA,  dtype={"Unreachable Alert": 'str'})

    # check by blank lines
    try:
        # get the line number where is the first blank line
        first_row_with_all_NaN = csv_details[csv_details.isnull().all(
            axis=1) == True].index.tolist()[0]
        # if exists a blank line, return all values before the blank line.
        csv_details = csv_details[0:first_row_with_all_NaN]
    except:
        # if don't exists a blank line, continue
        pass

    # Clean trash (% or spaces) at numerics columns
    for col_name in COLUMN_DATA:
        if col_name != 'Hosts' and col_name != 'Service':
            csv_details[col_name] = csv_details[col_name].astype(
                str).str.replace('%', '')
            csv_details[col_name] = csv_details[col_name].astype(
                str).str.replace(' ', '')

    # Rename columns names that will be in the PDF
    csv_details.columns = ['Hosts', 'Up', '', 'Down',
                           '', 'Unreachable', '', 'Scheduled', 'Undetermined']

    # convert all percentages to float
    for col_name in ['Up', 'Down', 'Unreachable', 'Scheduled', 'Undetermined']:
        csv_details[col_name] = csv_details[col_name].astype(float)

    # Convert all alers columns to integer
    csv_details[''] = csv_details[''].astype(int)

    # Sort CSV by OK descending (to get focus in the most worse first)
    if GlobalVars.sort_data_by_name is False:
        csv_details.sort_values(['Up', 'Hosts'],  axis=0, ascending=[
                                True, True], inplace=True)

    # Retun the details dataframe
    return csv_details


########################################
########################################
# Function to get the information details from centreon CSV placed after line 15
# Is necesary to force pandas to process the blank line to know where we need to stop
#
# data example of ServiceGroup
# 15 Host;Service;OK %;OK Mean Time %;OK Alert;Warning %;Warning Mean Time %;Warning Alert;Critical %;Critical Mean Time %;Critical Alert;Unknown %;UnknownMean Time %;Unknown Alert;Scheduled Downtimes %;Undetermined
# 16 server-dhcp;Trafico;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# 17 server-93;check_hp_hardware;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# [...]
# 58 server-4;Load;100%;100%;0;0%;0%;0;0%;0%;0;0%;0%;0;0 %;0%
# 59
# 60
# 61 Day;Duration;OK Mean Time;OK Alert;Warning Mean Time;Warning Alert;Unknown Mean Time;Unknown Alert;Critical Mean     Time;Critical Alert;Day
# 62 1582945200;55450.7462s;99.96%;2;0.02%;1;0%;0;0.02%;1;2020-02-29 00:00:00;
def get_centreon_csv_details_SG():
    """Function to get the information details from centreon CSV placed after line 15"""
    # Define columns to be used
    COLUMN_DATA = ["Host", "Service", "OK %", "OK Alert", "Warning %", "Warning Alert", "Critical %",
                   "Critical Alert", "Unknown %", "Unknown Alert",  "Scheduled Downtimes %",  "Undetermined"]

    # read the CSV file after line 15 where the headers start
    # Force dtype to "Unknown Alert" - BUG :-(
    csv_details = pd.read_csv(GlobalVars.csv_download_filepath,  sep=";",  skiprows=14,
                              skip_blank_lines=False,  usecols=COLUMN_DATA,  dtype={"Unknown Alert": 'str'})

    # check by blank lines
    try:
        # get the line number where is the first blank line
        first_row_with_all_NaN = csv_details[csv_details.isnull().all(
            axis=1) == True].index.tolist()[0]
        # if exists a blank line, return all values before the blank line.
        csv_details = csv_details[0:first_row_with_all_NaN]
    except:
        # if don't exists a blank line, continue
        pass

    # Clean trash (% or spaces) at numerics columns
    for col_name in COLUMN_DATA:
        if col_name != "Host" and col_name != "Service":
            csv_details[col_name] = csv_details[col_name].astype(
                str).str.replace('%', '')
            csv_details[col_name] = csv_details[col_name].astype(
                str).str.replace(' ', '')

    # Rename columns names that will be in the PDF
    csv_details.columns = ['Host', 'Service', 'OK', '', 'Warning',
                           '', 'Critical', '', 'Unknown', '', 'Scheduled', 'Undetermined']

    # convert all percentages to float
    for col_name in ['OK', 'Warning', 'Critical', 'Unknown', 'Scheduled', 'Undetermined']:
        csv_details[col_name] = csv_details[col_name].astype(float)

    # Convert all alers columns to integer
    csv_details[''] = csv_details[''].astype(int)

    # Sort CSV by OK descending (to get focus in the most worse first)
    if GlobalVars.sort_data_by_name is False:
        csv_details.sort_values(["OK", "Host",  "Service"],  axis=0, ascending=[
                                True, True, True], inplace=True)

    # Retun the details dataframe
    return csv_details


########################################
########################################
# Function to get the type of report (Host|Hostgroup|ServiceGroup)
# and set some variables.
def get_centreon_report_type():
    """Function to get the type of report (Host|Hostgroup|ServiceGroup) and set some variables."""

    # Get the type of report
    data_df = get_centreon_csv_info()

    # Get the content of first field on CSV
    GlobalVars.report_type = data_df.columns[0]

    # Get the report type
    if GlobalVars.report_type == 'ServiceGroup':
        GlobalVars.report_type_name = 'Service Group'
    elif GlobalVars.report_type == 'Hostgroup':
        GlobalVars.report_type_name = 'Host Group'
    elif GlobalVars.report_type == 'Host':
        GlobalVars.report_type_name = 'Host'
    else:
        print("Can't determinte the type of report on the CSV.")
        # Finish  :-(
        quit()
