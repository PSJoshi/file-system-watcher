#!/usr/bin/env python
import os
from datetime import datetime
import json
import argparse
import logging
import sys
from pprint import pprint

# setup logging
logging.basicConfig(stream=sys.stdout,level = logging.DEBUG)
logger = logging.getLogger(__name__)

def save_snap(snap_dict,snap_file):

    try:

        with open(snap_file, 'w') as out_file:
            json.dump(snap_dict, out_file, indent=4)

        logger.info("Snapshot is saved to %s successfully." %snap_file)

    except Exception as exc:
        logger.error("Error while saving snapshot to file %s - %s" % (snap_file,exc.message), exc_info=True)

def open_snapshot_file(snap_file):
    json_results = None
    try:
        with open(snap_file, 'r') as f:
            json_results = json.load(f)
    except Exception as exc:
        logger.error("Error while opening snap file %s - %s" % (args.snap1, exc.message),exc_info=True)
        sys.exit(1)
    return json_results
 
def file_exists(file_name):
    pass

def snap(args):

    logger.debug("Executing Snap for path: %s" %args.path)
    
    if not os.path.exists(args.path):
        logger.error("The path of snap directory %s is not valid. Kindly re-enter valid path" % args.path) 
        sys.exit(1)
    if not os.path.isdir(args.path):
        logger.error("The snap directory %s does not exits. Kindly re-enter valid directory" % args.path) 
        sys.exit(1)

    # snap_file
    snap_file = args.snap_filename

    # ensure path is absolute path
    abs_path = os.path.abspath(args.path)

    snapshot_dict = {
        'path': abs_path,
        'snap_date': datetime.now().isoformat(),
        'entries': dict()
    }

    try:
        for root, dirs, files in os.walk(abs_path):
            try: 
                # loop through files
                for name in files:
                    file_path = os.path.join(root,name)
                    logger.debug("File path: %s " %file_path)
                    file_creation_date = os.stat(file_path).st_ctime 
                    #logger.debug("File - %s , Creation time - %s" %(file_path, os.stat(file_path).st_ctime))
                    logger.debug("File - %s , Creation time - %s"%(file_path, datetime.fromtimestamp(file_creation_date))) 
                    snapshot_dict["entries"][file_path] = {'mtime': os.stat(file_path).st_mtime, 'type': 'file'}
            except Exception as exc:
                logger.error("Error while capturing file %s snap - %s" % (file_path,exc.message), exc_info=True)

            try:
                for name in dirs:
                    dir_path = os.path.join(root,name)
                    logger.debug("Directory path: %s" %dir_path)
                    dir_creation_date = os.stat(dir_path).st_ctime 
                    #logger.debug("Directory - %s , Creation time - %s" %(dir_path, creation_date))
                    logger.debug("Directory - %s , Creation time - %s" %(dir_path, datetime.fromtimestamp(dir_creation_date)))
                    snapshot_dict["entries"][dir_path] = {'mtime': os.stat(dir_path).st_mtime, 'type': 'directory'}
            except Exception as exc:
                logger.error("Error while capturing directory %s snap - %s" % (dir_path, exc.message), exc_info=True)


    except Exception as exc:
        logger.error("Error while capturing file/directory snap - %s" %exc.message,exc_info=True)

    #pprint(snapshot_dict)
    logger.debug("Snap dictionary: %s" %snapshot_dict)
    save_snap(snapshot_dict,snap_file) 


def diff(args):

    logger.debug("Executing diff function between %s and %s"
                 " to find out file/directory changes" %(args.snap1,args.snap2))

    if not os.path.exists(args.snap1):
        logger.error("Snap file %s does not exists" %args.snap1)
        sys.exit(1)

    if not os.path.exists(args.snap2):
        logger.error("Snap file %s does not exists" %args.snap2)
        sys.exit(1) 


    # read snap files
    json_data = open_snapshot_file(args.snap1)
    if json_data:
        snap1_json = json_data

    json_data = open_snapshot_file(args.snap2)
    if json_data:
        snap2_json = json_data

    modified_entries = list()
    removed_entries = list()
    added_entries = list()
     # check paths
    if snap1_json['path'] != snap2_json['path']:
        logger.error("Snap file paths %s and %s do not match." 
                     %(snap1_json['path'],snap2_json['path']))
        sys.exit(1)

    # check individual entries 
    for entry in snap1_json['entries']:
        if entry not in snap2_json['entries']:
            removed_entries.append("Entry - %s is removed." % entry)

        elif snap1_json['entries'][entry] != snap2_json['entries'][entry]:
            modified_entries.append("Entry - %s is modified." % entry) 
      
    for entry in snap2_json['entries']:
        if entry not in snap1_json['entries']:
            added_entries.append("Entry - %s is added." % entry)

    # merge lists
    comparison_results = added_entries + modified_entries + removed_entries

    # list the differences
    if comparison_results:
        for entry in comparison_results:
            logger.info(entry)
    else:
        logger.info("The snapshots %s and %s are identical." % (args.snap1,args.snap2))
   
def cmd_arguments():

    try:
        parser = argparse.ArgumentParser("This script can be used to keep track"
                                         " of file/directory changes in a given directory"
                                         " and it reports differences between two snap shots.")

        #subparsers = parser.add_subparsers(dest='action')
        subparsers = parser.add_subparsers()
        subparsers.required = True

        # snap subparser 
        parser_snap = subparsers.add_parser('snap', help='saves the state of directory as a json file')
        parser_snap.add_argument('--path', required=True, help='Full path of monitoring directory',dest='path')
        parser_snap.add_argument('--snap-filename', required=True, help="snapshot file name",dest='snap_filename')
        parser_snap.set_defaults(func=snap)

        # diff subparser
        parser_diff = subparsers.add_parser('diff', help='compare two snapshots of monitoring directory and report any changes')
        parser_diff.add_argument('snap1', help='Path to the first snapshot '
                                           ' that was created using the snap command')
        parser_diff.add_argument('snap2', help='Path to the second snapshot '
                                           ' that was created using the snap command')
        parser_diff.set_defaults(func=diff)

        args = parser.parse_args()

        # extract argument details for debugging
        args_details = vars(parser.parse_args())
        if args_details.has_key('path'):
            logger.debug("path:%s snap file:%s" %(args.path, args.snap_filename))
        elif args_details.has_key('snap1') and args_details.has_key('snap2'):
            logger.debug("snap1:%s snap2:%s" %(args.snap1, args.snap2))
    
        args.func(args)

    except Exception as exc:
        logger.error("Error while getting and parsing command line arguments - %s" %exc.message,exc_info=True)

if __name__ == "__main__":
    try:
    
        cmd_args = cmd_arguments()
    
    except Exception as exc:
        logger.error("Error while running file/directory tracker script - %s" %exc.message,exc_info=True)


