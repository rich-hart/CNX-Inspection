#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import os

def readzip(file_path):
    with open(file_path, "rb") as fin:
        img = fin.read()
    return img




try:
    con = psycopg2.connect(database="training-data", user="qa") 
    
    cur = con.cursor()
    file_name ='college-physics-9.4.zip' 
    data = readzip(os.path.join('./data',file_name))
    binary = psycopg2.Binary(data)
    cur.execute("INSERT INTO collections( name, collection_data) VALUES ( %s, %s)", (file_name, binary) )

    con.commit()    
    
except psycopg2.DatabaseError, e:

    if con:
        con.rollback()

    print 'Error %s' % e    
    sys.exit(1)
    
finally:
    
    if con:
        con.close()   
