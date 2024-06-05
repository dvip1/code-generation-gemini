from pathlib import Path
import google.generativeai as genai
from utils.convert_zip import ConvertZip
from utils.generate_files import generate_files
import os
import json
import re
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])


if __name__ == "__main__":
    file = input("what's the tech stack, for ex: (html,css, js)/ python : ")
    project = input("what do you want to make: ")
    context = "can you generate file system for the " + \
        file + " for this project " + project + \
        " Caution: Please don't generate any code for now, only the file system" + \
        " Additional Note: Don't generate assets in file structure for ex: image.jpg" + \
        ' Format(like python dictionary): [{"type": "directory", "path": "/project-name/"}, {"type": "file", "path": "project-name/index.html"}, {"type": "directory", "path": "project-name/css/"}, {"type": "file", "path": "project-name/css/styles.css"}] '
    response = chat.send_message(context)

    response_text = re.sub(r'```json\n|\n```', '', response.text)
    response_text = re.sub(r'\s', '', response_text)
    json_object = json.loads(response_text)

    print(json.dumps(json_object, indent=4))
    base_dir = os.getcwd()
    generate_files(base_dir=base_dir, file_structure=json_object,
                   chat=chat, project=project)
    dir = base_dir+json_object[0]["path"]
    zip_name = json_object[0]["path"]
    ConvertZip(dir, zip_name[1:-1])
