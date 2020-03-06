import Settings
#from CentreonData import *
from BuildPDF import *
#from reportlab.lib.units import  mm
#
#
#
#print (6*mm)

#print (Settings.csv_filepath)
#print (Settings.csv_filepath)
#Settings.csv_filepath="/tmp/centreon-report/centreon.csv"
#print (Settings.csv_filepath)


Settings.csv_filepath="/tmp/centreon-servicegroup.csv"
#Settings.csv_filepath="/tmp/centreon-host.csv"
#Settings.csv_filepath = "/tmp/centreon-hostgroup.csv"

# Initiate some variables based on the type of report (SG or HG)
get_centreon_report_type()

build_report()

# If SG Report
#if Settings.report_type == 'ServiceGroup':

# If HG Report
#elif Settings.report_type == 'Hostgroup':
