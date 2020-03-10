from Settings import get_command_line_args
from BuildPDF import build_report


if __name__== "__main__":
    
    # Get and set options in base to configuration file or command line arguments.
    get_command_line_args()

    
    build_report()


### TODO
# - Add more arguments options
# - Add option to sent PDF by email
# - Add a cover page.
# - Add some PDF report to repository

