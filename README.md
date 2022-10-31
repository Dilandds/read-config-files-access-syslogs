# read-config-files-and-access-syslogs
The config file contains valuable information pertaining to how your script will run. The config file can then be easily modified and widely distributed without having to alter the main script.Script will read syslog files according to the config file and the output can be then sent from the individual system to a central server for evaluation.

1.Script reads a configuration file projectini.ini (from the same location as the script ) that contains the following:
  a. Name of output file (projectoutput.txt)
  b. Filter options pertaining to logs
  c. Constants pertaining to actions of the script
  
2.Menu appears with instructions:

Selection--- <br />
1 System accounts <br />
2 System logs <br />
3 Generate Report <br />
Press Enter to exit <br />

3.Options
 1.option 1 - prints to screen all accounts and their group associations sorted alphabetically by account name
 2.option 2 - prints to screen system logs from /var/log/ based on the criteria specified in the projectini.ini file
 3.option 3 - Overwrites the previous file (file path/name specified in projectini.ini file)
                #Name of computer
                #Date and time (formatted)
                #Results from option 1#Results from option 2
                
              
# How the code fulfilled the requirements

The .ini file is read and parsed using the configparser standard library. After reading the configuration separate sections are sanitised to have proper types and default values in case of missing values.

After that a simple while loop is used to present the menu to the user. For each selected option a corresponding function is executed with the parsed configuration options.

System Accounts are listed using pwd and grp libraries.
System Logs are read from /var/log/ and parsed to apply the required filters such as from date and to date.
Finally generating the report is done by writing above outputs to the configured output path.




