# Plotting Applet
####WIP python based plotting application
...its a mess right now...

Not even close to done.. and i've broken it again.... so yeah...

## Main things:
Designed for ease of use amongst the non-programmers out there, the main focus was developing
 the gui side of the world, and then moving on from there. 

Supposed to end up as an application where you can stream and/or log:
- Serial Data
- NI DAQ based devices
- eventual more flexible packet payloads than either of those

### Other things:
Will end up with some basic signal processing functionality and statistics figures as well:
- Discrete FFT
- Boxcar Averaging
- FIR filters
- Z-transform
- general statistics for data sets
- etc.

### Extras if time allows:
- tool(s) for separate data importation, overlay, processing, etc.

#Dependencies: 
- [>= Python 3.5 (x_64)](https://www.python.org/ "Python main page") (Started in 3.5.1, then realised 6 had Come out :\ ) 
- [PyQtGraph](http://www.pyqtgraph.org/ "Official Documentation")
   - [numpy](http://www.numpy.org/ "Official Documentation")
   - [PyQt4](https://www.riverbankcomputing.com/software/pyqt/download "Official Page")
- [PySerial](https://pythonhosted.org/pyserial/ "Official Documentation")
- [PyDAQmx](https://pythonhosted.org/PyDAQmx/ "Official Documentation")

Note: For Windows Users I would recommend getting most of your packages as [precompiled wheels](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

**Side Note: This was and is being primarily developed on Windows 7 and 10 with limited Linux testing being done. Take that as you will.**

At this point it does startup but seeing as its still broken...that doesn't mean much.