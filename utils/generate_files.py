from pathlib import Path
import os
import re


def remove_code_block_markers(text):
    pattern = re.compile(r'```[a-z]+\n(.*?)\n```', re.DOTALL)
    result = pattern.sub(r'\1', text)
    return result


def create_directory(path):
    print("Entered create directory")
    try:
        os.makedirs(path)
    except Exception as e:
        raise Exception(f"Error occured while making directory {e}")


def create_file(path):
    Path(path).touch()


def generate_files(file_structure, base_dir, chat, project):
    for item in file_structure:
        full_path = os.path.join(base_dir, item['path'].lstrip('/'))
        print(f"type: {item['type']}, path: {
              item['path']}, full_path: {full_path}")
        if item['type'] == 'directory':
            create_directory(full_path)
        elif item['type'] == 'file':
            create_file(full_path)
            instruction = "Based on the file directory you gave me generate code for this & this file only" + \
                "Caution: only generate code and nothing else & only for the file that is described" + \
                f"generate code for: {item['path']}" + \
                f"details: {project}"
            res = chat.send_message(instruction)
            code = remove_code_block_markers(res.text)
            with open(full_path, "w") as file:
                file.write(code)
