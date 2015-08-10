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
For each backup dory will create a new folder with the current date and time.
Dory will then create two subfolders in `destination`:
```
destination/
    2022_08_10_13_45_31/
    2022_08_11_13_45_31/
    2022_08_10_13_45_31.log
    2022_08_11_13_45_31.log
    ...
```

each folder contains the _whole_ backup, but space usage is minimized due to the use of **hardlinks**.
