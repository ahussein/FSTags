'''
Created on Mar 28, 2011

@author: abdelrahman
'''

import os
from ConfigParser import ConfigParser
def get_tags(path):
    """
    Retreive a list of tags that are applied to a path
    
    @param path: path to a file/folder in the filesystem
    
    @return: list of tags applied to specific path
    """
    config_parser = ConfigParser()
    dir_tags = __get_dir_tags(path if os.path.isdir(path) else os.path.dirname(path), config_parser)
    if os.path.isdir(path):
        return dir_tags
    metadata_filepth = os.path.join(os.path.dirname(path), '.fstagsmeta')
    config_parser.read(open(metadata_filepth))
    return list(set([item.strip() for item in ('%s, %s'%(dir_tags, config_parser.get(path, 'tags'))).split(',')]))


def __get_dir_tags(path, config_parser):
    metadata_filepth = os.path.join(path, '.fstagsmeta')
    if not os.path.exists(metadata_filepth):
        raise ValueError('Metadata file %s not found in the system.'%path)
    config_parser.read(metadata_filepth)
    return config_parser.get('main', 'tags')
        
        
    
