import geopandas as gpd
import pandas as pd

def clean_data_dictionary(data_dict):
    """Clean up column names in the data dictionary"""
    data_dict.columns = ["Variable", "Label"]
    return data_dict


def clean_cluster_data(cluster_data):
    """Remove whitespace from column names in the clusters data, and convert region code to integer"""
    cluster_data.columns = cluster_data.columns.str.strip()
    #cluster_data["region"] = pd.to_numeric(cluster_data["region"], errors="coerce")
    return cluster_data


def clean_dhs_data(df):
    # 1. Transform v535 into boolean and remove all NaN
    df = df.dropna(subset=['v535'])
    df['v535'] = df['v535'].astype(bool)

    # 2. Transform adult_radio_regular into boolean
    df['adult_radio_regular'] = df['adult_radio_regular'].astype(bool)

    # 3. Transform v751 into boolean
    df['v751'] = df['v751'].astype(bool)
    return df


def clean_regions_data(regions_data):
    """Convert geojson data to 4326 CRS and clean column names"""

    # regions_data = gpd.GeoDataFrame.from_features(regions_data["features"])

    """
    regions_data = regions_data[["ISO_CODE", "NAME", "ISO2_CODE", "AREA_TYPE", "geometry"]]  # Select specific columns
    regions_data.columns = ["iso_code", "name", "iso2_code", "area_type", "geom"]  # Rename the columns
    regions_data = regions_data.to_crs(epsg=4326)  # transform the geometry column to the EPSG 4326 coordinate reference system.
    """
    return regions_data


def transform_pd_data(dict_df, clusters_df, dhs_df):
    """Transform the extracted data"""
    dict_df = clean_data_dictionary(dict_df)
    clusters_df=clean_cluster_data(clusters_df)
    dhs_df=clean_dhs_data(dhs_df)
    return dict_df, clusters_df, dhs_df

def transform_gpd_data(regions_gdf):
    # Extract the data we want and rename the columns

    regions_data = regions_gdf[['geometry', 'iso_code', 'name', 'iso2_code', 'area_type']]

    #regions_data.columns = ['geom', 'iso_code', 'name', 'iso2_code', 'area_type']
    

    # Drop rows with null or missing values
    regions_data = regions_data.dropna()

    # Convert string columns to categorical data types
    regions_data["iso_code"] = regions_data["iso_code"].astype("category")
    regions_data["name"] = regions_data["name"].astype("category")
    regions_data["iso2_code"] = regions_data["iso2_code"].astype("category")
    regions_data["area_type"] = regions_data["area_type"].astype("category")

    # Clean the geometry data, ensuring it's in EPSG:4326 format
    # regions_gdf.set_geometry("geometry")
    # regions_data["geom"] = regions_data.to_crs(epsg=4326)

    # Return the cleaned data as a GeoDataFrame
    return gpd.GeoDataFrame(regions_data)
    #return gpd.GeoDataFrame(regions_gdf)
