def create_data_dir(new_dir='habitat'):
    """
    Create Data Directory if it does not exist.

    Parameters
    ----------
    new_dir: character string
        Name of new directory
    """
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

# create_data_dir('habitat')

def soil_url_dict(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200"):
    """
    Set up soil URLs based on place.
    
    Parameters
    ----------
    place_gdf: GeoDataFrame
        GeoDataFrame of selected location
    soil_var, soil_sum, soil_depth: character string
        Name of soil variable, summary and depth

    Results
    -------
    soil_url: dict
        Dictionary of URLs
    """
    from math import floor, ceil
    
    soil_url_template = (
        "http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/"
        f"{soil_var}/"
        f"{soil_sum}/"
        f"{soil_depth}/"
        "lat{min_lat}{max_lat}_lon{min_lon}{max_lon}.tif")
    
    # soil_url_template.format(min_lat = 43, max_lat = 44, min_lon = -103, max_lon = -104)

    bounds_min_lon, bounds_min_lat, bounds_max_lon, bounds_max_lat = (place_gdf.total_bounds)

    # Initialize structure for saving image links
    url_names = []
    for min_lon in range(floor(bounds_min_lon), ceil(bounds_max_lon)):
        for min_lat in range(floor(bounds_min_lat), ceil(bounds_max_lat)):
            url_names.append(f"lon{min_lon}lat{min_lat}")

    soil_urls = {url_name: [] for url_name in url_names}
    for min_lon in range(floor(bounds_min_lon), ceil(bounds_max_lon)):
        for min_lat in range(floor(bounds_min_lat), ceil(bounds_max_lat)):
            print(min_lon, min_lat)
            soil_url = soil_url_template.format(min_lat = min_lat, max_lat = min_lat + 1,
                min_lon = min_lon, max_lon = min_lon + 1)
            soil_urls[f"lon{min_lon}lat{min_lat}"].append(soil_url)

    return soil_urls

# soil_urls = soil_url_dict(place_gdf, "sand", "mean", "100-200")

def merge_soil(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200",
               buffer = 0.1):
    """
    Merge soil data.

    Parameters
    ----------
    place_gdf: GeoDataFrame
        GeoDataFrame of selected location
    soil_var, soil_sum, soil_depth: character string
        Name of soil variable, summary and depth
    buffer: number
        Buffer around bounds of place_gdf
    Results
    -------
    soil_merged_das: DataFrame
        DataFrame with soil estimates clipped to bounds of place_gdf 
    """
    import geopandas as gpd
    import rioxarray as rxr
    from rioxarray.merge import merge_arrays # Merge rasters
    
    soil_urls = soil_url_dict(place_gdf, soil_var, soil_sum, soil_depth)
    
    #soil_das = {url_name: [] for url_name in list(soil_urls.keys())}
    soil_das = []
    for soil_key in list(soil_urls.keys()):
        soil_url = soil_urls[soil_key][0]
        print(soil_key)
        soil_da = rxr.open_rasterio(soil_url, mask_and_scale=True).squeeze()

        # Store the resulting DataArray for later
        soil_das.append(soil_da)

    print('Done.')

    # Merge all tiles
    soil_merged_das = merge_arrays(soil_das) 

    # Use bounds from place_gdf extended by buffer
    #bounds = place_gdf.to_crs(soil_merged_das.rio.crs).total_bounds
    #bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    #print(bounds)
    #soil_merged_das = soil_merged_das.rio.clip_box(*bounds)
    soil_merged_das = da_bounds(place_gdf, soil_merged_das, buffer)

    return soil_merged_das

# soil_merged_das = merge_soil(place_gdf, "sand", "mean", "100_200", 0.1)

def da_bounds(place_gdf, da, buffer = 0.1):
    """
    Clip bounds from place_gdf on da extended by buffer.

    Parameters
    ----------
    place_gdf: GeoDataFrame
        GeoDataFrame of selected location
    da: DataFrame
        DataFrame from calling routine
    buffer: number
        Buffer around bounds of place_gdf
    Results
    -------
    da: DataFrame
        DataFrame with restricted to bounds of place_gdf 
    """
    bounds = place_gdf.to_crs(da.rio.crs).total_bounds
    bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    da = da.rio.clip_box(*bounds)

    return da

# da_bounds(place_gdf, da, 0.1)


def process_maca(sites, scenarios=['pr'], climates=['rcp85', 'rcp45'], years = [2026],
                 buffer = 0.1):
    """
    Process MACA Monthly Data.

    Parameters
    ----------
    sites: dict of GeoDataFrames
       dictionary with GeoDataFrames
    scenarios: character string
        'pr' = precipitation
    climates: character string
        'rcp' = relative concentration pathway
    years: numeric
        first year of 5-year period
    buffer: number
        Buffer around bounds of place_gdf

    Returns
    -------
    maca_df: DataFrame
        data frame with parameters and values
    """
    import rioxarray as rxr
    import xarray as xr
    import pandas as pd
    import geopandas as gpd
    
    def convert_lonlat(longitude):
        return ((longitude + 180) % 360) - 180
    
    maca_da_list = []
    for site_name, site_gdf in sites.items():
        for scenario in scenarios:
            for year in years:
                for climate in climates:
                    year_end = year + 4
                    maca_url = (
                        "http://thredds.northwestknowledge.net:8080/"
                        "thredds/dodsC/MACAV2/BNU-ESM/"
                        "macav2metdata_"
                        f"{scenario}_BNU-ESM_r1i1p1_{climate}"
                        f"_{year}_{year_end}_CONUS_monthly.nc")
                    # Read data and set up coordinates.
                    #maca_da = rxr.open_rasterio(maca_url, mask_and_scale=True).squeeze().precipitation
                    maca_da = xr.open_dataset(maca_url).squeeze().precipitation
                    #maca_da = xr.DataArray(maca_da)
                    maca_da = maca_da.rio.write_crs("EPSG:4326")
                    maca_da = maca_da.assign_coords(
                        lon = ("lon", [convert_lonlat(l) for l in maca_da.lon.values]),
                        lat = ("lat", [convert_lonlat(l) for l in maca_da.lat.values]))
                    maca_da = maca_da.rio.set_spatial_dims(x_dim='lon', y_dim='lat')
                    # Clip bounds.
                    maca_da = da_bounds(site_gdf, maca_da, buffer)
                    maca_da_list.append(dict(
                        site_name = site_name,
                        scenario = scenario,
                        year = year,
                        climate = climate,
                        da = maca_da))
                    
    maca_df = pd.DataFrame(maca_da_list)

    return maca_df

# maca_df = process_maca({'buffalo': buffalo_gdf}, ['pr'], ['rcp85', 'rcp45'], [2026], 0.1)

def maca_year(maca_df, row=0, year=2027):
    """
    Extract and print year data

    Parameters
    ----------
    maca_df: DataFrame
        DataFrame with MACA data by row

    Returns
    -------
    maca_year: DataArray
        DataArray for year and row selected.
    """
    maca_da = maca_df.loc[row, 'da']
    # Find the total precipitation for each pixel across all months for each individual year?
    maca_yearly_da= maca_da.groupby('time.year').sum()
    
    # Calculate the total annual precipitation for each year?
    # maca_annual = maca_yearly_da.groupby('year').sum(["lat", "lon"])

    maca_year = maca_yearly_da['year' == year]
    maca_year = maca_year.rio.write_crs("EPSG:4326")

    return maca_year
    
# maca_2027 = maca_year(maca_df, 0, 2027)
# from landmapy.index import redline_over_index
# redline_over_index(buffalo_gdf, maca_2027, edgecolor="white")