import csv
import string
from pymarc import MARCReader, Record, Field
import pymarc
from fuzzywuzzy import fuzz
"""
Script starts with cleaning urls so they match (release URL edited back to just to artist URL) to check for direct match, and when they do it does a little fuzzy match on title.
"""
def Matchcheck(Bandcampurl_first, bcurl):
    if Bandcampurl_first == bcurl:
        print('Success')
                                                                               
        title = record['245']['a'].rstrip('/')
        fuzztitle = fuzz.ratio(str(title), str(bctitle))

        if fuzztitle > 85:
            print("possible success:")
            mms = record['001'].value()
        #check record level here?
            print(mms)
            spamwriter.writerow([bcurl, bctitle, mms, title, Bandcampurl])


with open('match_results.csv', 'wt',  encoding='utf-8-sig', newline = '') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter = ",")

    with open("bandcamp_title_list.csv", "rt", encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=",")

        count = 0
        next(f)
        for row in reader:
            bctitle = row[0]
            try:
                bcurl = row[3].split('//')[1]
            except:
                continue
            bcid = row[7]
            count = count + 1
            print(bctitle + "record no. " + str(count) + " looking for matches ... " + bcurl)

    #start with just bandcamp set (short records and fulll recieved and catalogued), then full set of digital.

            with open ('music_records_with_bandcamp_urls.mrc', 'rb') as file:
                nznbbibfile = MARCReader(file, to_unicode=True, force_utf8=True,)
                # loop through match file
                for record in nznbbibfile:
                    mms = record['001'].value()

                    r856s = record.get_fields('856')
                    for r856 in r856s:
                        Bandcampurl = record['856']['u']
                        if 'bandcamp' not in Bandcampurl:
                            continue

                        try:
                            Bandcampurl_first = Bandcampurl.split('//')[1]
                            Bandcampurl_first = Bandcampurl_first.split('/')[0]
                            Matchcheck(Bandcampurl_first, bcurl)
                                #print("try" + Bandcampurl_first)
                        except:
                            Bandcampurl_first = Bandcampurl_first.split('/')[0]
                            Matchcheck(Bandcampurl_first, bcurl)
                            print("except" + Bandcampurl_first)
 
                            