# Del_Files
#### First usage: copy del_files_example.conf to del_files.conf and update your personal config preferences


- SIMULATION_MODE: Y (Simulation mode) \ N (Delete the files)
- RECURSIVE MODE: Y (Scan directory RECURSIVELY) \ N (Don't scan RECURSIVELY)
- METHOD: T (depends on timestamp signature in the file name) \ C (depends on file creation time)
- BASE_DIR = C:\PATH\TO\FILES (Windows) \ /PATH/TO/FILES (Linux)
- FILES_TEMPLATE = file_*.zip (look for files starting with 'file', ending with 'zip')
- KEEP = 5 How many files to keep (Last X FILES or X DAYS)

