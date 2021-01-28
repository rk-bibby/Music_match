import os
import shutil
import json
import csv
# import humanize
import subprocess
from datetime import datetime

### root folder of the files under test
testSet_root = r"Y:\pre-deposit_prod\LD_Proj\music_working"

### paths to extractors
### verify these before starting this script - it will not work unless it can resolve each extrctor as called
path_to_exiftool = r"exiftool"

### used to set the location of logs folders - ina  subfolder called "logs"
project_root = r"Z:\NDHA\Formats\running_characteristics"

### this is the staging folder. All files are copied here before extractors are evoked. 
temp_file_folder = r"Z:\NDHA\Formats\temp"


#############
exiftool_log_root = os.path.join(project_root, "logs", "exiftool")

def call_subprocess(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        print (err)

def setup():
    if not os.path.exists(exiftool_log_root):
        os.makedirs(exiftool_log_root)
    if not os.path.exists(project_root):
        os.makedirs(project_root)
    if not os.path.exists(temp_file_folder):
        os.makedirs(temp_file_folder)

def get_files(verbose=True):
    ### starts with root folder, looks in first layer subfolder, and adds the path to every file it finds to a list
    ### if 2nd layer folders expected, this should be changed to a os.walk() operation.
    if verbose:
        now = datetime.now().strftime("%H:%M:%S")
        print (f"Getting files from {testSet_root} - {now}")
    my_files = []
    for folder in [x for x in os.listdir(testSet_root) if os.path.isdir(os.path.join(testSet_root, x))]:
        for f in [x for x in os.listdir(os.path.join(testSet_root, folder)) if os.path.isfile(os.path.join(testSet_root, folder, x))]:
            if f.endswith('flac'):
                my_files.append(os.path.join(testSet_root, folder, f))
    if verbose:
        now = datetime.now().strftime("%H:%M:%S")
        print (f"Got {len(my_files)} files from {testSet_root} - {now}")
    return my_files
   
def stage_file(infile, outfile, verbose=True):
    ### copies file from netowrk storage to local filestore
    ### the extractors don't seem to like working from the remote store, probably because of how long it takes to stream larger files to memory
    ### verbose logging shows the staging delay for file retrieval...
    if verbose:
        now = datetime.now().strftime("%H:%M:%S")
        # print (f"staging {infile} - {now} - {humanize.naturalsize(os.path.getsize(infile))}")
    shutil.copy(infile, outfile)
    if verbose:
        now = datetime.now().strftime("%H:%M:%S")
        print (f"staged {infile} - {now}")




# def csv_file_creator (album, artist, date, URL, track_number, track_title, FileName):

#     lst = []
#     lst.append(album )
#     lst.append( artist )
#     lst.append( date )
#     lst.append( URL )
#     lst.append( track_number )
#     lst.append( track_title )
#     lst.append( FileName )
#     print(lst)
    
#     if not os.path.isfile('music_list.csv'):
#         with open( 'music_list.csv', 'a' ) as csvfile:
#             fnames = ['Album', 'Artist', 'Date','URL', 'Track_number', 'Track_title', 'Filename']
#             writer = csv.DictWriter(csvfile, fieldnames=fnames)
#             writer.writeheader()

#     with open( 'music_list.csv', 'a' ) as csvfile:
#         writer = csv.writer( csvfile, delimiter = ',', quoting=csv.QUOTE_NONE)
#         writer.writerow(lst)


def parse_data(f, data_dict, outfile):
    for el in data_dict:
        album=(el['Album'])
        artist=(el['Artist'])
        date=(el['Date'])
        URL=(el['Comment']).replace("Visit http:", "http:")
        track_number=(el['TrackNumber'])
        track_title=(el['Title'])
        FileName=(el['FileName'])
        with open("music_list.txt", 'a', encoding="utf-8") as el_write:
            el_write.write('%s|%s|%s|%s|%s|%s|%s\n' % (album, artist, date, URL, track_number, track_title, FileName))

def do_exiftool(f, outfile, verbose=True): 
    # print ()
    ## evokes exiftool exe against given file, and saves resulting data in log folder
    cmd = f'{path_to_exiftool} -json "{f}" > "{outfile}"'
    call_subprocess(cmd)
    with open(outfile, "r") as read_file:
        data_dict = json.load(read_file)
        parse_data(f, data_dict, outfile)

    ## DELETE OUTFILE 


setup()
testSet = get_files()

for f in testSet:
    file_label = f.replace(testSet_root, "")[1:]
    print (f"working on {file_label}")
    __, file_id = f.rsplit(os.sep, 1)
    file_path, f_name = f.rsplit(os.sep, 1)

    ### the file_id is used to label the log foe each extractor
    ### it assumes each file is unique. It does not include the subfolder. 
    ### if youre using a complex filestore, with dup filenames, you'll need to adjust this stage.   
    file_id, __ = file_id.rsplit(".", 1)
    temp_file_name = os.path.join(temp_file_folder, f_name)

    ### this sets up the filenames / paths for each of the extractor logs per file
    # tika_logfile = os.path.join(tika_log_root, file_id+".xml")
    # mediainfo_logfile = os.path.join(media_info_log_root, file_id+".json")
    exiftool_logfile = os.path.join( exiftool_log_root, file_id+".json")
    # fits_logfile = os.path.join(fits_log_root, file_id+".xml")
    
    ### Extractors - 
    ### checks if log file has been attempted previously, skips if has log, and log file not empty. 
    ### file is only staged if any extractor is fired. 
    ### staged file is dumped after all extractors checked. 

    # if not os.path.exists(tika_logfile) or os.path.getsize(tika_logfile) == 0:
    #     if not os.path.exists(temp_file_name):
    #         stage_file(f, temp_file_name)
    #     do_tika(f, tika_logfile)

    # if not os.path.exists(mediainfo_logfile) or os.path.getsize(mediainfo_logfile) == 0:
    #     if not os.path.exists(temp_file_name):
    #         stage_file(f, temp_file_name)
    #     do_mediainfo(f, mediainfo_logfile)

    if not os.path.exists(exiftool_logfile) or os.path.getsize(exiftool_logfile) == 0:
        if not os.path.exists(temp_file_name):
            stage_file(f, temp_file_name)
        do_exiftool(temp_file_name, exiftool_logfile)

    # if not os.path.exists(fits_logfile) or os.path.getsize(fits_logfile) == 0:
    #     if not os.path.exists(temp_file_name):
    #         stage_file(f, temp_file_name)
    #     do_fits(f, fits_logfile)


    if os.path.exists(temp_file_name):
        os.remove(temp_file_name)



