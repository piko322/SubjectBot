from webregScheduler import CourseNode, DaySchedule
from datetime import datetime, timedelta
class User:
    """User object representing a user of the application. 
    Attributes:
        Schedule: Dictionary containing the schedule for each day of the week
    """
    # Dictionary to convert from datetime day to MWThF day
    dayDict = {"Mon":"M", "Tue":"Tu", "Wed":"W", "Thu":"Th", "Fri":"F", "Sat":"Sa", "Sun":"Su"}
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.schedule = {}
    
    def add_class(self, node:CourseNode):
        if node.day not in self.schedule:
            self.schedule[node.day] = DaySchedule(node.day)
        self.schedule[node.day].insert(node)
    
    def get_next_class(self):
        """Returns the next class based on the current time. Returns None if there is no next class.

        Returns:
            CourseNode: The next class to attend
        """
        # Find the next class to attend based on the current time
        curr_time = datetime.now()
        curr_day = curr_time.strftime("%a")
        
        # Convert curr_day into the MWThF format
        curr_day = self.dayDict[curr_day]
        
        curr_time = curr_time.time()

        # If the current day is not in the schedule, return None
        if curr_day not in self.schedule:
            msg = "No classes today!!"
            return {"Message": msg, "Course": None}
        
        # If the current time is after the last class of the day, return None
        if curr_time > self.schedule[curr_day].get_last_end_time():
            msg = "The day's over, rest up!"
            return {"Message": msg, "Course": None}
        
        curr_node = self.schedule[curr_day].head.next_node
        while curr_node.get_start_time() < curr_time:
            curr_node = curr_node.next_node
            
        # Find the time difference between the current time and the start time of the next class
        curr_time = datetime.combine(datetime.today(), curr_time)
        start_time = datetime.combine(datetime.today(), curr_node.get_start_time())
        time_diff = start_time - curr_time
        
        # Print the remaining duration in x hours and y minutes
        msg = f"Next class is {curr_node.get_name()} in {time_diff.seconds//3600} hours and {(time_diff.seconds//60)%60} minutes."
        return {"Message": msg, "Course": curr_node}
    
    def get_current_class(self):
        """Returns the current class based on the current time. Returns None if there is no current class.
        """
        curr_time = datetime.now()
        curr_day = curr_time.strftime("%a")
        curr_day = self.dayDict[curr_day]
        curr_time = curr_time.time()
        
        # If the current day is not in the schedule, return None
        if curr_day not in self.schedule:
            msg = ("No classes today!!")
            return {"Message": msg, "Course": None}
        
        no_class_msg = ("No classes currently in session.")
        
        # Iterate through the day schedule until the current time is between the start and end times of a class
        for course in self.schedule[curr_day]:
            if course.get_start_time() <= curr_time <= course.get_end_time():
                # Find the difference between two datetime.time objects
                curr_time = datetime.combine(datetime.today(), curr_time)
                end_time = datetime.combine(datetime.today(), course.get_end_time())
                time_diff = end_time - curr_time
                
                # Print the remaining duration
                msg = f"Class {course.get_name()} is still in session for {time_diff.seconds//60} minutes."
                return {"Message": msg, "Course": course}
            
            if course.get_start_time() > curr_time:
                # If the current time is before the start time of the first class, return None
                return {"Message": no_class_msg, "Course": None}
            
        # If iteration reaches the end of the schedule without any matches, return None
        return {"Message": no_class_msg, "Course": None}
    
    def get_schedule(self):
        # Sort the schedule keys by day of the week
        sorted_days = sorted(self.schedule.keys(), key=lambda day: ["M", "Tu", "W", "Th", "F", "Sa", "Su"].index(day))
        self.schedule = {day:self.schedule[day] for day in sorted_days}
        return self.schedule

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return f"User {self.name} with ID {self.id}, schedule: {self.schedule}"