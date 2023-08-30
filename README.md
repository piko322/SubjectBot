# SubjectBot
SubjectBot for Discord that I originally wrote in 2020 to help me with navigating online learning through high school during the COVID lockdown

## Current goals:
- Refactor the code to minimize the use of global variables
- Replace the "timeRefresh" function to use datetime objects instead of integers
- Replace nested list indexes with dictionaries to improve code readability
- Store the configs in a .txt or .json such that they can be dynamically changed and stored even after the bot turns off
- Create commands allowing users to modify their class schedule
- Modify the timetable system to use a linked list to iterate through courses on given days, using the individual courses as nodes