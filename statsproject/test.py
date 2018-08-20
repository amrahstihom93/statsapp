
import csv
import pymysql
import tablib
import sys
import pandas as pd
from pymongo import MongoClient
import json

conn = pymysql.connect(host='127.0.0.1',
                       port = 3306,
                       database='test',
                       user='root',
                       password='')
print(conn)