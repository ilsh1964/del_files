#!/usr/bin/env python3
# pylint: disable=R0914,W0612
"""
   delFiles - Delete log files(support several deletion method)

   Version: 3.2 - 2021-01-10
   Dev: Shavit Ilan (ilan.shavit@gmail.com)
"""

import logging
import glob
from datetime import date
import os
import json
import sys


def del_file_timestamp(base_dir, files_template, keep_files, \
                       simulation_mode, recursive_mode):
    """
        delete files on FILE_FIMESTAMP method
    """
    all_dir = [base_dir]
    if recursive_mode == "Y":
        for dirpath, dirs, files in os.walk(base_dir):
            all_dir.append(dirpath)

    for each_dir in all_dir:
        os.chdir(each_dir)
        files_list = glob.glob(files_template)
        files_list = sorted(files_list)
        num_files = len(files_list)

        if (num_files - keep_files) <= 0:
            log_message = "%s: No files to delete..." % each_dir
            if simulation_mode == 'Y':
                print(log_message)
            else:
                logging.info(log_message)


        for temp_i in range(num_files - int(keep_files)):
            log_message = "%s : %s" % (each_dir, files_list[temp_i])
            if simulation_mode == 'Y':
                print(log_message + " - Candidate file for deletion...")
            else:
                try:
                    os.remove(files_list[temp_i])
                    log_msg = log_message + " - Deleted!"
                    logging.info(log_msg)
                except OSError:
                    log_message = "%s: %s - OSError exception raised !!!" %\
                            (each_dir, files_list[temp_i])
                    logging.error(log_message)


def del_file_creation(base_dir, files_template, keep_days, simulation_mode, \
                      recursive_mode):
    """
        delete files on FILE_CREATION method
    """
    all_dir = [base_dir]
    if recursive_mode == "Y":
        for dirpath, dirs, files in os.walk(base_dir):
            all_dir.append(dirpath)

    current_date = date.today()
    for each_dir in all_dir:
        os.chdir(each_dir)
        files = glob.glob(files_template)
        need_delete = False
        for each_file in files:
            try:
                the_file = os.path.getmtime(each_file)
                the_file_ts = date.fromtimestamp(the_file)
                days_diff = (current_date - the_file_ts).days
                if days_diff > keep_days:
                    need_delete = True
                    log_message = "%s: %s" % (each_dir, each_file)
                    if simulation_mode == 'Y':
                        print(log_message + " - Candidate file for deletion...")
                    else:
                        os.remove(each_file)
                        log_msg = log_message + " - Deleted!"
                        logging.info(log_msg)
            except OSError:
                log_message = "%s: %s -  OSError Excepion Raised !!!" %\
                        (each_dir, each_file)
                logging.error(log_message)
            except TypeError:
                log_message = "%s: %s -  TypeError Exception Raised !!!" %\
                        (each_dir, each_file)
                logging.error(log_message)
        if not need_delete:
            log_message = "%s -  No files to delete..." % each_dir
            if simulation_mode == 'Y':
                print(log_message)
            else:
                logging.info(log_message)


def main():
    """
        read del_file.conf and call func to delete the files
        - SIMULATION_MODE: Y (Simulation mode)
                           N (Delete the files)
        - RECURSIVE MODE: Y (Scan directory RECURSIVELY)
                          N (Dont scan RECURSIVELY)
        - METHOD: T (depends on timestamp signature in the file name)
                  C (depends on file creation time)
        - BASE_DIR = C:\\PATH\\TO\\FILES (Windows) \\ /PATH/TO/FILES (Linux)
        - FILES_TEMPLATE = file_*.zip (starting with 'file', ending with 'zip')
        - KEEP = 5 How many files to keep (Last 5 FILES or 5 DAYS)
    """
    if os.name == 'posix':
        ini_file = "/etc/del_files.conf"
    elif os.name == 'nt':
        ini_file = os.path.expanduser('~') + "\\del_files.conf"
    else:
        print("Error: Unsupported platform")
        sys.exit()
    try:
        with open(ini_file, "r") as ini_file:
            json_content = json.load(ini_file)
    except FileNotFoundError:
        print("Missing or illegal config file: %s " % ini_file)
        sys.exit()
    for each_config in json_content:
        log_file = each_config["LOG_FILE"]
        logging.basicConfig(filename=log_file, level=logging.INFO,\
            format='%(asctime)s - %(levelname)s - %(message)s')
        simulation_mode = each_config['SIMULATION_MODE']
        base_dir = each_config['BASE_DIR']
        recursive_mode = each_config['RECURSIVE_MODE']
        method = each_config['METHOD']
        keep = int(each_config['KEEP'])
        files_template = each_config['FILES_TEMPLATE']

        if method == "T":
            del_file_timestamp(base_dir, files_template, keep, simulation_mode, recursive_mode)
        elif method == "C":
            del_file_creation(base_dir, files_template, keep, simulation_mode, recursive_mode)


if __name__ == "__main__":
    main()
