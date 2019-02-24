# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 20:45:19 2017

@author: Micah
"""
## .condarc file location
## C:\Users\Micah

import pandas as pd
dir_loc = 'C:/Users/Micah/project_realestate/'
postgres_key = pd.read_csv(dir_loc +'postgres_conn_cred.txt').to_dict(orient='records')[0]

# =============================================================================
# Create Schema
# =============================================================================
## Database Credentials 


from sqlalchemy import MetaData , create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

## Establishes a DBAPI connection.
db_connect_str = URL(**postgres_key)
engine =create_engine(db_connect_str)








from datetime import datetime
from sqlalchemy import DateTime
Base = declarative_base()

class Houses(Base):
    __tablename__= 'table_houses'
    house_id = Column(Integer(), primary_key=True)
    description_id = Column(Integer(), ForeignKey('table_descriptions.description_id')) #3
    location_id = Column(Integer(), ForeignKey('table_locations.location_id')) #3
    
    ## Define relationships
    description = relationship('Description', foreign_keys=[description_id])
    location = relationship('Location', foreign_keys=[location_id])
    
    street_address = Column(String(600), nullable=False, unique=True,index=True) # 1
    latitude = Column(Numeric())
    longitude = Column(Numeric())
        
    price = Column(Numeric(), index=True) # 1
    price_per_sqf = Column(Numeric())    
    property_tax = Column(Numeric())               
    home_insurance = Column(Numeric())        
    num_bedrooms = Column(Integer())               
    num_bathrooms = Column(Numeric())                        
    prop_sqft = Column(Numeric())               
    lot_size = Column(Numeric())
    house_style = Column(String(50))
    heat_fuel = Column(String(50))               
    basement = Column(String(50))               
    parking = Column(String(50))               
    year_built = Column(Integer())    
    url = Column(String(200))


class History(Base):
    __tablename__ = 'table_history'
    history_id = Column(Integer(), primary_key=True)
    house_id = Column(Integer(), ForeignKey('table_houses.house_id')) #3                 
    location_id = Column(Integer(), ForeignKey('table_locations.location_id')), #3                    
    description_id = Column(Integer(), ForeignKey('table_descriptions.description_id')) #3
    
    ## Relationships
    description = relationship('Description', foreign_keys=[description_id])
    location = relationship('Location', foreign_keys=[location_id])
    house = relationship('Houses', foreign_keys=[house_id])
    
    ## Identify the rest of the fields being used    
    date_scraped =  Column(DateTime(), index=True, nullable=False) # 1                   
    date_updated = Column(DateTime(), default=datetime.now, onupdate=datetime.now,index=True) # 2
    days_on_realtor = Column(Integer(), index=True) # 1
    spider = Column(String(20))
    project = Column(String(20))
    server = Column(String(20))
    
class Description(Base):
    __tablename__ = 'table_descriptions'       
    description_id =  Column(Integer(), primary_key=True)
    house_id = Column(Integer(), ForeignKey('table_houses.house_id')) #3
    location_id = Column(Integer(), ForeignKey('table_locations.location_id')) #3
    
    ## Relationships    
    
    location = relationship('Location', foreign_keys=[location_id])
    house = relationship('Houses', foreign_keys=[house_id])
    
    description = Column(String(1000))
               
class Location(Base):
    __tablename__ = 'table_locations'       
    location_id = Column(Integer(), primary_key=True)                                       
    description_id =  Column(Integer(), ForeignKey('table_descriptions.description_id')) #3
    house_id = Column(Integer(), ForeignKey('table_houses.house_id')) #3               
    
    # Relationships
    description = relationship('Description', foreign_keys=[description_id])    
    house = relationship('Houses', foreign_keys=[house_id])
    
    
    neighborhood = Column(String(50), index=True) # 1                                            
    postal_code = Column(String(9), index=True) # 1                                            
    city = Column(String(50))
    state = Column(String(2))
               


### Persisting the database
    
Base.metadata.create_all(engine)
# =============================================================================
# Notes    
# =============================================================================
# 1 = Index of fields to speed up queries
# 2 = Resets this column to the current date every time any part of the record 
# is updated. By using the callabe, instead of the function, we get the time that 
# each indivudal record is instatiated
#3 = Utilization of a string to connect to other objects
