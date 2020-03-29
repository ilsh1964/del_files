# Del_Files_V1

### SIMULATION_MODE = N
#### SIMULATION_MODE = Y shows files candinate to deletion
#### SIMULATION_MODE = N The file will be deleted

### DELETION_METHOD = FILE_TIMESTAMP
#### FILE_TIMESTAMP \ FILE_CREATION
#### FILE_TIMESTAMP depends on file timestamp: ie, files saved in this format: log_20160203
#### FILE_CREATION depends on the file creation date and not on it's name

## FILES_TEMPLATE = /path/to_file/log_*.tar.gz
#### The file template name, Example:
#### On Linux: /BACKUP/log_*
#### On Windows: C:\\Temp\\log_*)

## KEEP_FILES = 30
#### How many files to keep (works only on DELETION_METHOD = FILE_TIMESTAMP)

## KEEP_DAYS = 3
#### How many days to keep (works only on DELETION_METHOD = FILE_CREATION)

