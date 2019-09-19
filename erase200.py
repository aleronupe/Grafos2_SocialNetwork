import os
import json
path = 'data/ids'

files = []

for root, dirs, files_ in os.walk(path):
    for filename in files_:
        files.append(filename)

for f in files:
    delete = False
    all_path = path + '/' + f
    if f != '.keep':
        with open(all_path) as json_file:
                data = json.load(json_file)
                print(f, len(data))
                if (not len(data) % 202) and (len(data) > 0):
                        delete = True
    if delete:
        os.remove(path + '/' + f)
        print('\ndelete', f, '\n' )

