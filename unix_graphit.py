#!/usr/bin/env python


#######################
# functions
#######################

def getargs():

    parser = argparse.ArgumentParser(version='Version: 0.8 2015.11.05',description='Process and plot text data. (ie: output from sysstat utils)')
    parser.add_argument('-t','--transpose',action='store_true',default=False, help='Used to transpose data, example data type: intrstat')
    parser.add_argument('-of','--outfile',action='store',required=True,help='Name of the pdf to store the graph(s) in')
    parser.add_argument('-if','--infile',type = argparse.FileType('r'),help='Name of the file to load stat data from')
    parser.add_argument('-l','--labelfile',type=argparse.FileType('r'),help='Name of file to load more detailed graph labels')
    parser.add_argument('-q','--quiet',action='store_true',default=False,help='Supress log output')
    parser.add_argument('-d','--debug',action='store_true',default=False,help='Increase log verbosity')
    parser.add_argument('-c','--customy',action='store_true',default=False,help='NOT IMPLEMENTED: Plot custom y function')
    parser.add_argument('-F','--field',action='store',default=None,help='Data field separator. Default is white space')
    parser.add_argument('-ds','--datestring',action='store',default='%H:%M:%S',help='String to use to import dates. Default: %%H:%%M:%%S Options: %%Y: YYYY, %%y: YY, %%m: MM, %%d: DD, %%H, %%M, %%S')
    parser.add_argument('-df','--dateformat',action='store',default=None,help='String to use to display dates on the graphs, defaults to datestring')


    return parser.parse_args()

def loglevel(args,message,level):
    if args.quiet:
        pass
    elif level == 'normal':
        print('\n' + message)
    elif level == 'debug' and args.debug:
        print('\n' + message)

def isnumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

	return False

def formatdata(line,field):
# format data, turn number values in to int instead of string type
# return an array of scrubbed data
# also return hash of line types
    fixedline = []
    linetype = ''

    for item in line.split(field):
        if isnumber(item):
            fixedline.append(float(item))
            linetype = linetype + 'f'
        else:
            fixedline.append(item)
            linetype = linetype + 's'
    return (fixedline, linetype)

def piperead(field):
# read data in from unix command line
# return an array of arrays

    hashtype= {}
    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if not line:
            break
        # load line data get back formated line, and linetype
        fixedline, linetype = formatdata(line,field)
        # check if a new linetype, if so, save it to hash
        if not linetype in hashtype:
            hashtype[linetype] = []
        hashtype[linetype].append(list( fixedline) )
    return (hashtype)

def loadfiledata(filename,field):
# read data in from filename
# return an array of arrays

    hashtype= {}
    #for line in open(filename,'r'):
    for line in filename:
        # load line data get back formatted line, and line type
        fixedline, linetype = formatdata(line,field)
        # check if a new line type, if so, save it to hash
        if not linetype in hashtype:
            hashtype[linetype] = []
        hashtype[linetype].append(list( fixedline) )
    return (hashtype)

def rowtype(hashdata):
# print all row types and have user select header and data lines
    print('\nRow types found in data\n\n')
    count = 0
    arraytype = []
    for key in hashdata:
        arraytype.append(key)
        print('Line: %s' % count)
        print (str(hashdata[key][0]) + '\n')
        count += 1

    # need this to get user data from shell if data was piped
    sys.stdin = open('/dev/tty')

    # get user input and verify it's valid
    headerrow = ''
    datarow = ''
    while 1:
        headerrow = raw_input('\nSelect line number of header row: ')
        try:
            if int(headerrow) in range(len(arraytype)):
                break 
        except:
            print('Invalid Line')
    while 1:
        datarow = raw_input('\nSelect line number of data row: ')
        try: 
            if int(datarow) in range(len(arraytype)):
                break 
        except:
            print('Invalid Line')
    return( arraytype[int(headerrow)], arraytype[int(datarow)] )
    

