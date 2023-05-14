import os
import re
import sys
from pathlib import Path 

subs_path = Path.cwd()
subs_files = os.walk(subs_path)
sub_delay = sys.argv[1]

MILISECONDS_PER_HOUR = 3600000
MILISECONDS_PER_MINUTE = 60000
MILISECONDS_PER_SECOND = 1000

for dirpath, dirnames, filenames in subs_files:
    for filename in filenames:

        if filename.endswith('ass'):
                sub_file_location = Path(dirpath) / Path(str(filename))
                #print(sub_file_location, filename, filenames)
                text = open(sub_file_location, encoding = "UTF-8").readlines()
                output_file = open(sub_file_location, 'w', encoding = "UTF-8")
        else:
            continue
        
        print(sub_file_location)
    # if sub_file.endswith('srt'):
            
    #     time_regex = re.compile(r'\d\d:\d\d:\d\d,\d\d\d')
    #     for line in text:
            
    #         time_line = time_regex.search(line)
    #         if time_line != None:
    #             sub_time = time_line.group()
    #             continue

    #         if searched_term in line:
    #             output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time + '\n' + 'Dialogue: ' + line + '\n')

        if filename.endswith('ass'):
        
            time_regex = re.compile(r'\d,(\d):(\d\d):(\d\d\.\d\d)(,)(\d):(\d\d):(\d\d\.\d\d)')

            with open(sub_file_location) as sub_file_location:
                for num, line in enumerate(text, 0):
                
                    time = time_regex.search(line)
    
                    if time != None:
                        dialogue_regex = re.compile(r'(.*)(\d:\d\d:\d\d\.\d\d),(\d:\d\d:\d\d\.\d\d)(.*)') 
    
                        #Will divide the dialogue into (previous text, start time, end time, posterior text)
                        
                        line_content = dialogue_regex.search(line)
    
                        timestamps = []
    
                        for i in [1, 5]:
                        
                            hours = int(time.group(i))
                            minutes = int(time.group(i+1))
                            seconds = float(time.group(i+2))
    
                            #Separate in groups the different time units
    
                            miliseconds_total = int(hours * MILISECONDS_PER_HOUR + minutes * MILISECONDS_PER_MINUTE + seconds * MILISECONDS_PER_SECOND + sub_delay)
    
                            hours = miliseconds_total // MILISECONDS_PER_HOUR
                            miliseconds = miliseconds_total % MILISECONDS_PER_HOUR
    
                            minutes = miliseconds // MILISECONDS_PER_MINUTE
                            miliseconds = miliseconds % MILISECONDS_PER_MINUTE
    
                            seconds = round(miliseconds / MILISECONDS_PER_SECOND,2)
    
                            #Turn everything into miliseconds, add it up with the sub_delay and convert back
                            #to hours, minutes and seconds 
    
                            if len(str(minutes)) == 1:
                                minutes = '0' + str(minutes)
                            else:
                                minutes = str(minutes)
        
                            if len(str(seconds)) == 1:
                                seconds = '0' + str(seconds)
                            else:
                                seconds = str(seconds)
    
    
                            timestamp = str(hours) + ':' + minutes + ':' + seconds
    
                            timestamps.append(timestamp)
    
                        output_file.write(line_content.group(1) + timestamps[0] + ',' + timestamps[1] + line_content.group(4) + '\n')
    
                    else:
                        output_file.write(text[num])
        
