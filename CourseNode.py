"""
CourseNode
~~~~~~~~~~

A library for creating a noded for a linked list of courses in a day.
Contains start time, duration, course name, location, next_node, prev_node, and a changeable variable
for how long to remind the user before this specific class starts.

Calculates the end time of the course on runtime.
"""
from datetime import datetime, timedelta

class CourseNode():
    def __init__(self, course_name:str, start_time:datetime, duration:int, location:str, prev_node=None, next_node=None, reminder:int=0):
        self.course_name = course_name
        self.start_time = start_time
        self.duration = duration
        # Calculate end time by adding the duration to the start time
        self.end_time = datetime.strptime(start_time, '%H:%M') + timedelta(minutes=duration)
        # TODO: Use Google Places API to get a google maps link to the location if found, else use the location string
        self.location = location
        self.prev_node = prev_node
        self.next_node = next_node
        self.reminder = reminder