def graphlabels(hasheddata,headerkey):
# select x and y fields from header line
    print ('\nFields from selected header row\n')
    arraytype = []
    count = 0
    for item in hasheddata[headerkey][0]:
        print ('Field: %s: %s' % (count,item) )
        arraytype.append(item)
        count += 1
    print ('Field: %s: Interval: each line is a new data sample' % (count) )
    arraytype.append('None')

    # need this to get user data from shell if data was piped
    sys.stdin = open('/dev/tty')

    # get user input and verify it's valid
    x = ''
    y = ''
    xlist = []
    ynolist = []
    while 1:
        x = raw_input('\nSelect x axis. (ie: Date, or Interval): ')
        try:
            if int(x) in range(len(arraytype)):
                break 
        except:
            print('Invalid Line')

    xlist.append(x)

    while 1:
        x = raw_input('\nSelect multi-item x axis field # (ie: mpstat: CPU) or n/N for none: ')
        try:
            if (x.lower() == 'n' or int(x) in range(len(arraytype))  ):
                break 
        except:
            print('Invalid Line')

    xlist.append(x)

    y = raw_input('\nSelect y axis numbers NOT to graph seperated by a space: %s ' % (xlist) )
    ynolist = xlist + y.split()

    return(xlist,ynolist)

def selectdata(position,data,multix):
# return a list of desired data
# data: is a list of list
    wanteddata = {}
    
    if multix.lower() == 'n':
        wanteddata['Interval'] = []
        for item in range(len(data)):
            wanteddata['Interval'].append(data[item][int(position)])
    else:
        for item in range(len(data)):
            if not data[item][int(multix)] in wanteddata: wanteddata[data[item][int(multix)] ] = []
            wanteddata[data[item][int(multix)] ].append(data[item][int(position)])

    return wanteddata

def graphit(xlist,y, header, data, datestring, dateformat, longlabels = {}):
# data: list of list of data
# header: list of headers
# x: str of number of x position in header, and data
# y: str of number of y position in header, and data
    x = int(xlist[0])
    y = int(y)
    lhead='Legend'

    if header[y] in longlabels:
        graphtitle = longlabels[header[y]]
    else:
        graphtitle = header[y]

    xdata = {}
    ydata = selectdata(y,data,xlist[1])

    #fig = plt.figure(dpi=200 )
    fig, ax = plt.subplots(1,dpi=200)

    # If x axis is 'None' then make x values a list 0 to length of ydata
    if x == len(header):
        xdata['Interval'] = range(len(ydata[ydata.keys()[0] ] ))
        plt.xlabel('Per Data Point' )
        plt.title('%s' % (graphtitle) )

    else:
        plt.xlabel('Time')
        plt.title('Time vs %s' % (graphtitle) )
        unf_dates = selectdata(x,data,xlist[1])
        date_obj = {}
        xdata = {}
        for item in unf_dates:
            date_obj[item] = [datetime.datetime.strptime(str(i), datestring) for i in unf_dates[item] ]
            xdata[item] = [mdates.date2num(i) for i in date_obj[item] ]

    if not xlist[1].lower() == 'n':
        lhead=header[int(xlist[1])]

    plt.ylabel(header[y])

    if x == len(header):
        for item in ydata:
            if len(ydata) == 1:
                plt.fill_between(xdata['Interval'], ydata[item],label=item,alpha=0.5)
            else:
                plt.plot(xdata['Interval'],ydata[item],label=item,marker=None,linestyle='-')
    else:
        mdates.DateFormatter(datestring)
        for item in ydata:
            if len(ydata) == 1:
                plt.fill_between(xdata[item],ydata[item],label=item,alpha=0.5)
            else:
                plt.plot_date(xdata[item],ydata[item],label=item,marker=None,linestyle='-')
        ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformat) )
        fig.autofmt_xdate()
    plt.legend(title=lhead,fontsize=4)
    plt.grid(True)

    return fig

