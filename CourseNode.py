"""
CourseNode
~~~~~~~~~~

A library for creating nodes for a linked list of classes.
Each node contains the name of the course, the start time, 
the duration, the end time, the location, the previous node, 
the next node, and the reminder time.

Duration is calculated at runtime by subtracting the start and end times.

The prev_node and next_node will be added by a function in the linked list class.
"""
from datetime import datetime, timedelta
from typing import Any

class CourseNode():
    def __init__(self, node_title:str, start_time:datetime, day:str, end_time:datetime, location:str, prev_node=None, next_node=None, reminder:int=0):
        self.node_title = node_title
        self.start_time = start_time
        self.end_time = end_time
        # Calculate duration at runtime
        self.duration = (end_time - start_time).minutes
        # TODO: Use Google Places API to get a google maps link to the location if found, else use the location string
        self.location = location
        self.prev_node = prev_node
        self.next_node = next_node
        self.reminder = reminder
        self.day = day
    
    def __repr__(self):
        return f"{self.node_title} from {self.start_time} to {self.end_time} at {self.location} every {self.day}"
    
    # Getter and Setter methods for each attribute
    def get_node_title(self):
        return self.node_title
    
    def set_node_title(self, node_title):
        self.node_title = node_title
        
    def get_start_time(self):
        return self.start_time
    
    def set_start_time(self, start_time):
        self.start_time = start_time
        self.duration = (self.end_time - start_time).minutes
        
    def get_end_time(self):
        return self.end_time
    
    def set_end_time(self, end_time):
        self.end_time = end_time
        self.duration = (end_time - self.start_time).minutes
    
    # Duration is calculated at runtime, so no setter method    
    def get_duration(self):
        return self.duration
    
    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
        
    def get_prev_node(self):
        return self.prev_node
    
    def set_prev_node(self, prev_node):
        self.prev_node = prev_node
        
    def get_next_node(self):
        return self.next_node
    
    def set_next_node(self, next_node):
        self.next_node = next_node
        
    def get_reminder(self):
        return self.reminder
    
    def set_reminder(self, reminder):
        self.reminder = reminder
        