#!/usr/bin/python2.6
import pkg_resources
pkg_resources.require("TurboGears")

from turbogears import update_config, start_server, config
import cherrypy
cherrypy.lowercase_api = True
from os.path import *
import sys
sys.path.append('../')
from components import db




# first look on the command line for a desired config file,
# if it's not on the command line, then
# look for setup.py in this directory. If it's not there, this script is
# probably installed
if len(sys.argv) > 1:
    update_config(configfile=sys.argv[1], 
        modulename="infoshopkeeperonline.config")
elif exists(join(dirname(__file__), "setup.py")):
    update_config(configfile="dev.cfg",modulename="infoshopkeeperonline.config")
else:
    update_config(configfile="prod.cfg",modulename="infoshopkeeperonline.config")

config.update({'sqlobject.dburi':db.conn()})


from infoshopkeeperonline.controllers import Root

start_server(Root())