def transpose(hasheddata, datakey,headerkey):
    arraytype = []
    count = 0
    for item in hasheddata[datakey][0]:
        print ('Field: %s: %s' % (count,item) )
        arraytype.append(item)
        count += 1

    # may need this to get user data from shell if data was piped
    sys.stdin = open('/dev/tty')
    field = ''
    newheader = {}
    transposeddata = {}
    transposeddata[datakey] = []
    newdata = {}

    while 1:
        field = raw_input('\nSelect field to be new header line in transposed data: ')
        try:
            if int(field) in range(len(arraytype)):
                break 
        except:
            print('Invalid Line')

    newheader = selectdata(field,hasheddata[datakey],'n')

    # counter used as 0 to lenght of current data line
    multirowlen = len(hasheddata[datakey][0])
    rowmultiplier = 0
    # counter used as 0 to length of new header
    multisetlen = 0
    setmultiplier = 0
    # length of new header
    countset = len(set(newheader['Interval']))

    # transpose data based on inital row length and 
    # the number of different items in the set of selected field
    for row in range(len(hasheddata[datakey])):

        multisetlen += 1

        for position in range(len(hasheddata[datakey][row])):
            if (position + rowmultiplier) == len(transposeddata[datakey]):
                transposeddata[datakey].append([])
                transposeddata[datakey][position + rowmultiplier].append(hasheddata[headerkey][0][position])
            transposeddata[datakey][position + rowmultiplier].append(hasheddata[datakey][row][position])

        if multisetlen == countset:
            multisetlen = 0
            rowmultiplier += multirowlen

    transposeddata[headerkey] = []
    transposeddata[headerkey].append(newheader['Interval'][:countset])

    for key in transposeddata:
        for item in transposeddata[key]:
            fixedline,linetype = formatdata(' '.join(map (str,item)) )
            if not linetype in newdata:
                newdata[linetype] = []
            newdata[linetype].append(list(fixedline) )
    #print newdata

    return newdata

def detailedlabels(labelfile,header):

    # load data from labefile
    # file format "OS:datatype:header:long header
    longlabels = {}

    for line in labelfile:
        linelist = line.split(':')

        if not linelist[0] in longlabels:
            longlabels[linelist[0]] = {}
        if not linelist[1] in longlabels[linelist[0]]:
            longlabels[linelist[0]][linelist[1]] = {}
        if not linelist[2] in longlabels[linelist[0]][linelist[1]]:
            longlabels[linelist[0]][linelist[1]][linelist[2]] = linelist[3]
    
    for OS in longlabels:
        print OS
    os = ''
    while 1:
        os = raw_input('\nSelect OS type: ')

        if os in longlabels:
            break
        else:
            print('Invalid selection')

    datatype = ''
    for command in longlabels[os]:
        print command

    while 1:
        datatype = raw_input('\nSelect OS type: ')

        if datatype in longlabels[os]:
            break
        else:
            print('Invalid selection')

    return longlabels[os][datatype]

def checkcusty(listitems,headers):
# check users custom y string to see if it's valid
# list items is a list of users advanced y function
# headers is a list of headers
    for item in listitems[::2]:
        if isnumber(item) or item in headers[0]:
            pass
        else:
            return False

    for item in listitems[1::2]:
        if item not in ['-','+','/','*']:
            return False

    return True

def getcusty(headers):
# get users customer y string
    custy = ''
    print('\nCustom Y option selected')
    print('Supported inputs are, -, +, *, /, numbers, and header strings') 
    for item in headers[0]:
        print item

    while 1:
        custy = raw_input('Enter Y function: ')
        if checkcusty(custy.split(),headers):
            break
        else:
            print('Invalid entry')

    return custy.split()

def customydata(custy,hasheddata,datakey,headerkey):
# expand custy list as a list of list
# if not in header then * by len of ydata
# if in header, put list of ydata
# feed each line through mathfunc
# return data
    pass

