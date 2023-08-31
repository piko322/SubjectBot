"""
webregParser
~~~~~~~~~~~~

A library to parse a pdf file from the UCSD webreg website 
into pandas dataframe objects. Initializes with a filepath to a pdf file,
and has functions to return the weekly and non weekly events as pandas dataframes.
"""
import PyPDF2
import pandas as pd
from tabula import read_pdf
from tabulate import tabulate
import regex as re
import numpy as n
from datetime import datetime

class webregParser:
    
    #TODO: Make this compatible with URLs
    def __init__(self, filepath:str):
        
        self.filepath = filepath
        # Use pdfReader to read ONLY the text contents of the pdf file
        reader = open(filepath, "rb")
        pdfReader = PyPDF2.PdfFileReader(reader)

        pageObj = pdfReader.getPage(0)
        raw_data = pageObj.extract_text()
        raw_data_lines=raw_data.split("\n")

        # Find the index where the first course begins, by finding the line that starts with "Action"
        course_start_index = [i for i in range(len(raw_data_lines)) if raw_data_lines[i].startswith("Action")][0]
        raw_data_lines = raw_data_lines[course_start_index + 1:]

        # Read the raw data into a pandas dataframe using tabula
        raw_df = read_pdf(filepath, pages="all")[0]

        def repair_column(df: pd.DataFrame, col: str, raw_data_lines: list) -> list:
            """
            Tabula does not always parse the columns correctly due to the way webreg formats their tables, 
            and PyPDF2 only reads the text in the pdf, not the tables.
            so this function takes in the raw dataframe from tabula, the column name to be fixed, and the raw_data_lines list from PyPDF2.
            It then identifies "broken" columns by finding string entries that start with a lower case letter, and fixes them by
            matching the value in the broken column with the data in the raw_data_lines list using regex.
            """
            # The "Units" column contain floats, so no need to fix it
            if col == "Units":
                return df[col]
            broken_col = df[col].tolist()
            # Fix the broken column by finding matching text in the "Title" column and the raw_data_lines list
            for i in range(len(broken_col)):
                broken_val = broken_col[i]
                fix_val = raw_data_lines[i]
                
                # if broken_val is NaN, continue
                if broken_val != broken_val:
                    continue

                # If the first character in broken_val is in lower case, fix it by matching it to the fix_val
                if broken_val[0].islower():
                    # Find the index of the string in broken_val inside the fix_val, and decrement by one to get the missing character
                    search_value = re.search(broken_val, fix_val)
                    
                    # If search_value is None, try to take the first 5 characters of broken_val and search for it in fix_val        
                    if search_value is None:
                        search_value = re.search(broken_val[:5], fix_val)
                    try:
                        fix_index = search_value.start()
                    except:
                        continue    
                    missing_char = fix_val[fix_index - 1]
                    broken_col[i] = missing_char + broken_val
            return broken_col

        # Adjust the column titles to the correct position, and drop the NaN columns
        df = raw_df.copy()
        df.columns = list(df.columns[1:]) + ["dummy"]
        df.columns = [title.replace("\r", " ") for title in df.columns]
        df = df[df.columns[:-3]]

        # If the last row is all NaN, drop it
        if df.iloc[-1].isnull().all():
            df = df.iloc[:-1]
        # For each NaN in the "Subject Course" column, fill it with the value above it
        df["Subject Course"] = df["Subject Course"].fillna(method="ffill")
        for col in df.columns:
            df[col] = repair_column(df, col, raw_data_lines)
        df = df[["Subject Course", "Title", "Section Code", "Type", "Days", "Time", "Instructor", "Units", "Status / (Position)", "BLDG", "Room", "Grade Option"]]
        
        self.df = df
        
    def get_weekly(self):
        """Get the weekly schedule dataframe for this webregParser object by
        filtering out the non weekly events and returning a new formatted dataframe
        """
        # Create a DataFrame only containing the weekly reoccuring classes
        weekly_df = self.df.copy()

        # Filter out the entries with NaN or TBA days
        weekly_df = weekly_df[(weekly_df["Days"].notna()) & (weekly_df["Days"] != "TBA")]
        # Filter out the entries where the "Days" includes numbers
        weekly_df = weekly_df[weekly_df["Days"].apply(lambda x: not any(char.isdigit() for char in x))]
        
        # Reset the index of weekly_df
        weekly_df.reset_index(inplace=True)
        weekly_df.drop(columns=["index"], inplace=True)

        # For each row in weekly_df, split the "Days" column by uppercase letters into a list
        weekly_df["Days"] = weekly_df["Days"].apply(lambda day: re.findall('[A-Z][^A-Z]*', day)) 

        # Split the values in the "Time" column to get the start and end time
        weekly_df["Time"] = weekly_df["Time"].apply(lambda time: time.split("-"))

        # For the "Title" column of weekly_df, if the value is NaN then replace it with the Subject Course value 
        # and add the type value at the end
        for i in range(len(weekly_df)):
            row = weekly_df.iloc[i]
            title = row["Title"]
            if title != title:
                subject_course = row["Subject Course"]
                course_type = row["Type"]
                new_title = subject_course + " " + course_type
                weekly_df.loc[i, "Title"] = new_title
        # Add a new column for the node parser to use, which is a concatenation of the "Subject Course" and "Type" columns
        weekly_df["Node Title"] = weekly_df["Subject Course"] + " " + weekly_df["Type"]

        return weekly_df
    
    def get_non_weekly(self):
        """Get the non weekly schedule dataframe for this webregParser object
        """
        non_weekly_df = self.df.copy()
        
        # Filter out the entries where the "Days" column is NaN or "TBA"
        non_weekly_df = non_weekly_df[(non_weekly_df["Days"].notna()) & (non_weekly_df["Days"] != "TBA")]
        
        # Filter in only the entries where the "Days" column contains a number
        non_weekly_df = non_weekly_df[non_weekly_df["Days"].apply(lambda x: any(char.isdigit() for char in x))]
        
        # Rename the "Days" into "Date"
        non_weekly_df = non_weekly_df.rename(columns={"Days": "Date"})

        non_weekly_df.drop(columns=["Section Code", "Instructor", "Units", "Status / (Position)", "Grade Option"], inplace=True)

        non_weekly_df["Time"] = non_weekly_df["Time"].apply(lambda x: x.split("-"))
        
        return non_weekly_df    
    
    def update_filepath(self, filepath:str):
        self.filepath(filepath)
    
    def __repr__(self):
        return f"webregParser object reading from file {self.filepath} with weekly df size {self.weekly_df.shape[0]} and non weekly df size {self.non_weekly_df.shape[0]}"
    
