import json
import re
import socket
import os
import argparse
import sys

# Verbose STDERR printing helper function
def veprint(*args, **kwargs):
    global verbose
    if verbose: 
        print(*args, file=sys.stderr, **kwargs)

## Allowed tag words = (allowed characters: all alphanumerics, '/', '-', and '_')
def validateTags(data):
    valid_tag_pattern = re.compile('^[a-zA-Z0-9_/-]+$')
    for i,(reg,tag) in enumerate(data.items()):
        if not re.match(valid_tag_pattern, tag): 
          veprint("tag name invalid: ", tag )  
          return False
    return True
    
parser = argparse.ArgumentParser()
parser.add_argument("-j","--tagsfilepath", type=str, help="File location for json.tags", default="tags.json")
parser.add_argument("-x", "--execute", help="Execute command (requires sudo)", action="store_true")
parser.add_argument("--verbose", help="increase output verbosity", default=False, action="store_true")
args = parser.parse_args()

verbose = args.verbose
veprint("verbosity turned on printing to STDERR")

if args.execute:
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script option.\nPlease try again, this time using 'sudo'. Exiting.")

hostname = socket.gethostname()

with open(args.tagsfilepath, "r") as jsonfile:
    data = json.load(jsonfile)
    jsonfile.close()

if validateTags(data):
    veprint("Tagname validated")
else:
    exit(args.tagsfilepath, "Is missing valid tagnames - all alphanumerics, '/', '-', and '_' . Exiting.")
    
tag_set = set()

for i,(reg,tag) in enumerate(data.items()):
    x = re.search(reg, hostname) 
    if x:
        tag_set.add(tag)
        veprint("Found - TAG: '", tag, "' REGEX: '", reg, "'", sep='')

tags_str = ','.join(tag_set)

if args.execute:
    os.system('/opt/CrowdStrike/falconctl -s --tags="', tags_str, '"',sep='')
    os.system(' systemctl restart falcon-sensor')
else:
    print('sudo /opt/CrowdStrike/falconctl -s --tags="', tags_str, '"',sep='')
    print('sudo systemctl restart falcon-sensor')
