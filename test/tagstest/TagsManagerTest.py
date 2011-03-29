'''
Created on Mar 29, 2011

@author: abdelrahman
'''
import time
import unittest
import os
from tags.TagsManager import TagsManager

class TagsManagerTest(unittest.TestCase):
    
    
    def setUp(self):
        self.tags_manager = TagsManager()
        dir_prefix = '_%s'%time.time()
        self.test_dir = os.path.join(os.path.dirname(___file__), 'test_%s'%dir_prefix)
        os.mkdir(self.test_dir)
        
    def tearDown(self):
        os.rmdir(self.test_dir)
        del self.tags_manager
    
    def test_simple_add_tags(self):
        tags = 'testing_%s'%time.time()
        self.tags_manager.add_tags(self.test_dir, tags)
        self.assertTrue(self.test_dir in self.tags_manager.find(tags))
        self.tags_manager.remove_tags(self.test_dir, tags)
        
    
    def test_simple_remove_tags(self):
        tags = 'testing_%s'%time.time()
        self.tags_manager.add_tags(self.test_dir, tags)
        self.tags_manager.remove_tags(self.test_dir, tags)
        self.assertTrue(self.test_dir not in self.tags_manager.find(tags))
        
    
    def test_simple_find(self):
        tags = 'testing_%s'%time.time()
        self.assertTrue(not self.tags_manager.find(tags))
        self.tags_manager.add_tags(self.test_dir, tags)
        self.assertTrue(self.test_dir in self.tags_manager.find(tags))