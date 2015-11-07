# Unixgraphit
Quick and dirty graphing of text based data.

Due to environmental limitations the requirements are: Python Standard Library + python matplotlib library.


### Options
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


### Usage

