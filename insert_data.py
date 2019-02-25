# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 18:53:54 2019

@author: Micah
"""

from scrapinghub import ScrapinghubClient
import pandas as pd
dir_loc = 'C:/Users/Micah/project_realestate/'
scrapy_apikey = pd.read_csv(dir_loc +'scrapy_api.txt',squeeze=True)[0]
postgres_key = pd.read_csv(dir_loc +'postgres_conn_cred.txt').to_dict(orient='records')[0]

client = ScrapinghubClient(scrapy_apikey)


### List of deployed projects
list_projects = client.projects.list()


### Getting a summary of all projects

client.projects.summary()

project = client.get_project(list_projects[0])

### Invoking a job 
spider = project.spiders.get(project.spiders.list()[0]['id'])

spider.jobs.summary()

last_key = list(spider.jobs.iter_last())[0]['key']



## Accessing job output data
### Project ID/Spider ID/Job ID
job = client.get_job(last_key)

# =============================================================================
# SQL Alchemy Connection to the database   
# =============================================================================

import sqlalchemy  as sqal
from sqlalchemy import MetaData , create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

## Establishes a DBAPI connection.
db_connect_str = URL(**postgres_key)
engine =create_engine(db_connect_str)

# reflects the schema, and produces mapping

connection=engine.connect()


# =============================================================================
# Defining the Classes
# =============================================================================

from sqlalchemy import Table, Column, Integer, Numeric, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.automap import automap_base
import sqlalchemy as sqla

Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

## Referencing the objects in the database
Houses = Base.classes.table_houses
Descriptions = Base.classes.table_descriptions
Locations = Base.classes.table_locations
History = Base.classes.table_history


Session = sessionmaker() #1 
session = Session(bind=engine) #2

#1 Defines a Session class with the bind configuration supplied by sessionmaker
#2 Creates a session for our use from our generated Session class.


# =============================================================================
# Bulk Inserts of data
# =============================================================================

### Going through the job items
results = list()
for item in job.items.iter():
    results.append(item)

df_results = pd.DataFrame(results)
df_results.head()

house_columns = list(set(df_results.columns.values) & set(list(dir(Houses))))
description_columns = list(set(df_results.columns.values) & set(list(dir(Descriptions))))
locations_columns = list(set(df_results.columns.values) & set(list(dir(Locations))))
history_columns = list(set(df_results.columns.values) & set(list(dir(History))))


list_house_to_write = df_results[house_columns].to_dict(orient='records')
list_description_to_write = df_results[description_columns].to_dict(orient='records')
list_locations_to_write = df_results[locations_columns].to_dict(orient='records')
list_history_to_write = df_results[history_columns].to_dict(orient='records')

## Bulk insert  
metadata = sqla.schema.MetaData(bind=engine, reflect=True)
table_houses = Table('table_houses', metadata, autoload=True)
table_descriptions = Table('table_descriptions', metadata, autoload=True)
table_locations = Table('table_locations', metadata, autoload=True)
table_history = Table('table_history', metadata, autoload=True)


connection=engine.connect()
connection.execute(table_houses.insert(), list_house_to_write)
connection.execute(table_descriptions.insert(), list_description_to_write)
connection.execute(table_locations.insert(), list_locations_to_write)
#connection.execute(table_history.insert(), list_history_to_write)

### Commit the changes
session.commit()
session.close()





