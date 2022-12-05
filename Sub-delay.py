import os
import re
import sys
from pathlib import Path 

subs_path = Path.cwd()
output_path = Path.cwd() / 'Search-matches.txt'
subs_files = os.listdir(subs_path)
sub_delay = 1000

MILISECONDS_PER_HOUR = 3600000
MILISECONDS_PER_MINUTE = 60000
MILISECONDS_PER_SECOND = 1000



seconds = sub_delay // 1000
minutes = seconds 

for sub_file in subs_files:

    sub_file_location = Path(subs_path) / Path(str(sub_file))
    text = open(sub_file_location, encoding = "UTF-8").readlines()
    #output_file = open(output_path, 'a', encoding = "UTF-8")

    if sub_file.endswith('srt'):
        
        time_regex = re.compile(r'\d\d:\d\d:\d\d,\d\d\d')
        for line in text:
            
            time_line = time_regex.search(line)
            if time_line != None:
                sub_time = time_line.group()
                continue

            if searched_term in line:
                output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time + '\n' + 'Dialogue: ' + line + '\n')

    if sub_file.endswith('ass'):

        time_regex = re.compile(r'\d,\d:\d\d:\d\d.\d\d')

        with open(sub_file_location) as sub_file_location:
            for num, line in enumerate(sub_file_location, 0):
                if time_regex.search(line) != None:
                    dialogue_regex = re.compile(r'}(.*)')
                    dialogue = dialogue_regex.search(line).group(1)

                    #Search for a typesetting dialogue and gets its text

                    sub_time = time_regex.search(line).group()
                    
                    #Separate the total of miliseconds in miliseconds, seconds, minutes, etc.
                else:
                    dialogue_regex = re.compile(r'\d,\d,\d,,(.*)')
                    dialogue = dialogue_regex.search(line)
                    output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time.group() + '\n' + 'Dialogue: ' + dialogue.group(1) + 2 * '\n')
#Use split(,,) to get the dialogue text and add it to the new line Dialogue:  (delayed timing)

#output_file.close()