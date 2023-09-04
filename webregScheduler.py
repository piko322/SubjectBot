"""
CourseScheduler
~~~~~~~~~~~~~~~
This module contains the CourseNode class representing a "block" in a weekly schedule,
and a CourseSchedule class representing a doubly linked list of CourseNode objects.
"""

from datetime import datetime, timedelta
from typing import Any

class CourseNode:
    """Node representing a class "block" in a weekly schedule.
    
    Attributes:
        node_title: The title of the course, which is a concatenation of the subject course and type
        day: The day of the week the course is on
        start_time: The start time of the course
        end_time: The end time of the course
        duration: The duration of the course in minutes
        location: The location of the course
        prev_node: The previous node in the linked list
        next_node: The next node in the linked list
        reminder: The number of minutes before the start time of the course to send a reminder  (default 0)
    """
    
    def __init__(self, node_title:str=None, day:str=None,  start_time=-1, end_time=-1, \
                    location:str=None, prev_node=None, next_node=None, reminder:int=0):
        self.node_title = node_title
        if start_time == -1 and end_time == -1:
            self.start_time = -1
            self.end_time = -1
        else:
            # Calculate duration at runtime
            # Convert start_time and end_time to datetime objects
            self.start_time = datetime.strptime(start_time, "%I:%M%p")
            self.end_time = datetime.strptime(end_time, "%I:%M%p")
            self.duration = int((self.end_time - self.start_time).total_seconds() / 60)
        # TODO: Use Google Places API to get a google maps link to the location if found, else use the location string
        self.location = location
        self.prev_node = prev_node
        self.next_node = next_node
        self.reminder = reminder
        self.day = day
    
    def __str__(self):
        return self.node_title
    
    def __repr__(self):
        dayDict = {"M":"Monday", "Tu":"Tuesday", "W":"Wednesday", "Th":"Thursday", "F":"Friday", "Sa":"Saturday", "Su":"Sunday"}
        if self.start_time == -1 or self.end_time == -1:
            return f"Sentinel Node on {dayDict[self.day]}"
        start_time = self.start_time.strftime("%I:%M%p")
        end_time = self.end_time.strftime("%I:%M%p")
        return f"{self.node_title} from {start_time} to {end_time} at {self.location} on {dayDict[self.day]}, lasting {self.duration} minutes"
    
    # Getter and Setter methods for each attribute
    def get_node_title(self):
        return self.node_title
    
    def set_node_title(self, node_title):
        self.node_title = node_title
        
    def get_start_time(self):
        return self.start_time
    
    def set_start_time(self, start_time:datetime):
        self.start_time = start_time
        self.duration = (self.end_time - start_time).total_seconds() / 60

    def get_end_time(self):
        return self.end_time
    
    def set_end_time(self, end_time:datetime):
        self.end_time = end_time
        self.duration = (end_time - self.start_time).total_seconds() / 60
    
    # Duration is calculated at runtime, so no setter method    
    def get_duration(self):
        return self.duration
    
    def get_location(self):
        return self.location
    
    def set_location(self, location):
        self.location = location
        
    def get_prev(self):
        return self.prev_node
    
    def set_prev(self, prev_node):
        self.prev_node = prev_node
        
    def get_next(self):
        return self.next_node
    
    def set_next(self, next_node):
        self.next_node = next_node
        
    def get_reminder(self):
        return self.reminder
    
    def set_reminder(self, reminder):
        self.reminder = reminder
        
    # Comparison methods to compare the start times of two CourseNode objects.
    # If the days are different, raise a ValueError: "Cannot compare two CourseNode objects with different days"
    # If the start times are the same, compare the end times instead
    # If the end times are also the same, compare the node titles
    def __gt__(self, other):
        if self.day != other.day:
            raise ValueError("Cannot compare two CourseNode objects with different days")
        if self.start_time == other.start_time:
            if self.end_time == other.end_time:
                return self.node_title > other.node_title
            return self.end_time > other.end_time
        return self.start_time > other.start_time
    
    def __lt__(self, other):
        if self.day != other.day:
            raise ValueError("Cannot compare two CourseNode objects with different days")
        if self.start_time == other.start_time:
            if self.end_time == other.end_time:
                return self.node_title < other.node_title
            return self.end_time < other.end_time
        return self.start_time < other.start_time
    # If two nodes have the same day, start time, end time, and node title, they are the same node
    def __eq__(self, other): 
        if self.day == other.day:
            if (self.start_time == other.start_time) and (self.end_time == other.end_time):
                if self.node_title == other.node_title:
                    return True
        return False

class ScheduleIterator:
    def __init__(self, head):
        self.curr_node = head.next_node
    
    def __next__(self):
        # If the current node is the tail node, stop iteration
        if self.curr_node.get_start_time() == -1 or self.curr_node.get_end_time() == -1:
            raise StopIteration
        else:
            curr_node = self.curr_node
            self.curr_node = self.curr_node.get_next()
            return curr_node
        
    def __iter__(self):
        return self

class DaySchedule:
    """Doubly linked list of CourseNode objects representing a schedule for a single day.
    Attributes:
        head: The head node of the linked list
        tail: The tail node of the linked list
        size: The number of nodes in the linked list
        length: The total length of the schedule in minutes
    """
    def __init__(self, day:str=None):
        if day not in ["M", "Tu", "W", "Th", "F", "Sa", "Su"]:
            raise ValueError("Invalid day of the week: must be one of M, Tu, W, Th, F, Sa, Su")
        self.day = day
        # Set sentinel nodes for head and tail
        self.head = CourseNode(day=day)
        self.tail = CourseNode(day=day)
        self.size = 0
        self.length = 0
    
    def __iter__(self):
        return ScheduleIterator(self.head)
    
    def insert(self, new_node:CourseNode):
        if self.size == 0:
            self.head.next_node = new_node
            new_node.prev_node = self.head
            new_node.next_node = self.tail
            self.tail.prev_node = new_node
        else:
            curr_node = self.head.next_node
            # Iterate through the linked list until a class with a later start time is found
            while new_node > curr_node:
                curr_node = curr_node.next_node
                # If the end of the linked list is reached, insert the node at the end
                if curr_node == self.tail:
                    break
            # Update the new node
            new_node.next_node = curr_node
            new_node.prev_node = curr_node.prev_node
            # Update the node before the new node
            curr_node.prev_node.next_node = new_node
            # Update the node after the new node
            curr_node.prev_node = new_node
            
        self.size += 1
        self.length += new_node.duration
    
    def __repr__(self):
        curr_node = self.head.next_node
        schedule = f"{self.day} Schedule: "
        while curr_node != self.tail:
            schedule += curr_node.get_node_title() + ", "
            curr_node = curr_node.next_node
        return schedule[:-2]

    
    
    