# Centreon Report to PDF

**centreon_report_to_pdf** is a software to generate PDF files from [centreon](https://www.centreon.com/en/) dashboard Hosts and Services Group.

Basically, it connect to [centreon](https://www.centreon.com/en/) server using an autologin link or a username/password to download the HostGroup/ServiceGroup CSV file from a specifc period of time. After this, it process the CSV file and generate the PDF with charts, resume and details table. Optional, you can add a Cover Page and sent the PDF Report by email too.

# Tutorial
[Eric Coquard](https://www.sugarbug.fr/) wrote a great tutorial (*in French*) showing how to configure and use centreon_report_to_pdf [here](https://www.sugarbug.fr/atelier/techniques/ihmweb/centreon/centreon-report-to-pdf/). Thanks man !!! :-D

# Installation

**centreon_report_to_pdf** have been test on Debian and Ubuntu (lasted versions), but it should work in any environment with  [python](https://www.python.org/) v3.5+ and some dependencies.

* Clone this repository:
```
git clone https://github.com/vhsantos/centreon_report_to_pdf.git
```

* Install the dependencies:
```
cd centreon_report_to_pdf
pip install -r requirements.txt
```

# Usage

You will need a ***'config.ini'*** file before use this software. On the repository exists a *"config_example.ini"* that you can copy/rename to use.

After edit your 'config.ini' file, you only need to run:
```
python3 centreon_report_to_pdf.py
```
to generate the PDF report.


# Options

Some options are allowed at the command line to overrirde the default options on configuration file:
- -c or --config filename
    - Allow your specific an alternative config file name. For example: 
    ```
    python3 centreon_report_to_pdf.py -c client1_config.ini
    ```
- -H or --hostgroup NUMBER
    - Allow your to specific the hostgroup number. You can repeat this option to group two or more hosts groups on the report, for example: 
    ```
    python3 centreon_report_to_pdf.py -H 2 -H 12 -H 20
    ```
- -S or --servicegroup NUMBER
    - Allow your to specific the servicegroup number. You can repeat this option to group two or more services groups on the report, for example: 
    ```    
    python3 centreon_report_to_pdf.py -S 1 -S 14 -S 15
    ```
- -p or --period PERIOD
    - Allow your to specific the time period to your report. Valid values to periods are:
        - yesterday
        - this_week
        - last_week
        - this_month
        - last_month
        - this_year
        - last_year

    ```    
    python3 centreon_report_to_pdf.py -p this_week
    python3 centreon_report_to_pdf.py -p this_year
    ```

- -o or --pdf_output /path/to/report.pdf
    - Allow your specific the path to pdf report.
    ```    
    python3 centreon_report_to_pdf.py -H 1 -S 14 -S 15 -o /tmp/my_report.pdf
    ```
- --email_to 
     - Allow your to specific a new email address, for example:
     ```
     python3 centreon_report_to_pdf.py --email_to user@gmail.com --email_to boss@office365.com --email_to it@mycompany.com
     ```

# Host and Service Group IDs

To obtain the list of Hosts and Services Groups from centreon, you can use the [clapi](https://documentation.centreon.com/docs/centreon/en/lastest/api/clapi/index.html) command line. Some examples:

- To get all the **[Hosts Groups IDs](https://documentation.centreon.com/docs/centreon/en/latest/api/clapi/objects/host_groups.html)**
```
/usr/share/centreon/bin/centreon -u USERNAME -p PASSWORD -o HG -a show
```

- To get all the **[Services Groups IDs](https://documentation.centreon.com/docs/centreon/en/latest/api/clapi/objects/service_groups.html)**
```
/usr/share/centreon/bin/centreon -u USERNAME -p PASSWORD -o SG -a show
```

# Cover Page
You can add a Cover Page to your reports with a logo/image and some titles/texts. Please, check the configuration file to enable it and see all parameters.


# Sent PDF Report by email
You can change the configuration file to sent the PDF report by email. Actually, you can:
- Use a local SMTP server or an external (gmail, office465, etc) with/out authentication.
- Sent the PDF Report to one or more recipients.
- Use a text file like email body template.


# Report Example
[centreon_report.pdf](http://downloads.vhsantos.net/centreon_report.pdf)


#### TODO
 - Add more arguments options
 - Add some PDF report to repository


