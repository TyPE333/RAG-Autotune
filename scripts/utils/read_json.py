import json
import os

def json_generator(file_path:str):
    """
    """
    #check if file_path is valid 
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as file:
        try:
            data = json.load(file)
        except Exception as e:
            print(e)
        for item in data:
            yield item