#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import hashlib
import json
import pathlib
import shutil
import os

def archive_all(takeout_dir, archive_dir, dry_run=True):
    trace_verbose(
        ">>> archive_all(takeout_dir=%s, archive_dir=%s, dry_run=%s) <<<" % 
        (takeout_dir, archive_dir, dry_run)
    )

    for dirpath, dirs, files in os.walk(takeout_dir):
        trace_verbose(" + source: %s" % dirpath)

        for dir in dirs:
            archive_all(
                takeout_dir=os.path.join(dirpath, dir), 
                archive_dir=archive_dir,
                dry_run=dry_run
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
    
    archive_target_dir = create_archive_dir(
        archive_dir=archive_dir, 
        taken_time=taken_time, 
        dry_run=dry_run
    )

    trace_verbose("   * archive_dir: %s" % archive_dir)

    move_file(file, archive_target_dir, dry_run=dry_run)
    move_file(file_json, archive_target_dir, dry_run=dry_run)

def move_file(file, archive_target_dir, dry_run=True):
    file_basename = os.path.basename(file)
    archive_target_file = os.path.join(archive_target_dir, file_basename)

    trace_verbose("   * move_file: %s" % archive_target_file)

    if not os.path.exists(archive_target_file):
        if dry_run:
            print('>>> shutil.move(%s, %s)' % (file, archive_target_dir))
        else:
            shutil.move(file, archive_target_dir)
    else:
        print("WARNING: %s already exists" % archive_target_file)
        file_sha1 = calculate_sha1(file)
        archive_target_file_sha1 = calculate_sha1(archive_target_file)
        
        print("WARNING: %s with %s SHA1 than %s" % (
            archive_target_file, 
            'DIFERENT' if file_sha1 != archive_target_file_sha1 else 'same', 
            file
        ))

def calculate_sha1(file):
    openedFile = open(file, 'rb')
    readFile = openedFile.read()
    return hashlib.sha1(readFile).hexdigest()

def create_archive_dir(archive_dir, taken_time, dry_run=True):
    def create_dir_if_not_exists(path):
        if not os.path.exists(path):
            if dry_run:
                print('>>> os.mkdir(%s)' % path)
            else:
                os.mkdir(path)

    create_dir_if_not_exists(archive_dir)

    archive_dir = os.path.join(archive_dir, taken_time.strftime('%Y'))
    create_dir_if_not_exists(archive_dir)

    archive_dir = os.path.join(archive_dir, taken_time.strftime('%m'))
    create_dir_if_not_exists(archive_dir)

    return archive_dir

def trace_verbose(text):
    if __debug__:
        print(text)