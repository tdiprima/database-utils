# Reads image data from a CSV file, connects to a MongoDB database to query, print, check, rename specific fields on
# data entries, or remove documents based on the image data, and use 'pathdbapi' and 'quipdb' libraries to handle image files.
# TODO: get_auth_token url, username, password

import csv

from quipdb import *

from pathdbapi import *

# Global vars
img = {"study": "", "subject": "", "image": ""}

MARK = 'mark'
ANALYSIS = 'analysis'

# Args
execution_id = "CNN_synthetic_n_real"
file_location = "/data/segmentation_results/manifest.csv"
collection = "TCGABRCA"

# Mongo vars
myclient = connect("ca-mongo", 27017)
mydb = myclient["camic"]

# Pathdb vars
url = "http://example"
token = get_auth_token(url, "username", "password")


def do_removal(mycol, myquery):
    print("*** Removing docs in " + mycol.name + "... ***")
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to remove', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
        mydocs = mycol.find(myquery)
        for x in mydocs:
            ret_val = 0
            if mycol.name == ANALYSIS:
                ret_val = check_it(x['image'])
            if mycol.name == MARK:
                ret_val = check_it(x['provenance']['image'])
            if ret_val:
                mycol.delete_one({"_id": x['_id']})


def do_print(mycol, myquery):
    count = mycol.count_documents(myquery)
    if count == 0:
        print('Count', mycol.name, ':', count, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
        mydocs = mycol.find(myquery)
        if mycol.name == ANALYSIS:
            for x in mydocs:
                print_it(x, x['image'])
        if mycol.name == MARK:
            for x in mydocs:
                print_it(x, x['provenance']['image'])


def print_it(doc, x):
    print(doc['_id'], x['slide'], x['imageid'], x['study'], x['subject'])
    check_it(x)


def check_it(x):
    if x['study'] != img['study'] or x['subject'] != img['subject'] or x['imageid'] != img['image']:
        print("\nSomething didn't match up")
        print(x['study'], "!=", img['study'])
        print(x['subject'], "!=", img['subject'])
        print(x['imageid'], "!=", img['image'], '\n')
        return 0
    else:
        return 1


def do_rename(mycol, myquery, val):
    print("*** Renaming execution_id in " + mycol.name + "... ***")
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to rename', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
    mydocs = mycol.find(myquery)

    if mycol.name == ANALYSIS:
        for x in mydocs:
            ret_val = check_it(x['image'])
            if ret_val:
                mycol.update_one({"_id": x['_id']}, {'$set': {'analysis.execution_id': val}}, upsert=False)

    if mycol.name == MARK:
        for x in mydocs:
            ret_val = check_it(x['provenance']['image'])
            if ret_val:
                mycol.update_one({"_id": x['_id']}, {'$set': {'provenance.analysis.execution_id': val}}, upsert=False)


def do_thing(mycol, myquery):
    print("*** do_thing " + mycol.name + "... ***")
    count = mycol.count_documents(myquery)
    if count == 0:
        print('No docs to do_thing', mycol.name, '; query:', myquery)
    else:
        print('Count', mycol.name, ':', count)
    mydocs = mycol.find(myquery)

    if mycol.name == MARK:
        for x in mydocs:
            ret_val = check_it(x['provenance']['image'])
            if ret_val:
                q = {"_id": x['_id']}, {
                    "$set": {"provenance.data_loader": "quip_csv.py", "provenance.batch_id": "mybatch",
                             "tag_id": "mytag"}}
                print(q)  # mycol.update_one({'x': 1}, {'$inc': {'x': 3}})  # mycol.update_one(q, upsert=False)


def main():
    # Read file
    with open(file_location) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count = 1
                continue
            else:
                img['study'] = row[1]
                img['subject'] = row[2]
                img['image'] = row[3]

                id = get_slide_unique_id(token, url, collection, img['study'], img['subject'], img['image'])
                print('id:', id)
                a_query = {"image.slide": id, "analysis.execution_id": execution_id}
                m_query = {"provenance.image.slide": id, "provenance.analysis.execution_id": execution_id}
                # do_removal(mydb[ANALYSIS], a_query)
                # do_removal(mydb[MARK], m_query)
                # do_print(mydb[ANALYSIS], a_query)
                # do_print(mydb[MARK], m_query)
                # do_rename(mydb[ANALYSIS], a_query, execution_id + "_mark_backup")
                # do_rename(mydb[MARK], m_query, execution_id + "_mark_backup")
                do_thing(mydb[MARK], m_query)  # https://api.mongodb.com/python/current/api/pymongo/collection.html


def do_removal1(mycol, myquery):
    mydocs = mycol.find(myquery)
    for x in mydocs:
        # Analysis:
        # print(x['_id'], x['image']['slide'], x['image']['imageid'], x['image']['study'], x['image']['subject'],
        #       x['analysis']['submit_date'])
        # Mark:
        # print(x['_id'], x['provenance']['image']['slide'], x['provenance']['image']['imageid'],
        #       x['provenance']['image']['study'], x['provenance']['image']['subject'])  # submit_date
        mycol.delete_one({"_id": x['_id']})


def main1():
    # Read file
    with open(file_location) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                # print(f'\t{row[1]} {row[2]} {row[3]}.')
                id = get_slide_unique_id(token, url, collection, row[1], row[2], row[3])
                print('id:', id)
                do_removal(mydb["analysis"], {"image.slide": id, "analysis.execution_id": execution_id})
                do_removal(mydb["mark"],
                           {"provenance.image.slide": id, "provenance.analysis.execution_id": execution_id})
                line_count += 1
        print(f'Processed {line_count} lines.')


print('DONE.')
