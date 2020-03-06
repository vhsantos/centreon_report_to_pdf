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


#Settings.csv_filepath="/tmp/centreon-servicegroup.csv"
#Settings.csv_filepath="/tmp/centreon-host.csv"
#Settings.csv_filepath = "/tmp/centreon-hostgroup.csv"

Settings.SG_ID.extend(["/tmp/centreon-hostgroup.csv", "/tmp/centreon-servicegroup.csv",  "/tmp/centreon-report/nuevo-Servicios-GASCO.csv",  "/tmp/centreon-report/hostgroup-GASCO.csv" ])
print (Settings.SG_ID)


build_report()



# If SG Report
#if Settings.report_type == 'ServiceGroup':

# If HG Report
#elif Settings.report_type == 'Hostgroup':
