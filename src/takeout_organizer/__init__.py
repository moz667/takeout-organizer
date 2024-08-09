#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum
import json
import os
import pathlib
import shutil
from tempfile import gettempdir

from simple_file_checksum import get_checksum

CUR_EXECUTION_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def archive_all(takeout_dir, archive_dir, dry_run=True):
    CUR_EXECUTION_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

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

                archive_target_dir_no_json = create_dir_if_not_exists(
                    os.path.join(archive_dir, 'no-json-data'), dry_run=dry_run
                )

                move_file(
                    cur_file, archive_target_dir_no_json, dry_run=dry_run
                )
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
        print("WARNING: '%s' dont have photoTakenTime/timestamp" % file_json)
        return
    
    taken_time = datetime.fromtimestamp(int(data['photoTakenTime']['timestamp']))
    
    archive_target_dir = create_archive_dir(
        archive_dir=archive_dir, 
        taken_time=taken_time, 
        dry_run=dry_run
    )

    trace_verbose("   * archive_dir: %s" % archive_dir)

    return_move_file = move_file(file, archive_target_dir, dry_run=dry_run)

    if return_move_file == MoveFileReturn.DIFERENT_CHECKSUM:
        archive_target_dir = create_dir_if_not_exists(
            os.path.join(archive_dir, 'duplicates-diferent-checksum'), dry_run=dry_run
        )

        return_move_file = move_file(
            file, archive_target_dir, dry_run=dry_run
        )
    
    log_move_file(file, return_move_file=return_move_file)

    return_move_file = move_file(file_json, archive_target_dir, dry_run=dry_run)
    log_move_file(file, return_move_file=return_move_file)


class MoveFileReturn(Enum):
    OK = 0
    ALREADY_EXISTS = 1
    DIFERENT_CHECKSUM = 2

def move_file(file, archive_target_dir, dry_run=True):
    file_basename = os.path.basename(file)
    archive_target_file = os.path.join(archive_target_dir, file_basename)

    trace_verbose("   * move_file: %s" % archive_target_file)

    if not os.path.exists(archive_target_file):
        if dry_run:
            print(">>> shutil.move('%s', '%s')" % (file, archive_target_dir))
        else:
            shutil.move(file, archive_target_dir)
    else:
        file_checksum = get_checksum(file)
        archive_target_file_checksum = get_checksum(archive_target_file)
        
        if file_checksum == archive_target_file_checksum:
            print("WARNING: Can't move '%s' to '%s', already exists" % (
                file, archive_target_file
            ))

            return MoveFileReturn.ALREADY_EXISTS
        else:
            print("WARNING: Can't move '%s' to '%s', already exists and has DIFERENT checksum!" % (
                archive_target_file, 
                file
            ))

            return MoveFileReturn.DIFERENT_CHECKSUM
    
    return MoveFileReturn.OK

def log_move_file(file, return_move_file):
    base_filename = 'takeout-organizer_%s.log' % CUR_EXECUTION_TIMESTAMP

    if return_move_file == MoveFileReturn.ALREADY_EXISTS:
        base_filename = 'takeout-organizer_already-exists_%s.log' % CUR_EXECUTION_TIMESTAMP
    elif return_move_file == MoveFileReturn.DIFERENT_CHECKSUM:
        base_filename = 'takeout-organizer_diferent-checksum_%s.log' % CUR_EXECUTION_TIMESTAMP
    
    with open(os.path.join(gettempdir(), base_filename), 'a') as log:
        log.write("%s\n" % file)
    

def create_archive_dir(archive_dir, taken_time, dry_run=True):
    create_dir_if_not_exists(archive_dir, dry_run)

    archive_dir = os.path.join(archive_dir, taken_time.strftime('%Y'))
    create_dir_if_not_exists(archive_dir, dry_run)

    archive_dir = os.path.join(archive_dir, taken_time.strftime('%m'))
    create_dir_if_not_exists(archive_dir, dry_run)

    return archive_dir

def create_dir_if_not_exists(path, dry_run=True):
    if not os.path.exists(path):
        if dry_run:
            print(">>> os.mkdir('%s')" % path)
        else:
            os.mkdir(path)
    
    return path

def trace_verbose(text):
    if __debug__:
        print(text)