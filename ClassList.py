"""
ClassList
~~~~~~~~~

A library for creating a linked list representing a weekly schedule using the CourseNode class.
Has functions to read from a pdf file, parse it using the webregParser library, and add the courses to the linked list.
"""
import webregParser as wrP
import webregScheduler

schedule = wrP.webregParser("webregMain.pdf")
weekly_df = schedule.get_weekly()
print(weekly_df)