dory is just a simplified rsync command for simple backup.

**This is not finished yet, so DO NOT use it unless for testing!!**

## requirements
- python3.4
    - termcolor
- rsync
- ssh

## Usage
```
dory source destination
```

where either source or destination can be a remote ssh path.

## Folder Structure
For each backup dory will create a new folder with the current date and time and a log file in the specified `destination`.
```
destination/
    2022_08_10_134531/
    2022_08_10_134531.log

    2022_08_11_150011/
    2022_08_11_150011.log

    2022_08_12_091122.part/    <- currently running backup
    2022_08_12_091122.log
    
    ...
```

Each folder contains the _whole_ backup, but space usage is minimized due to the use of **hardlinks**.

For currently running backups the folder will end with `.part`. In case the backup process crashes one always knows, that those folders are not completely finished!
After a successful backup the `.part` is removed from the folder name.
