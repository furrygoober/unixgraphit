# Unixgraphit
Quick and dirty graphing of text based data.

I am primarily a UNIX system admin, with some questionably scripting skills. 
The main goals for writing this script were to learn, have fun, and help troubleshoot issues at work.
Hopefully a few other people out there may find this script useful.

Due to environmental limitations the requirements are limited to: Python Standard Library + python matplotlib library.

You should be able to throw a wide range of text base numbers at this thing and get some graphs. (mpstat, vmstat, iostat, nicstat, prstat, pidstat, fsstat, intrstat, sar, etc)

### Options
```
usage: unix_graphit.py [-h] [-v] [-t] -of OUTFILE [-if INFILE] [-l LABELFILE]
                       [-q] [-d] [-c] [-F FIELD] [-ds DATESTRING]
                       [-df DATEFORMAT]

Process and plot text data. (ie: output from sysstat utils)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -t, --transpose       Used to transpose data, example data type: intrstat
  -of OUTFILE, --outfile OUTFILE
                        Name of the pdf to store the graph(s) in
  -if INFILE, --infile INFILE
                        Name of the file to load stat data from
  -l LABELFILE, --labelfile LABELFILE
                        Name of file to load more detailed graph labels
  -q, --quiet           Supress log output
  -d, --debug           Increase log verbosity
  -c, --customy         NOT IMPLEMENTED: Plot custom y function
  -F FIELD, --field FIELD
                        Data field separator. Default is white space
  -ds DATESTRING, --datestring DATESTRING
                        String to use to import dates. Default: %H:%M:%S
                        Options: %Y: YYYY, %y: YY, %m: MM, %d: DD, %H, %M, %S
  -df DATEFORMAT, --dateformat DATEFORMAT
                        String to use to display dates on the graphs, defaults
                        to datestring
```

### Usage
##### Example: via unix shell piping vmstat output to the script and save the output
```
cat vmstat.data.txt | ./unix_graphit.py -of vmstat.pdf

...
Line: 1
['r', 'b', 'w', 'swap', 'free', 're', 'mf', 'pi', 'po', 'fr', 'de', 'sr', 's0', 's1', 's3', 's4', 'in', 'sy', 'cs', 'us', 'sy', 'id']
...

Select line number of header row: 1

...
Line: 2
[5.0, 0.0, 0.0, 7779448.0, 8687968.0, 136.0, 1110.0, 64.0, 92.0, 98.0, 0.0, 2025.0, 97.0, -0.0, 68.0, 7.0, 17119.0, 30322.0, 19241.0, 18.0, 6.0, 76.0]
...

Select line number of data row: 2

...
Field: 21: id
Field: 22: Interval: each line is a new data sample


Select x axis. (ie: Date, or Interval): 22

Select multi-item x axis field # (ie: mpstat: CPU) or n/N for none: n

Select y axis numbers NOT to graph seperated by a space: ['22', 'n']
```

##### Example: load mpstat data from a file, get detail labels and graph the data
```
./unix_graphit.py -if mpstat.data.txt -of mpstat.pdf -l labels.txt

...
Line: 0
['Tue', 'Nov', 3.0, '10:00:49', 'EST', 2015.0, 0.0, 88.0, 2.0, 179.0, 1579.0, 583.0, 2156.0, 95.0, 299.0, 968.0, 5.0, 3151.0, 22.0, 6.0, 0.0, 72.0]

Line: 1
['Tue', 'Nov', 3.0, '10:00:49', 'EST', 2015.0, 'CPU', 'minf', 'mjf', 'xcal', 'intr', 'ithr', 'csw', 'icsw', 'migr', 'smtx', 'srw', 'syscl', 'usr', 'sys', 'wt', 'idl']

Select line number of header row: 1

Select line number of data row:0

solaris10

Select OS type:solaris10

sysperf
mpstat
vmstat

Select OS type:mpstat


Fields from selected header row

Field: 0: Tue
Field: 1: Nov
Field: 2: 3.0
Field: 3: 10:00:49
Field: 4: EST
Field: 5: 2015.0
Field: 6: CPU
Field: 7: minf
Field: 8: mjf
Field: 9: xcal
Field: 10: intr
Field: 11: ithr
Field: 12: csw
Field: 13: icsw
Field: 14: migr
Field: 15: smtx
Field: 16: srw
Field: 17: syscl
Field: 18: usr
Field: 19: sys
Field: 20: wt
Field: 21: idl
Field: 22: Interval: each line is a new data sample

Select x axis. (ie: Date, or Interval):22

Select multi-item x axis field # (ie: mpstat: CPU) or n/N for none: 6

Select y axis numbers NOT to graph seperated by a space: ['22', '6'] 0 1 2 3 4 5
```


