# Import required packages
import os
import re
import pandas as pd


# Check for files
files = os.listdir()

# Look for txt files
for file in files:
    if '.txt' in file:
        txt_file = file

# Load the txt file and remove empty lines
text = open(txt_file, 'r+', encoding="utf8").readlines()
text = [line for line in text if re.search(r'\S', line)]

# Initialize empty lists to store date and messages
date = []
message = []
processed = ['' for i in range(len(text))]


# Loop through txt file and process it so each line has a date and a message
for index in range(len(text)):
        
        line = text[index]
       
        if len(re.findall(r'[0-9]+/+[0-9]+/+[0-9]+', line)) == 0:
                line = " ".join(text[index - 1].split()) + " " + " ".join(text[index].split())
                processed[index - 1] = line
        else:
                processed[index] = line
  
# loop through the processed file to add date and message
for line in processed:
        date.append(re.findall(r'[0-9]+/+[0-9]+/+[0-9]+', line))
        message.append(re.findall(r' - (.*)$', line))


        
# Convert into dataframe
df = pd.DataFrame({'date' : date, 'message' : message})

# Remove square brackets
df = df.apply(lambda x : x.str.get(0), axis=1)

# Remove missing rows
df = df.dropna()

# Convert to lowercase
df['message'] = df['message'].str.lower()

# Get the subject
df['subject'] = df['message'].str.split(":").str.get(0)

# Check for work from home
df['wfh'] = df['message'].str.contains('wfh') | df['message'].str.contains('work from home') | df['message'].str.contains('working from home')

# Check who worked from home on which days
wfh = df.query('wfh == True')
wfh = wfh.pivot_table(index='date', 
                      columns='subject', 
                      aggfunc='count', 
                      values='wfh',
                      fill_value=0).reset_index().rename_axis(None, axis=1)
wfh.to_csv('wfh_calendar.csv', index=None)