def mathfunc(total,mathsymbol,datapoint):
    if mathsymbol == '-':
        return total - float(datapoint)
    elif mathsymbol == '+':
        return total + float(datapoint)
    elif mathsymbol == '/':
        return total / float(datapoint)
    elif mathsymbol == '*':
        return total * float(datapoint)


##########################
# Main
#########################
def main():

    args = getargs()

    # set dateformat to datestring if no dateformat entered
    if args.dateformat == None:
        args.dateformat = args.datestring

    # Check and force pdf file extension
    if args.outfile.split('.')[-1] != 'pdf':
        loglevel(args,'Adding pdf extension. New file is %s.pdf' % (args.outfile),'debug')
        args.outfile = args.outfile + '.pdf'

    pdfdoc = PdfPages(args.outfile)
    mygraph = ''

    # Load data
    if args.infile:
        # load data from file option infile
        loglevel(args,'Reading data from file: %s' % args.infile,'debug')
        hasheddata = loadfiledata(args.infile,args.field)
    # if there is data from stdin
    elif not sys.stdin.isatty():
        # read in data and linetypes from shell
        loglevel(args,'Reading data from shell stdin','debug')
        hasheddata = piperead(args.field)
    else:
        loglevel(args,'Error....: no data found from input file or the shells stdin','normal')
        sys.exit()

    # select header and data rows
    headerkey, datakey = rowtype(hasheddata)


    # Call Detailed label function
    longlabels = {}
    if args.labelfile:
        longlabels =  detailedlabels(args.labelfile,hasheddata[headerkey][0])

    # transpose data
    if args.transpose:
        loglevel(args,'Transposing data','normal')
        hasheddata = transpose(hasheddata,datakey,headerkey)

        loglevel(args,'Reselect new header and data rows','normal')
        headerkey, datakey = rowtype(hasheddata)

    # select x column to graph and the y list of values not to graph
    xlist,ynolist = graphlabels(hasheddata,headerkey)

    # check if time date string is needed (non-interval x selection)
    if int(xlist[0]) != len(hasheddata[headerkey][0]):
        print('\nDate String Needed')
        print('Example: %H:%M:%S : HH:MM:SS')
        print('%Y: YYYY, %y: YY, %m: MM, %d: DD, %H: HH, %M: MM, %S: SS')
        datefmt = raw_input('Enter date string (Default: %s) : ' % args.datestring)

        if datefmt != '':
            args.datestring = datemft

    if args.customy:
        customy = getcusty(hasheddata[headerkey])
        print customy


    # create graphs
    for y in range(len(hasheddata[headerkey][0]) ):
        # if item is not in our ynolist then make a graph of it
        if  str(y) not in ynolist:
            # if y data is a digit, then graph it
            if isnumber(hasheddata[datakey][0][y]):
                try:
                    plt.close(mygraph)
                    loglevel(args,'Attempting to created graph of %s'  % (hasheddata[headerkey][0][y]),'debug')
                    mygraph = graphit(xlist,y,hasheddata[headerkey][0],hasheddata[datakey],args.datestring, args.dateformat,longlabels) 
        #mygraph.savefig('graph.png',format='png', dpi = 200)
                    pdfdoc.savefig(mygraph)
                    loglevel(args,'Created graph of %s'  % (hasheddata[headerkey][0][y]),'debug')
                except Exception as e:
                    print e
                    loglevel(args,'Error...: Unable to plot %s' % (hasheddata[headerkey][0][int(y)] ),'normal' )
                    loglevel(args,'X values are: %s' % (xlist),'debug')

            #pdfdoc.savefig(mygraph)
    #mygraph.savefig(pdf,format='pdf', dpi = 200)
    #mygraph.close()
    loglevel(args,'Saving %s' % args.outfile,'normal')
    pdfdoc.close()

###############################################################
if __name__ == '__main__':
    import sys
    import argparse
    import datetime
    import matplotlib
    # Tell matplotlib not to use XWindow display
    matplotlib.use('Agg')

    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    main()

