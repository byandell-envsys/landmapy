# -*- coding: utf-8 -*-
"""USGS Water Data Access

This module provides functions to access and visualize data from the USGS Water Data initiative.
"""

import dataretrieval.nwis as nwis
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import hvplot.pandas  # This activates .hvplot() on DataFrames
import holoviews as hv
from IPython.display import display

# Initialize HoloViews extension for Bokeh
try:
    hv.extension('bokeh')
except Exception:
    # Fallback or ignore if not in an environment that supports it
    pass

def get_usgs_data(site_id="06446000", site_name="White River near Oglala, SD", 
                  latitude=43.2548611, longitude=-102.8268889,
                  parameters=["00065", "00060"], 
                  start_date="1990-10-01", end_date="2026-02-03",
                  plot_map=True, plot_series=True):
    """
    Fetch and process data from a USGS gaging station.
    
    Args:
        site_id (str): USGS site number.
        site_name (str): Name of the site for labeling.
        latitude (float): Latitude of the station.
        longitude (float): Longitude of the station.
        parameters (list): USGS parameter codes (e.g., ["00065", "00060"]).
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        plot_map (bool): Whether to display an interactive map.
        plot_series (bool): Whether to display a time-series plot.
        
    Returns:
        pd.DataFrame: Daily resampled mean of the first parameter (usually discharge).
    """
    
    # Coordinates for USGS station
    data = {
        "Site": [site_id],
        "Name": [site_name],
        "Latitude": [latitude],
        "Longitude": [longitude]
    }

    # Create df and gdf
    df_meta = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(
        df_meta,
        geometry=gpd.points_from_xy(df_meta["Longitude"], df_meta["Latitude"]),
        crs="EPSG:4326"
    )

    if plot_map:
        # Plot with aerial basemap
        full_title = f"USGS Gaging Station: {site_name} ({site_id})"
        map_plot = gdf.hvplot(
            geo=True,
            tiles="EsriImagery",
            kind="points",
            size=100,
            color="blue",
            hover_cols=["Name", "Site"],
            width=800,
            height=500,
            title=full_title,
            # Semi-zoom around the point
            xlim=(longitude - 0.05, longitude + 0.05),
            ylim=(latitude - 0.05, latitude + 0.05)
        )
        # Display the map in notebook environments
        display(map_plot)

    # Create df using data from USGS
    df = nwis.get_record(sites=site_id, parameterCd=parameters, start=start_date, end=end_date)
    
    # Remove missing values (NaN, -999999.0)
    df = df.replace(-999999, np.nan)
    
    if plot_series:
        # Determine the primary parameter code (usually discharge 00060 or gage height 00065)
        main_param = "00060" if "00060" in parameters else parameters[0]
        
        series_plot = df.hvplot(
            y=main_param,
            width=800,
            height=400,
            title=f"USGS Data: {site_name} ({site_id})",
            ylabel=f"Value ({main_param})",
            xlabel="Date"
        )
        display(series_plot)

    df.index = pd.to_datetime(df.index)
    
    # Resample to daily mean of the primary parameter (e.g. Discharge 00060)
    # If 00060 is in parameters, use it, otherwise use the first one.
    target_param = "00060" if "00060" in parameters else parameters[0]
    
    df_daily = (
        df[target_param]
        .resample("D")
        .mean()
    )

    return df_daily

def find_usgs_site(site_name, state_code):
    """
    Find USGS site information by station name and state code.
    
    Args:
        site_name (str): Partial or full name of the station to search for.
        state_code (str): Two-letter state code (e.g., "SD", "WI").
        
    Returns:
        pd.DataFrame: DataFrame containing site_id, station_nm, lat, and lon.
    """
    # Fetch all sites in the given state
    df, meta = nwis.what_sites(stateCd=state_code)
    
    if df.empty:
        return pd.DataFrame()
    
    # Filter by name (case-insensitive)
    mask = df['station_nm'].str.contains(site_name, case=False, na=False)
    filtered_df = df[mask].copy()
    
    # Keep only relevant columns
    cols = ['site_no', 'station_nm', 'dec_lat_va', 'dec_long_va']
    # Filter columns that exist
    available_cols = [c for c in cols if c in filtered_df.columns]
    
    return filtered_df[available_cols]

def get_site_metadata(site_id):
    """
    Retrieve available parameters and period of record for a USGS site.
    
    Args:
        site_id (str): USGS site number.
        
    Returns:
        dict: Metadata containing site_id, parameters, start_date, and end_date.
    """
    # Fetch site series catalog
    df, meta = nwis.get_info(sites=site_id, seriesCatalogOutput=True)
    
    if df.empty:
        return {
            "site_id": site_id,
            "parameters": [],
            "start_date": None,
            "end_date": None
        }
    
    # Filter for daily values ('dv')
    df_dv = df[df['data_type_cd'] == 'dv'].copy()
    
    if df_dv.empty:
        # Fallback to all series if no 'dv' found, or handle as empty
        params = []
        start = None
        end = None
    else:
        # Get unique parameter codes, dropping NaNs
        params = df_dv['parm_cd'].dropna().unique().tolist()
        
        # Determine overall period of record for daily values
        # Convert to datetime to find min/max
        df_dv['begin_date'] = pd.to_datetime(df_dv['begin_date'])
        df_dv['end_date'] = pd.to_datetime(df_dv['end_date'])
        
        start = df_dv['begin_date'].min().strftime('%Y-%m-%d')
        end = df_dv['end_date'].max().strftime('%Y-%m-%d')
    
    return {
        "site_id": site_id,
        "parameters": params,
        "start_date": start,
        "end_date": end
    }

if __name__ == "__main__":
    # Example 1: Original usage
    result = get_usgs_data(plot_map=False, plot_series=False)
    print("Daily data head:")
    print(result.head())
    
    # Example 2: Finding a site by name
    print("\nSearching for 'White River' in SD:")
    sites = find_usgs_site("White River", "SD")
    print(sites.head())
    
    # Example 3: Fetching site metadata
    print("\nFetching metadata for 06446000:")
    meta = get_site_metadata("06446000")
    print(meta)