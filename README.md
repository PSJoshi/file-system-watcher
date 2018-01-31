### Purpose
This python script can be used for tracking file/directory changes. It also reports the difference between two snap shots of the file/directory under watch and list out file addition or file deletion or file modifications.

There are many ways to monitor file/directory changes in real time. One such example is fswatch program available here:
https://github.com/emcrisostomo/fswatch

Other ways to watch files/directories include making use of file integrity monitors like tripwire(https://www.tripwire.com/products/tripwire-file-integrity-manager/), aide(http://aide.sourceforge.net) and run the cron job on a daily basis to find out differences.

Since I wanted to know how easy it is to write a python script to monitor file/directory changes, I wrote this script to get first hand experience.

 
### Description 

The main script - tracker.py supports two functions:
* snap  - take a snapshot of file(s) and/or directories under its watch
* diff - report differences between the file/directory snapshots in terms of file addition/deletion/modifications.

#### snap function
When tracker.py is called with snap argument, it saves the state of the file system PATH as a json snapshot file. The snapshot contains a list of named entries with a metadata for each file/directory entry.

#### diff function
When tracker.py is called with diff argument, it compares between two snapshots of file/directory files and reports the changes between them.

### Typical usage
#### snap mode
```psj@ubuntu:~/Dev$ python tracker.py snap --path /home/psj/Dev/2017-project/ --snap-filename snap.json```

#### diff mode
```psj@ubuntu:~/Dev$ python tracker.py diff snap.json snap1.json```
DEBUG:__main__:Executing diff function between snap.json and snap1.json to find out file/directory changes
INFO:__main__:Entry - /home/psj/Dev/2017-project/test.txt is removed.

The script can run on both python 2 and python 3.
### Python required libraries
* json
* argparse

If these are not presen on your machine, install them using python package managers - pip or easy_install.
``` 
$ pip install json
$ pip install argparse
```


