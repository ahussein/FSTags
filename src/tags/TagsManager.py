'''
Created on Mar 26, 2011

@author: abdelrahman
'''

from storage.StorageManager import StorageManager
import MetadataHelper
from ConfigParser import ConfigParser
import os


class TagsManager(object):
    """
    The main class that manage the tags on directory and files
    """
    
    def __init__(self):
        """
        Initialize the TagsManager
        """
        self._storage = StorageManager()
        
    
    def add_tags(self, path, tags):
        """
        Adds a set of tags to a folder/file path
        
        @param path: the full folder/file path that the tags will be applied to. If a folder is given, the tags will be applied to all the child files
        @param tags: comma separated list of tags
        """
        tags_list = tags.split(',')
        for tag in tags_list:
            self._storage.put(tag.strip(), path)
        #add metadata for the path. to be used in show tags and in the plugin manager
        if os.path.isdir(path):
            #currently we tag only all the files under a folder no sub-folder taging is supported, this is noly for plugin processing and tags viewing , for searching full dir structure is supported
            config_parser = ConfigParser()
            metadata_path = os.path.join(path, '.fstagsmeta')
            if not os.path.exists(metadata_path):
                config_parser.add_section('main')
                config_parser.set('main', 'tags', tags)
            else:
                config_parser.read(metadata_path)
                config_parser.set('main', 'tags', '%s, %s'%(config_parser.get('main', 'tags'), tags))
            with open(metadata_path, 'wb') as config_file:
                config_parser.write(config_file)
        else:
            self.__add_tags_to_file(path, tags)
    

    def __add_tags_to_file(self, path, tags):
        """
        Adds tags to the metadata file
        """
        config_parser = ConfigParser()
        metadata_path = os.path.join(os.path.dirname(path), '.fstagsmeta')
        if not os.path.exists(metadata_path):
            config_parser.add_section('main')
            config_parser.set('main', 'tags', '')
            config_parser.add_section(path)
            config_parser.set(path, 'tags', tags)
            with open(metadata_path, 'wb') as config_file:
                config_parser.write(config_file)
        else:
            config_parser.read(metadata_path)
            if path in config_parser.sections():
                config_parser.set(path, 'tags', '%s, %s'%(config_parser.get(path, 'tags'), tags))
            else:
                config_parser.add_section(path)
                config_parser.set(path, 'tags', tags)
            with open(metadata_path, 'wb') as config_file:
                config_parser.write(config_file)
    
    def spcialtags(self, path, threshold = 10):
        """
        """
        for item in filter(lambda item: os.path.isfile(os.path.join(path, item)), os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.getsize(item_path)/1024/1024 > 10:
                self.add_tags(item_path, 'big')
            else:
                self.add_tags(item_path, 'small')
                
            
    
    def remove_tags(self, path, tags):
        """
        Removes a set of tags from a folder/file path
        
        @param path: the full folder/file path that the tags will be removed from. If a folder is given, the tags will be removed from all the child files
        @param tags: comma separated list of tags
        """
        tags_list = tags.split(',')
        for tag in tags_list:
            self._storage.remove_one(tag.strip(), path)
    
    
    def show_tags(self, path):
        """
        Prints a list of tags applied to a folder/file path
        
        @param path: the full folder/file path
        """
        print MetadataHelper.get_tags(path)
    
    
    def find(self, tags, match_all = True):
        """
        Retrieve a list of folder/file paths that match a specific set of tags
        
        @param tags: comma separated list of tags
        @param match_all:  if True then all the tags must be applied to the folder/file to match, otherwise any of the tags applied to the folder/file then it will match
        """
        result = list()
        tags_list = tags.split(',')
        for tag in tags_list:
            ret = self._storage.get(tag.strip())
            if match_all:
                result = self.__intersection(result, ret) if result else ret
#                result = list(set(ret).intersection(set(result) if result else set(ret)))
            else:
                result.extend(ret)
        return list(set(result))
    
    def __intersection(self, first_list, second_list):
        """
        Finds the intersection between tow lists and take into account the parent/child relation between folder/folder/file relation
        
        @param first_lsit: first list
        @param second_list: second list
        """
        result_list = list()
        for item in first_list:
            skip = False
            for seconditem in second_list:
                if item in seconditem:
                    result_list.append(seconditem)
                    skip = True
            if skip:
                continue
            if item in second_list:
                result_list.append(item)
        return result_list