import Settings
from Settings import *
from BuildPDF import build_report

prepare_csv_url()
quit()

Settings.HG_IDs = get_config_HG_IDs()

print (Settings.HG_IDs)

Settings.SG_IDs = get_config_SG_IDs()
print (Settings.SG_IDs)

Settings.SG_IDs.extend(["/tmp/centreon-hostgroup.csv", "/tmp/centreon-servicegroup.csv",  "/tmp/centreon-report/nuevo-Servicios-GASCO.csv",  "/tmp/centreon-report/hostgroup-GASCO.csv" ])


build_report()



# If SG Report
#if Settings.report_type == 'ServiceGroup':

# If HG Report
#elif Settings.report_type == 'Hostgroup':
