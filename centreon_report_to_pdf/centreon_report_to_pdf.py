from Settings import get_command_line_args
from BuildPDF import build_report
from SMTP import sent_pdf_by_email
import sys 


if __name__== "__main__":
    
    # Get and set options in base to configuration file or command line arguments.
    get_command_line_args()

#    sys.exit()
    sent_pdf_by_email()
    
    sys.exit()
    build_report()


### TODO
# - Add more arguments options
# - Add option to sent PDF by email
# - Add a cover page.

