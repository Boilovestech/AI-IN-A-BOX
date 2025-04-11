import os
import json
import datetime as datetime
prompt = "hi"

files_list = []
dir_list = []

for root, dirs, files in os.walk("LLM_CLI_FILEACCESS\\sandbox", topdown=True):
    for name in files:
        file_path = os.path.join(root, name)
        files_dict = {
            "name": name,
            "type": "File",
            "path": file_path,
            "Creation: ": str(datetime.datetime.fromtimestamp(os.path.getctime(file_path))),  # Convert creation time
            "last modified: ": str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))  # Convert modification time
        }
        files_list.append(files_dict)

    for name in dirs:
        str_dirs = "Directory:" + name
        dir_dict = {
            "name": str_dirs,
            "type": "Directory",
            "path": os.path.join(root, name)
        }
        files_list.append(dir_dict)
print(files_dict)
#----------------------------#

file_list_final = [files_list]
#----------------------------#

#jsonify the structure
def jsonify(structure):
    json_structure = json.dumps(structure, indent=4)
    return json_structure

json_str = jsonify(file_list_final)

def structure_to_use():
    return json_str

#----------------------------#
#read the contents of the file
def read_file_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()
