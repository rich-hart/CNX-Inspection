#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import subprocess
import sys
import os
from os import listdir
from os.path import isfile, join, abspath, dirname

here = abspath(dirname(__file__))
DATA_DIR = 'data'
TRAINING_DATA_DIR =join(here, 'data')

settings = { 'python-exe': 'python',
             'oer-exports-path': '/home/vagrant/production/oer.exports',
             'print-style': 'ccap-physics',
             'prince-path': '/usr/bin/prince',
             'collection-dir': '/home/vagrant/development/CNX-Inspection/data',
             'output-dir': '/home/vagrant/development/CNX-Inspection/data',
             'git-hash':'7a0bcc69ce90b5cb15666184c4bd3dde26959aef',
             'collection-name': 'col11287_1.1_complete',
             }

def read_binary(file_path):
    with open(file_path, "rb") as fin:
        img = fin.read()
    return img

with psycopg2.connect(database="training-data", user="qa") as con:
    with con.cursor() as cur:
    
        zipfiles = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f)) and '.zip' in f]
    
        for file_name in zipfiles:
            settings['collection-name'] = file_name.replace(".zip","")
#            data = read_binary(join(DATA_DIR,file_name))
#            binary = psycopg2.Binary(data)
    
            command = "unzip {collection-dir}/{collection-name}.zip".format(**settings)
    
            p=subprocess.Popen(command.split(),cwd=settings['collection-dir'])
    
            p.wait()

            col_metadata_path = join(settings['collection-dir'],
                                     settings['collection-name'],
                                     'collection.xml')
            from lxml import etree
            from StringIO import StringIO

            NAMESPACES = {
                'cnx':"http://cnx.rice.edu/cnxml",
                'cnxorg':"http://cnx.rice.edu/system-info",
                'md':"http://cnx.rice.edu/mdml",
                'col':"http://cnx.rice.edu/collxml",
                'cnxml':"http://cnx.rice.edu/cnxml",
                'm':"http://www.w3.org/1998/Math/MathML",
                'q':"http://cnx.rice.edu/qml/1.0",
                'xhtml':"http://www.w3.org/1999/xhtml",
                'bib':"http://bibtexml.sf.net/",
                'cc':"http://web.resource.org/cc/",
                'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                'lang':"en",
            }
            with open(col_metadata_path) as f:
                parser = etree.XMLParser(recover=True)
                tree = etree.parse(StringIO(f.read()), parser)
                settings['collection-version']=tree.xpath('//md:version',namespaces=NAMESPACES)[0].text
                settings['collection-title']=tree.xpath('//md:title',namespaces=NAMESPACES)[0].text 

             
            data = read_binary(join(settings['collection-dir'], 
                                    settings['collection-name']+'.zip'))
    
            binary = psycopg2.Binary(data)
    
            cur.execute("INSERT INTO collections (title, name, version, zip) "\
                        "VALUES (%s,%s,%s,%s)", (settings['collection-title'],
                                                 settings['collection-name'],
                                                 settings['collection-version'],
                                                 binary,))
    
            con.commit()

 
            command     =  "git checkout {git-hash}".format(**settings)
    
            p=subprocess.Popen(command.split(),cwd=settings['oer-exports-path'])
    
            p.wait()
    
            command = "{python-exe} {oer-exports-path}/collectiondbk2pdf.py "\
                      "-p {prince-path} "\
                      "-d {collection-dir}/{collection-name} "\
                      "-s {print-style} "\
                      "{output-dir}/{collection-name}.pdf".format(**settings)
    
            p=subprocess.Popen(command.split(),cwd=settings['oer-exports-path'])
    
            p.wait()
    
            data = read_binary(join(settings['collection-dir'], 
                                    settings['collection-name']+'.pdf'))
    
            binary = psycopg2.Binary(data)
    
            cur.execute("INSERT INTO pdfs (git_commit, style, pdf) "\
                        "VALUES (%s,%s,%s)", (settings['git-hash'],
                                                 settings['print-style'],
                                                 binary))
    
            cur.execute("SELECT id FROM collections ORDER BY id DESC LIMIT 1")
    
            collection_id = cur.fetchone()[0]
    
            cur.execute("SELECT id FROM pdfs ORDER BY id DESC LIMIT 1")
    
            pdf_id = cur.fetchone()[0]
    
            cur.execute("INSERT INTO collections_pdfs( collection, pdf) VALUES (%s,%s)",(collection_id, pdf_id))

            con.commit()
     
