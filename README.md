# Unixgraphit
Quick and dirty graphing of text based data.

Due to environmental limitations the requirements are: Python Standard Library + python matplotlib library.


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
##### Example: unix shell pipe vmstat output to the script and save the output
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


