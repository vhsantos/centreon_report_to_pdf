from Settings import get_command_line_args
from BuildPDF import build_report
from SMTP import sent_pdf_by_email
import GlobalVars


if __name__ == "__main__":

    # Get and set options in base to configuration file or command line arguments.
    get_command_line_args()

    # Built the PDF report.
    build_report()

    # If send_pdf_by_email is enable on configuration file, sent the PDF by email
    if GlobalVars.send_pdf_by_email is True:
        sent_pdf_by_email()


# TODO
# - Add more arguments options
