#! /usr/bin/python3
# from extract_csv import *
from config import config
import boto3
import pandas as pd
import geopandas as gpd
from transform import *
from load_dhs import *

def extract_files():
    # create S3 resource
    s3 = boto3.resource('s3')
    
    # specify bucket name and file names
    bucket_name = 'ds-interview-sandbox'
    file_names = [
        'shared/data_dictionary.csv',
        'shared/ug_clusters.csv',
        'shared/uga_dhs_2016.csv',
        'shared/uga_regions.geojson'
    ]
    
    s3=boto3.client('s3')    
# create pandas and geopandas dataframes from S3 files
    
    data_dict_df = pd.read_csv(f's3://{bucket_name}/{file_names[0]}')
    
    clusters_df = pd.read_csv(f's3://{bucket_name}/{file_names[1]}')
    #print(clusters_df.head())
    dhs_df = pd.read_csv(f's3://{bucket_name}/{file_names[2]}')
    regions_gdf = gpd.read_file(f's3://{bucket_name}/{file_names[3]}')
    #regions_df = regions_gdf.drop(columns='geometry')
    
    # print dataframes to check the data
    print(data_dict_df)
    #print(clusters_df.head())
    #print(dhs_df.head())
    #print(regions_df.head())
    return data_dict_df,clusters_df, dhs_df,regions_gdf
    

if __name__ == "__main__":
    db_config = config(section="postgresql")
    dict_df,clusters_df,dhs_df,regions_gdf=extract_files()
    
    # Transform Dataframes
    #dict_df, clusters_df, dhs_df = transform_pd_data(dict_df, clusters_df, dhs_df)
    dhs_data=clean_dhs_data(dhs_df)
    
    regions_gdf = transform_gpd_data(regions_gdf)    

    # Load transformed data into Postgres Database for Querying
    #load_ldata_to_postgres(dict_df,clusters_df,dhs_data,regions_gdf,db_config)    
    load_dhs(dhs_data, db_config)
