#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
   delFiles - Delete log files(support several deletion method)

   Version: 2.0 (2020-03-28)
   Dev: Shavit Ilan (ilan.shavit@gmail.com)
"""


### import section ###
import logging
import glob
from ConfigParser import SafeConfigParser
from datetime import datetime, date
import os
import sys


def get_timestamp():
    """
        return timestamp in this format '2012-12-07 17:45:57'
    """
    timestamp = str(datetime.now())
    return timestamp[0:19]


def del_file_timestamp(files_template, keep_files, simulation_mode):
    """
        delete files on FILE_FIMESTAMP method
    """
    files_list = glob.glob(files_template)
    files_list = sorted(files_list)
    num_files = len(files_list)

    if (num_files - keep_files) <= 0:
        log_message = "%s \t No files to delete..." % get_timestamp()
        if simulation_mode == 'Y':
            print log_message
        else:
            logging.info(log_message)


    for temp_i in range(num_files - int(keep_files)):
        log_message = "%s \t %s \t is going to be deleted..." % \
                        (get_timestamp(), files_list[temp_i])
        if simulation_mode == 'Y':
            print log_message
        else:
            logging.info(log_message)
            os.remove(files_list[temp_i])


def del_file_creation(files_template, keep_days, simulation_mode):
    """
        delete files on FILE_CREATION method
    """
    current_date = date.today()
    files = glob.glob(files_template)

    need_delete = False
    for each_file in files:
        the_file = os.path.getctime(each_file)
        the_file_ts = date.fromtimestamp(the_file)
        days_diff = (current_date - the_file_ts).days
        if days_diff > keep_days:
            need_delete = True
            log_message = "%s \t %s \t is going to be deleted..." % \
                            (get_timestamp(), each_file)
            if simulation_mode == 'N':
                logging.info(log_message)
                os.remove(each_file)
            else:
                print log_message
    if not need_delete:
        log_message = "%s \t No files to delete..." % get_timestamp()
        if simulation_mode == 'Y':
            print log_message
        else:
            logging.info(log_message)


def main():
    """
        Explain the function of the main program
    """
    # Initialize Parser and logging modules
    if 'linux' in sys.platform:
        ini_file = sys.argv[0].replace("del_files.py", "del_files.ini")
        log_file = sys.argv[0].replace("del_files.py", "del_files.log")
    elif 'win' in sys.platform:
        ini_file = sys.argv[0].replace("del_files.exe", "del_files.ini")
        log_file = sys.argv[0].replace("del_files.exe", "del_files.log")

    logging.basicConfig(filename=log_file, level=logging.INFO)
    parser = SafeConfigParser()
    parser.read(ini_file)
    simulation_mode = parser.get('CONFIG', 'SIMULATION_MODE')
    deletion_method = parser.get('CONFIG', 'DELETION_METHOD')
    keep_files = int(parser.get('CONFIG', 'KEEP_FILES'))
    keep_days = int(parser.get('CONFIG', 'KEEP_DAYS'))
    files_template = parser.get('CONFIG', 'FILES_TEMPLATE')

    if deletion_method == "FILE_TIMESTAMP":
        del_file_timestamp(files_template, keep_files, simulation_mode)
    elif deletion_method == "FILE_CREATION":
        del_file_creation(files_template, keep_days, simulation_mode)


if __name__ == "__main__":
    main()

