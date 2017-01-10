# Plotting Applet
#####WIP python based plotting application
Its a mess right now...the markdown is more nice than the actual thing itself at this point.

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
- more complete fakeSerial module, right now it's pretty basic.

#Dependencies: <sup>[3]</sup> 
- [>= Python 3.5 (x_64)][py] (Started in 3.5.1, then realised 6 had Come out :\ ) 
- [PyQtGraph][pyqtg]
   - [numpy][np] <sup>[2]</sup>
   - [PyQt4][pyqt] <sup>[1]</sup><sup>[2]</sup>
- [PySerial][ser]
- [PyDAQmx][DAQ]

At this point it does startup but seeing as its still broken...that doesn't mean much.

---
[1] Being built with PyQt4, so its recommended, I haven't tested with any other PyQt bindings.

[2] For Windows Users I would recommend getting most of your packages as [precompiled wheels][whls]

[3] This was and is being primarily developed on Windows 7 and 10 with limited Linux testing being done. Take that as you will.

[py]:https://www.python.org/ "Python main page" 
[pyqtg]:http://www.pyqtgraph.org/ "Official Documentation"
[np]: http://www.numpy.org/ "Official Documentation"
[pyqt]: https://www.riverbankcomputing.com/software/pyqt/download "Official Page"
[ser]: https://pythonhosted.org/pyserial/ "Official Documentation"
[DAQ]:https://pythonhosted.org/PyDAQmx/ "Official Documentation"
[whls]: http://www.lfd.uci.edu/~gohlke/pythonlibs/
