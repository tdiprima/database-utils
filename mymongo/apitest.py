# Contains tests for the pathdbapi library, particularly the functions get_auth_token and get_slide_unique_id,
# including handling for certain exceptions and command line input.
# TESTING PATHDB API (OLD!)
from pathdbapi import *
import sys


def test1():
    try:
        url = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
    except IndexError as error:
        # Output expected IndexErrors.
        print('Required: url username password')
        exit(1)
    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception, False)
        exit(1)

    token = get_auth_token(url, username, password)
    print(token)

    id = get_slide_unique_id(token, url, 'TCGA BRCA DEMO', 'TCGA-BRCA', 'TCGA-A2-A3XZ', 'A3XZ-01Z-00-DX1')
    print(id)

    raise MyException('TESTING MyException')


def test2():
    token = get_auth_token(sys.argv[1], sys.argv[2], sys.argv[3])
    print(token)

    id = get_slide_unique_id(token, sys.argv[1], "TCGA BRCA DEMO", "TCGA-BRCA", "TCGA-A2-A3XZ", "A3XZ-01Z-00-DX1")
    print(id)


def test3():
    raise MyException("My hovercraft is full of eels")
