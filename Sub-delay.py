import os
import re
import sys
from pathlib import Path 

subs_path = Path.cwd()
output_path = Path.cwd() / 'Search-matches.txt'
searched_term = sys.argv[1]
subs_files = os.listdir(subs_path)
episode_regex = re.compile(r'\d\d')
season_regex = re.compile(r'S\d\d')

for sub_file in subs_files:

    sub_file_location = Path(subs_path) / Path(str(sub_file))
    text = open(sub_file_location, encoding = "UTF-8").readlines()
    output_file = open(output_path, 'a', encoding = "UTF-8")
    episode = episode_regex.findall(sub_file)
    if episode == None:
        continue
    if season_regex.search(sub_file) == None:
        num = 0
    else:
        num = 1

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

        for line in text:

            if searched_term in line and 'Dialogue' in line:
                dialogue_regex = re.compile(r'}(.*)')
                dialogue = dialogue_regex.search(line)
                
                sub_time = time_regex.search(line)

                if dialogue != None:  
                    output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time.group() + '\n' + 'Dialogue: ' + dialogue.group(1) + 2 * '\n')

                else:
                    dialogue_regex = re.compile(r'\d,\d,\d,,(.*)')
                    dialogue = dialogue_regex.search(line)
                    output_file.write('Episode: ' + episode[num] + '\n' + 'Start time: ' + sub_time.group() + '\n' + 'Dialogue: ' + dialogue.group(1) + 2 * '\n')

output_file.close()