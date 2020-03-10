from Settings import *
import GlobalVars
from BuildPDF import build_report


if __name__== "__main__":

    get_command_line_args()
#    
#    sys.exit()
    
    build_report()


#TODO:
# Add an cover page
# Add a send email function
# Option to choice a different configuration file


