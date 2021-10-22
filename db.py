import sqlite3 as sl
from os.path import exists
import json
import os
import numpy as np


json_template = {
    "filename": [],
    "inference": [],
    "confidence": [],
    "saveLocation": []
}


def init_json(db_path):

    path = os.path.join(db_path, 'mydb.json')
    file_exists = exists(path)

    if not file_exists:
        with open(path, 'w') as outfile:
            json.dump(json_template, outfile)

    with open(path) as json_file:
        json_format = json.load(json_file)
    return(json_format)


def update_json(json_format, json_file):
    for key in json_format.keys():
        json_format[key].append(json_file[key])

    with open('media/db/mydb.json', 'w') as outfile:
        json.dump(json_format, outfile)
    return(json_format)


def get_prev(json_file):
    json_return = {}
    length = len(json_file["filename"])
    length = np.min([length, 5])
    for key in json_file.keys():
        json_return[key] = json_file[key][-length:]
    return(json_return)


def convert(json_file):
    outputs = []
    length = len(json_file["filename"])
    for i in range(length):
        outputs.append([
                        json_file["filename"][i],
                        json_file["inference"][i],
                        json_file["saveLocation"][i],
                        json_file["confidence"][i]
                        ])
    return(outputs)
