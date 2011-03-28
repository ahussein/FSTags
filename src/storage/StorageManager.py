'''
Created on Mar 26, 2011

@author: abdelrahman
'''
    
from ConfigParser import ConfigParser
import lightcloud
class LightCloudManager(object):
    """
    A wrapper for lightcloud key/value store that implement the storage interface
    """
    CONFIG_FILE_PATH = '/etc/lightcloud.cfg'
    
    def __init__(self):
        self.config = dict()
        self._lookup_nodes = list()
        self._storage_nodes = list()
        
    def initialize(self, config_file_path = CONFIG_FILE_PATH):
        """
        Initializes the lightcloud storage manager, load the configuration and creates the nodes
        
        @param config_file_path: path to the configuration file, which is formatted as INI file
        """
        self.load_config(config_file_path)
        self._lookup_nodes, self._storage_nodes = lightcloud.generate_nodes(self.config)
        lightcloud.init(self._lookup_nodes, self._storage_nodes)
        
    
    def load_config(self, config_file_path = CONFIG_FILE_PATH):
        """
        Loads the configuration of the lightcloud storage server(server ips/ports) and connect to the server
        
        @param config_file_path: path to the configuration file, which is formatted as INI file
        """
        config_parser = ConfigParser()
        config_parser.read(config_file_path) 
        for section in config_parser.sections():
            self.config[section] = list()
            server_string = '%s:%s'%(config_parser.get(section, 'server'), config_parser.get(section, 'port'))
            self.config[section].append(server_string)
                
    
    def put(self, key, value):
        """
        Put a key/value pairs into the lightcloud storage backend
        
        @return: True if the item put successfully, False otherwise
        """
        #first try to get the the list of items stored for this key if any, then add the new value to the list otherwise add the new key/value to the store
        return lightcloud.list_add(key, [value]) == 'ok'
            
    
    def get(self, key):
        """
        Retrieves the value of a key from the lightcloud store
        
        @param key: the key to retrieve
        
        @return: list of the value(s) if exist,  empty list otherwise
        """
        #try to retrieve a list of the values, if the key doesnt exist in the list keys then try to get it from the normal keys
        result = lightcloud.list_get(key)
        if isinstance(result, list):
            return result
        result = lightcloud.get(key)
        if result:
            return [result]
        return list()
            
            
    def remove(self, key):
        """
        Removes a key and its value from the lightcloud store
        
        @param key: the key of the value to remove
        
        @return: True if the key/value removed successfully, False otherwise
        """
        return lightcloud.delete(key)
    
    
    def remove_one(self, key, value):
        """
        Removes one of the value from the values list of a key
        
        @param key: a key in the store
        @param value: value to remove from the values list
        
        @return: True if the key/value removed successfully, False otherwise
        """
        return lightcloud.list_remove(key, value) == 'ok'
        
    

class StorageManager(object):
    """
    Generic key/value store interface
    """
    SUPPORTED_STORES = {'LIGHTCLOUD': LightCloudManager,}
    def __init__(self, storagetype = 'LIGHTCLOUD'):
        """
        Initialize storage manager based on the storage type provided, if none provided then it uses lightcloud as storage backend
        """
        if storagetype not in self.SUPPORTED_STORES:
            raise ValueError('Unsupported storage type %s, the current supported storage types are %'%(storagetype, self.SUPPORTED_STORES.keys()))
        self.manager = self.SUPPORTED_STORES[storagetype]()
        self.manager.initialize()
    
    def put(self, key, value):
        """
        Put a pair of key/value into the backend store
        
        @param key: the key of the object to store, currently we only support string keys
        @param value:  the value of the object to store, currently we only support string values
        
        @return: True if the operation completed successfully, False otherwise 
        """
        return self.manager.put(key, value)
        
    
    def get(self, key):
        """
        Retrieve a value from the backend store that match the requested key, None if the key doesnt exist
        
        @param key: the key of the value to retrieve
        
        @return: list of the value(s) if exist,  empty list otherwise
        """
        return self.manager.get(key)
    
    def remove(self, key):
        """
        Removes a key and its value from the backend store
        
        @param key: the key of the value to remove
        
        @return: True if the key/value removed successfully, False otherwise
        """
        return self.manager.remove(key)
    
    
    def remove_one(self, key, value):
        """
        Removes one of the value from the values list of a key
        
        @param key: a key in the store
        @param value: value to remove from the values list
        
        @return: True if the key/value removed successfully, False otherwise
        """
        return self.manager.remove_one(key, value)