# read-config-files-and-access-syslogs
The config file contains valuable information pertaining to how your script will run. The config file can then be easily modified and widely distributed without having to alter the main script.Script will read syslog files according to the config file and the output can be then sent from the individual system to a central server for evaluation.

1.Script reads a configuration file projectini.ini (from the same location as the script ) that contains the following:
  a. Name of output file (projectoutput.txt)
  b. Filter options pertaining to logs
  c. Constants pertaining to actions of the script
  
2.Menu appears with instructions:

Selection--- <br />
&nbsp; 1 System accounts <br />
&nbsp; 2 System logs <br />
&nbsp; 3 Generate Report <br />
&nbsp; Press Enter to exit <br />

3.Options <br />
 nbsp 1.option 1 - p rints to screen all accounts and their group associations sorted alphabetically by account name <br />
 nbsp 2.option 2 - prints to screen system logs from /var/log/ based on the criteria specified in the projectini.ini file <br />
 nbsp 3.option 3 - Overwrites the previous file (file path/name specified in projectini.ini file) <br />
           ensp     #Name of computer <br />
           ensp     #Date and time (formatted) <br />
           ensp     #Results from option 1#Results from option 2 <br />
                
              
# How the code fulfilled the requirements

The .ini file is read and parsed using the configparser standard library. After reading the configuration separate sections are sanitised to have proper types and default values in case of missing values.

After that a simple while loop is used to present the menu to the user. For each selected option a corresponding function is executed with the parsed configuration options.

System Accounts are listed using pwd and grp libraries.
System Logs are read from /var/log/ and parsed to apply the required filters such as from date and to date.
Finally generating the report is done by writing above outputs to the configured output path.




