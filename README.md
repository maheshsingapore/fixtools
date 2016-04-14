# fixtools
python tools for analyzing fix messages

<any fix feed>| ft compare 
<any fix feed>| ft compare [-a| exact tag numbers to compare] 
     Eg.: ft extract '3=' any.application.log| ft compare 
     Eg.: less -f any.fix.feed| ft compare 6 
     Eg.: less -f any.fix.feed| ft compare -a 

ft extract <filter condition> <log file> 
     E.g.: ft extract '3=' any.application.log 
     E.g.: less -f any.application.log| ft extract '3=' 

ft serve [path] [port] 
     Eg.: ft serve 
     Eg.: ft serve templates 
     Eg.: ft serve ~ 9999 

<any fix feed>| ft tabulate <list of space-separated tags to print as a table> 
     Eg.: ft extract '3=' any.application.log| ft tabulate 3 37  4 
     Eg.: less -f any.fix.feed| ft tabulate 3 37  4 
     Eg.: less -f any.fix.feed| ft tabulate --csv 3 37  4 
     Eg.: less -f any.fix.feed| ft tabulate -c 3 37  4 

ft simulate <template> 
     E.g.: ft simulate templates/Execution.template 
