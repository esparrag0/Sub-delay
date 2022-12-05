import os
import re
import sys
from pathlib import Path 

subs_path = Path.cwd()
output_path = Path.cwd() / 'Search-matches.ass'
subs_files = os.listdir(subs_path)
sub_delay = 73400

MILISECONDS_PER_HOUR = 3600000
MILISECONDS_PER_MINUTE = 60000
MILISECONDS_PER_SECOND = 1000

for sub_file in subs_files:

    sub_file_location = Path(subs_path) / Path(str(sub_file))
    text = open(sub_file_location, encoding = "UTF-8").readlines()
    output_file = open(output_path, 'a', encoding = "UTF-8")

    # if sub_file.endswith('srt'):
        
    #     time_regex = re.compile(r'\d\d:\d\d:\d\d,\d\d\d')
    #     for line in text:
            
    #         time_line = time_regex.search(line)
    #         if time_line != None:
    #             sub_time = time_line.group()
    #             continue

    #         if searched_term in line:
    #             output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time + '\n' + 'Dialogue: ' + line + '\n')

    if sub_file.endswith('ass'):

        time_regex = re.compile(r'\d,(\d):(\d\d):(\d\d).(\d\d)')

        with open(sub_file_location) as sub_file_location:
            for num, line in enumerate(text, 0):

                time = time_regex.search(line)

                if time != None:
                    dialogue_regex = re.compile(r'(.*)(\d,\d:\d\d:\d\d.\d\d)(.*)') #Just considers the ending time
                    
                    #Will divide the dialogue into (previous text, time, posterior text)

                    line_content = dialogue_regex.search(line)

                    hours = int(time.group(1))
                    minutes = int(time.group(2))
                    seconds = int(time.group(3))
                    miliseconds = int(time.group(4))*10

                    #Separate in groups the different time units

                    miliseconds_total = miliseconds + hours * MILISECONDS_PER_HOUR + minutes * MILISECONDS_PER_MINUTE + seconds * MILISECONDS_PER_SECOND + sub_delay
                    
                    hours = miliseconds_total // MILISECONDS_PER_HOUR
                    miliseconds = miliseconds_total % MILISECONDS_PER_HOUR

                    minutes = miliseconds // MILISECONDS_PER_MINUTE
                    miliseconds = miliseconds % MILISECONDS_PER_MINUTE

                    seconds = miliseconds // MILISECONDS_PER_SECOND
                    miliseconds = miliseconds % MILISECONDS_PER_SECOND #prolly will have to divide by 10, round to two digits
                                                                       # and treat it as a
                                                                       #fraction of a second to dont worry about padding
                                                                       #or exceding the amount of digits.

                    #Turn everything into miliseconds, add it up with the sub_delay and convert back
                    #to hours, minutes, seconds and miliseconds
        
                    #prolly wrong to include miliseconds here
                    if len(str(minutes)) == 1:
                        minutes = '0' + str(minutes)
                    else:
                        minutes = str(minutes)
   
                    if len(str(seconds)) == 1:
                        seconds = '0' + str(seconds)
                    else:
                        seconds = str(seconds)

                    if len(str(miliseconds)) == 1:
                        miliseconds = '0' + str(miliseconds)
                    else:
                        miliseconds = str(miliseconds)

                    timestamp = '0,' + str(hours) + ':' + minutes + ':' + seconds + '.' + miliseconds

                    output_file.write(line_content.group(1) + timestamp + line_content.group(3) + '\n')

                else:
                    output_file.write(text[num])



#Use split(,,) to get the dialogue text and add it to the new line Dialogue:  (delayed timing)

#output_file.close()