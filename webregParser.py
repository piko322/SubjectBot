"""
webregParser
~~~~~~~~~~~~

A library to parse a pdf file from the UCSD webreg website 
into pandas dataframe objects.
"""
import PyPDF2
import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import regex as re
import numpy as np
from datetime import datetime

# Use pdfReader to read ONLY the text contents of the pdf file
reader = open("webregMain.pdf", "rb")
pdfReader = PyPDF2.PdfFileReader(reader)

pageObj = pdfReader.getPage(0)
raw_data = pageObj.extract_text()
raw_data_lines=raw_data.split("\n")

# Find the index where the first course begins, by finding the line that starts with "Action"
course_start_index = [i for i in range(len(raw_data_lines)) if raw_data_lines[i].startswith("Action")][0]
raw_data_lines = raw_data_lines[course_start_index + 1:]