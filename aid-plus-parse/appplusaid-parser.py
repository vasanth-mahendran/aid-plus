import os
import math
import csv
import pymongo
import xml.sax
from os import listdir
from os.path import isfile, join
import time

start_time = time.time()
from pymongo.errors import BulkWriteError

from saxndfparse import NdfParse
from pymongo import MongoClient
csv.register_dialect('pipes', delimiter='|')
csv.register_dialect('dollar', delimiter='$')

root = '/Users/vasanthmahendran/Documents/study/2016-spring/5320-se/project/SPECIAL SE/'

class appplusaid_parser:
    #MONGO_PORT = 27017
    MONGO_PORT = 3001
    MONGO_HOST = 'localhost'
    db_client = MongoClient(MONGO_HOST, MONGO_PORT)
    #drug_db = db_client.drug_db
    drug_db = db_client.meteor
    drug_fed_collection = drug_db.drug_fed
    demo_fed_collection = drug_db.demo_fed
    report_src_collection = drug_db.report_src_fed
    indi_drug_fed_collection = drug_db.indi_drug_fed
    reac_out_ind_fed_collection = drug_db.reac_out_ind_fed
    therapy_fed_collection = drug_db.therapy_fed
    out_c_fed_collection = drug_db.out_c_fed
    rx_terms_fed_collection = drug_db.rx_terms_fed
    rx_terms_ing_fed_collection = drug_db.rx_terms_ing_fed

    def __init__(self):
        self.parsedir(root)

    def parsedir(self,folder):
        for file in listdir(folder):
            if isfile(join(folder, file)):
                if file.endswith(".txt"):
                    print("--------", file, "-----------")
                    self.parsetxtfile(join(folder, file), self.choosedialect(file))
                if file.endswith(".xml"):
                    print("--------", file, "-----------")
                    self.parsexmlfile(join(folder, file), self.choosedialect(file))
            else:
                self.parsedir(join(folder, file))

    def parsetxtfile(self,filepath,dialect):
        file = open(filepath, "r")
        try:
            reader = csv.DictReader(file, fieldnames=None, restkey=None, restval=None, dialect=dialect)
            keys = self.getkeys(filepath)

            if("DRUG" in filepath):
                bulk = self.drug_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    insert_dict = dict((k, row[k]) for k in keys)
                    bulk.insert(insert_dict)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- DRUG: %s minutes ---" % round(((time.time() - start_time) / 60), 2))

            elif ("DEMO" in filepath):
                bulk = self.demo_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    insert_dict = dict((k, row[k]) for k in keys)
                    bulk.insert(insert_dict)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- DEMO: %s minutes ---" % round(((time.time() - start_time) / 60), 2))

            elif ("RxTermsIngredients" in filepath):
                bulk = self.rx_terms_ing_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    insert_dict = dict((k, row[k]) for k in keys)
                    bulk.insert(insert_dict)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- RXTERM ING: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("RxTerms" in filepath):
                bulk = self.rx_terms_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    insert_dict = dict((k, row[k]) for k in keys)
                    bulk.insert(insert_dict)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- RXTERM: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("THER" in filepath):
                bulk = self.therapy_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    bulk.insert(row)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- THER: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("INDI" in filepath):
                bulk = self.indi_drug_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    bulk.insert(row)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- INDI: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("REAC" in filepath):
                bulk = self.reac_out_ind_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    bulk.insert(row)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- REAC: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("RPSR" in filepath):
                bulk = self.report_src_collection.initialize_ordered_bulk_op()
                for row in reader:
                    bulk.insert(row)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- RSPR: %s minutes ---" % round(((time.time() - start_time) / 60), 2))
            elif ("OUTC" in filepath):
                bulk = self.out_c_fed_collection.initialize_ordered_bulk_op()
                for row in reader:
                    bulk.insert(row)
                try:
                    bulk.execute()
                except BulkWriteError as bwe:
                    print(bwe.details)
                print("--- OUTC : %s minutes ---" % round(((time.time() - start_time) / 60), 2))
        finally:
            file.close()

    def parsexmlfile(self, filepath, dialect):
        file = open(filepath, "r")
        try:
            xml.sax.parse(file, NdfParse())
        finally:
            file.close()

    def choosedialect(self,file):
        if "DEMO" in file or "DRUG" in file or "INDI" in file or "OUTC" in file or "REAC" in file or "RPSR" in file or "THER" in file:
            return "dollar"
        elif "RxTerms" in file:
            return "pipes"
        else:
            return"excel-tab"

    def getkeys(self,filename):
        if('DRUG' in filename):
            return ['primaryid','caseid','drug_seq','role_cod','drugname','val_vbm','route','dose_vbm',
                    'cum_dose_chr','cum_dose_unit','lot_num','exp_dt','dose_amt','dose_unit','dose_form','dose_freq']
        elif ('DEMO' in filename):
            return ['primaryid','caseid','caseversion','i_f_code','event_dt','mfr_dt','rept_cod','mfr_num','mfr_sndr',
                    'age','age_cod','age_grp','sex','e_sub','wt','wt_cod','rept_dt','occp_cod','occr_country']
        elif ('RxTermsIngredients' in filename):
            return ['RXCUI','INGREDIENT','ING_RXCUI']
        elif ('RxTerms' in filename):
            return ['RXCUI','GENERIC_RXCUI','TTY','FULL_NAME','RXN_DOSE_FORM','BRAND_NAME','DISPLAY_NAME','ROUTE',
                    'NEW_DOSE_FORM','STRENGTH']

app_parser = appplusaid_parser()