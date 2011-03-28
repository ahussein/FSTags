'''
Created on Mar 27, 2011

@author: abdelrahman
'''

from ConfigParser import ConfigParser
import time
import os, sys
from threading import Thread
PLUGINS_CFG = '/etc/fsplugins.cfg'

class PluginsManager(object):
    """
    Handle different plugins to the FSTags system
    """
    
    def __init__(self, plugins_cfg_file = PLUGINS_CFG):
        self.__config_parser = ConfigParser()
        self.__config_parser.read(plugins_cfg_file)
        self.__plugins_dir = self.__config_parser.get('main', 'plugins_dir')
        self.__interval = self.__config_parser.getint('main', 'interval')
        self.__plugins = dict()
        sys.path.append(self.__plugins_dir)
    
    def reload_plugins(self):
        """
        loads the plugins from the plugins directory 
        """
        for item in os.listdir(self.__plugins_dir):
            plugin_dir = os.path.join(self.__plugins_dir, item)
            if not os.path.isdir(plugin_dir):
                continue
            if not os.path.exists(os.path.join(plugin_dir, '__init__.py')):
                print 'path %s not a valid python package, plugins needs to be valid packages. Skipping plugin..'%plugin_dir
                continue
            if item not in self.__plugins.keys():
                self.__plugins[item] = plugin_dir
                
        
    
    def start(self):
        """
        Start the manager 
        """
        while True:
            self.reload_plugins()
            for plugin, plugin_dir in self.__plugins.iteritems():
                eval('from %s import %s'%(plugin, 'main'))
                t = Thread(target = main.execute, args = [plugin_dir])
                t.setDaemon(1)
                t.start()
            #do stuff
            time.sleep(self.__interval)