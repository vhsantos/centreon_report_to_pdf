# Centreon Report to PDF

**centreon_report_to_pdf** is a software to generate PDF files from [centron](https://www.centreon.com/en/) dashbard Hosts and Services Group.

Basically, it connect to [centron](https://www.centreon.com/en/) using an autologin link or a username and password to download the HostGroup / ServiceGroup CSV file from a specifc period of time. After this, it process the field and genarate the PDF with charts, resume and details table.

### Installation

**centreon_report_to_pdf** have been test on Debian and Ubuntu (lasted versions), but it should work in any enviroment with  [python](https://www.python.org/) v3.5+ and some dependeces.

* Clone this repository.
* Install the dependencies.
```
cd centreon_report_to_pdf
pip install -r requirements.txt
```

### Usage

You will need a config.ini file before use this softare. On the repository exist a *"config_example.ini"* that you can copy/rename to use.

After edit your config file, you only need to run:
```
centreon_report_to_pdf
```
to generate the PDF.


### Options

Some options are allowed at the command line:
- -c or --config filename
    - Allow your specific an alternative config file name. For example: 
    ```centreon_report_to_pdf -c client1_config.ini```
- -H or --hostgroup NUMBER
    - Allow your specific the hostgroup number. You can repeat this option to group two or more hosts groups on the report, for example: 
    ```centreon_report_to_pdf -H 2 -H 12 -H 20```
- -S or --servicegroup NUMBER
    - Allow your specific the hostgroup number. You can repeat this option to group two or more services groups on the report, for example: 
    ```centreon_report_to_pdf -S 1 -S 14 -S 15```


### Host Group and Service Group IDs

To obtain the list of Hosts and Services Groups from centreon, you can use the [clapi](https://documentation.centreon.com/docs/centreon/en/lastest/api/clapi/index.html) command line. Some examples:

- To get all the **[Hosts Groups IDs](https://documentation.centreon.com/docs/centreon/en/latest/api/clapi/objects/host_groups.html)
```/usr/share/centreon/bin/centreon -u USERNAME -p PASSWORD -o HG -a show```

- To get all the **[Services Groups IDs](https://documentation.centreon.com/docs/centreon/en/latest/api/clapi/objects/service_groups.html)**
```/usr/share/centreon/bin/centreon -u USERNAME -p PASSWORD -o SG -a show```

### TODO
 - Add more arguments options
 - Add option to sent PDF by email
 - Add a cover page.
 - Add some PDF report to repository

