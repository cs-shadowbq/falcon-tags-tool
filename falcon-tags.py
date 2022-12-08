import json
import re
import socket

hostname = socket.gethostname()

with open("tags.json", "r") as jsonfile:
    data = json.load(jsonfile)
    jsonfile.close()

tag_set = set()

for i,(reg,tag) in enumerate(data.items()):
    x = re.search(reg, hostname) 
    if x:
        tag_set.add(tag)

tags_str = ','.join(tag_set)
    
print('falconctl -s --tags="', tags_str, '"',sep='')
print('systemctl restart falcon-sensor')
