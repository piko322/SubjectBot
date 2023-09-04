from webregScheduler import CourseNode, DaySchedule
class User:
    """User object representing a user of the application. 
    Attributes:
        Schedule: Dictionary containing the schedule for each day of the week
    """
    
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.schedule = {}
    
    def add_class(self, node:CourseNode):
        if node.day not in self.schedule:
            self.schedule[node.day] = DaySchedule(node.day)
        self.schedule[node.day].insert(node)
    
    def get_schedule(self):
        # Sort the schedule keys by day of the week
        sorted_days = sorted(self.schedule.keys(), key=lambda day: ["M", "Tu", "W", "Th", "F", "Sa", "Su"].index(day))
        self.schedule = {day:self.schedule[day] for day in sorted_days}
        return self.schedule.values()

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return f"User {self.name} with ID {self.id}, schedule: {self.schedule}"