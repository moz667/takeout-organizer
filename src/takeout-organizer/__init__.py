#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import pathlib
import os

def archive_all(takeout_dir, archive_dir, dry_run=True):
    for dirpath, dirs, files in os.walk(takeout_dir):
        trace_verbose(" + source: %s" % dirpath)

        for dir in dirs:
            archive_all(
                takeout_dir=os.path.join(dirpath, dir), 
                archive_dir=archive_dir
            )
        
        for file in files:
            trace_verbose("   * file: %s" % file)
            cur_file = os.path.join(dirpath, file)
            cur_file_extension = pathlib.Path(cur_file).suffix

            # 1. Si la extension es json o no tiene extension (archivo oculto), 
            # pasamos al siguiente fichero
            if cur_file_extension.lower() == '.json' or \
                cur_file_extension == '':
                continue
            
            # 2. Si NO existe un archivo que se llame igual que el actual pero 
            # con la extension .json, sacamos mensaje por pantalla y continuamos
            cur_file_json = os.path.join(dirpath, file + '.json')
            if not os.path.isfile(cur_file_json):
                print("WARNING: %s not found" % cur_file_json)
                continue
            
            archive_file(
                file=cur_file, 
                file_json=cur_file_json, 
                archive_dir=archive_dir, 
                dry_run=dry_run
            )

def archive_file(file, file_json, archive_dir, dry_run=True):
    with open(file_json) as json_data:
        data = json.load(json_data)

    if not 'photoTakenTime' in data or \
        not 'timestamp' in data['photoTakenTime']:
        print("WARNING: %s dont have photoTakenTime/timestamp" % file_json)
        return
    
    taken_time = datetime.fromtimestamp(int(data['photoTakenTime']['timestamp']))

    # TODO: Estamos por aqui...

"""
# taken_time = datetime.datetime(2024, 3, 3, 9, 50, 28)
>>> taken_time.year
2024
>>> taken_time.month
3
>>> taken_time.day
3
"""

def trace_verbose(text):
    if __debug__:
        print(text)