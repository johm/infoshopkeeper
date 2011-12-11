# Copyright 2007 Guillaume Beaulieu

# This file is part of Infoshopkeeper.

# Infoshopkeeper is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or any later version.

# Infoshopkeeper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Infoshopkeeper; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

import sys
    
try:
    from mx.DateTime import *
except:
    print "mxdatetime does not seem installed"
    print " on debian you need to apt-get install python-egenix-mxdatetime"
    sys.exit(0)

try:
    from sqlobject import *
except:
    print "sqlobject does not seem installed"
    print " on debian you need to apt-get install python-sqlobject"
    sys.exit(0)
try:
    from wx import *
except:
    pass
#    print "wxWindows does not seem installed"
#    print " on debian you need to apt-get install wx-common python-wxgtk2.6"
# since we have non-gui uses now with different python version
#    sys.exit(0)


class configuration:
    def get(self, var):
        import etc_default
        import etc
	if var in dir(etc):
	    return getattr(etc, var)
	elif var in dir(etc_default):
	    return getattr(etc_default, var)
	else:
	    self.fatal(var)
    
    def fatal(self, var):
    	print "FATAL CONFIGURATION ERROR !"
	print "Unable to reach configuration value " + var + "\n"
	print "     (did you modify the config before using ? did you used an"
	print "                                                   obsolete config file ?)"
	print "\n\n\n"
	exit

a = configuration()

if a.get("dbtype") == 'mysql':
    try:
        import MySQLdb as dbmodule
    except:
        print "python mysqldb does not seem installed, and you specified your database is of type mysql"
        print " on debian you need to apt-get install python-mysqldb"
	sys.exit(0)

