import os
import exiftool
import csv

#The function takes fn, tit, creat, year, mms, pol_no, pid

# def csv_file_creator (folder, album_name, artist, date, track_number, track_title, comment, mime_type, MD5, file_path):

#     lst = []
#     lst.append(folder )
#     lst.append( album_name )
#     lst.append( artist )
#     lst.append( date )
#     lst.append( track_number )
#     lst.append( track_title )
#     lst.append( comment )
#     lst.append( mime_type )
#     lst.append( MD5 )
#     lst.append( file_path )
#     print(lst)
    
#     if not os.path.isfile('music_project.csv'):
#         with open( 'music_project.csv', 'a' ) as csvfile:
#             fnames = ['folder', 'album_name', 'artist', 'date', 'track_number', 'track_title', 'comment', 'mime_type', 'MD5', 'file_path']
#             writer = csv.DictWriter(csvfile, fieldnames=fnames)
#             writer.writeheader()

#     with open( 'music_project.csv', 'a' ) as csvfile:
#         writer = csv.writer( csvfile, delimiter = ',', quoting=csv.QUOTE_NONE)
#         writer.writerow(lst)

# filefolder=r
rootDir = r"Z:\NDHA\NDHA"
for dirName, subdirList, fileList in os.walk(rootDir):
        # print('Found directory: %s' % subdirList, fileList)  
    if "Staring" in os.path.join(dirName):
        for fi in os.listdir(os.path.join(dirName)):
            # print(dirt, fi)
            file_list=[]
            randoms=[]
            if fi.endswith('flac') or fi.endswith('jpg'):
                file_list =file_list+[fi]
            else:
                randoms=randoms+[fi]

            for fl in file_list:
                file_path=os.path.join(dirName,fl)
                with exiftool.ExifTool() as et:
                    metadata = et.get_metadata(file_path)
                    # print(metadata)
                    folder=et.get_tag("File:Directory", file_path).split("/")[-1]
                    album_name=et.get_tag("Vorbis:Album", file_path)
                    if not album_name:
                        album_name=""
                    artist=et.get_tag("Vorbis:Albumartist", file_path)
                    if not artist:
                        artist=""
                    date=et.get_tag("Vorbis:Date", file_path)
                    if not date:
                        date=""
                    track_title=et.get_tag("Vorbis:Title", file_path)
                    if not track_title:
                        track_title=""
                    track_number=et.get_tag("Vorbis:TrackNumber", file_path)
                    if not track_number:
                        track_number=""
                    try:
                        comment=et.get_tag("Vorbis:Comment", file_path).replace("Visit http:", "http:")
                    except:
                        pass
                    mime_type=et.get_tag("File:MIMEType", file_path)
                    MD5=et.get_tag("FLAC:MD5Signature", file_path)
                    if not MD5:
                        MD5=""
                    print(folder, album_name, artist, date, track_number, track_title, comment, mime_type, MD5, file_path)
                    # print(folder, album_name, artist, date, track_number, track_title, mime_type, MD5, file_path)
                    # csv_file_creator(folder, album_name, artist, date, track_number, track_title, comment, mime_type, MD5, file_path)

                    # with open("Exif.txt", 'a', encoding="utf-8") as f:
                    #     f.write('%s' % (metadata))  