import csv
import string
from pymarc import MARCReader, Record, Field
import pymarc
from fuzzywuzzy import fuzz
"""
Script starts with cleaning urls so they match (release URL edited back to just to artist URL) to check for direct match, and when they do it does a little fuzzy match on title.
"""

with open('match_results.csv', 'wt',  encoding='utf-8-sig', newline = '') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter = ",")

#need to update filename and rows
    with open("bandcampdata.csv", "rt", encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=",")
        count = 0
        for row in reader:
            """to align with bandcamp title file metadata"""
            bcid = row[0]
            bctitle = row[2]
            bcurl = row[3].split('//')[1]
            count = count + 1
            print("record no. " + str(count) + " looking for matches ... " + bcurl)

    #start with just bandcamp set (short records and fulll recieved and catalogued), then full set of digital.

            with open ('music_records_with_bandcamp_urls.mrc', 'rb') as file:
                nznbbibfile = MARCReader(file, to_unicode=True, force_utf8=True,)
                # loop through match file
                for record in nznbbibfile:
                    mms = record['001'].value()
                    #year = r008.value()[7:11]

                    #if not year == cvlyear:
                    #    continue

                    r856s = record.get_fields('856')
                    for r856 in r856s:
                        Bandcampurl = record['856']['u']
                        if 'bandcamp' not in Bandcampurl:
                            #print('no bandcamp in url: ', mms)
                            continue
                        #print(Bandcampurl)
                        try:
                            Bandcampurl_first = Bandcampurl.split('//')[1]
                            Bandcampurl_first = Bandcampurl_first.split('/')[0]
                            #print(Bandcampurl_first)
                        except:
                            Bandcampurl_first = Bandcampurl_first.split('/')[0]
                            #print(Bandcampurl_first)
 
                        if Bandcampurl_first == bcurl:
                            #print('Success')
                                                                               
                            title = record['245']['a']
                            #need to strip final punctuation

                        #fuzztitle = fuzz.token_set_ratio(str(title), str(cvltitle))
                            fuzztitle = fuzz.ratio(str(title), str(bctitle))

                            if fuzztitle > 85:
                                print("possible success:")
                                mms = record['001'].value()
                                #check record level here?
                                print(mms)
                                spamwriter.writerow([bcurl, bctitle, mms, title, Bandcampurl])