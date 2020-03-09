from BuildPDF import build_report
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="Configuration file (default = config.ini)")
parser.add_argument("-v", "--verbosity", help="increase output verbosity")

args = parser.parse_args()
print (args.config_file)
sys.exit()

if __name__== "__main__":
    build_report()


#TODO:
# Add an cover page
# Add a send email function
# Option to choice a different configuration file


