#!/usr/bin/env python

"""
A simple python script.

"""

import sys

from pymongo import MongoClient


def main(arguments):
    client = MongoClient('mongodb://localhost:27017')
    db = client['camic']
    docs = db.analysis
    my_docs = docs.find({"image.imageid": "AALI-01Z-00-DX1", "analysis.execution_id": "CNN_synthetic_n_real"})
    # print("{ field: { $in: [<value1>, <value2>, ... <valueN> ] } }")
    print(my_docs)
    # db.mark.createIndex( { "provenance.image.imageid" : 1 }, {background: true}  );


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
