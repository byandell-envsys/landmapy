def da_bounds(place_gdf, da, buffer = 0.1):
    """
    Deprecated: use gdf_da_bounds()
    """
    return gdf_da_bounds(place_gdf, da, buffer)

def soil_url_dict(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200"):
    """
    Deprecated: use landmapy.polaris.soil_url_dict()
    """
    import landmapy
    return polaris.soil_url_dict(place_gdf, soil_var, soil_sum, soil_depth)
    
def merge_soil(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200",
               buffer = 0.1):
    """
    Deprecated: use landmapy.polaris.merge_soil()
    """
    import landmapy
    return polaris.merge_soil(place_gdf, soil_var, soil_sum, soil_depth, buffer)
    
def create_data_dir(new_dir='habitat'):
    """
    Create Data Directory if it does not exist.

    Args:
        new_dir (char, optional): Name of new directory
    Returns:
        data_dir (char): path to new directory
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

def gdf_da_bounds(place_gdf, da, buffer = 0.1):
    """
    Clip bounds from place_gdf on da extended by buffer.

    The buffer value could be 0.025 instead of 0.1
    
    Args:
        place_gdf (gdf): gdf of selected location
        da (da): da from calling routine
        buffer (float): Buffer around bounds of place_gdf
    Results:
        da (da): da with restricted to bounds of place_gdf 
    """
    bounds = place_gdf.to_crs(da.rio.crs).total_bounds
    bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    da = da.rio.clip_box(*bounds)

    return da

# da = gdf_da_bounds(place_gdf, da, 0.1)

def process_maca(sites, scenarios=['pr'], climates=['rcp85', 'rcp45'], years = [2026],
                 buffer = 0.1):
    """
    Process MACA Monthly Data.

    Args:
        sites (dict): dictionary with gdfs
        scenarios (char, optional): 'pr' = precipitation
        climates (char, optional): 'rcp' = relative concentration pathway
        years (int, optional) : first year of 5-year period
        buffer (float): Buffer around bounds of place_gdf
    Returns:
        maca_df (df): df with parameters and values
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

    Args:
        maca_df (df): DataFrame with MACA data by row
    Returns:
        maca_year (da): da for year and row selected.
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

def srtm_download(place_gdf, elevation_dir, buffer = 0.1):
    """
    Download SRTM data and create DataArray.

    Parameters
    ----------
    place_gdf: GeoDataFrame
      GeoDataFrame for redlined city
    elevation_dir: character string
      Name of directory with elevation data
    buffer: number
      Buffer around bounds of place_gdf
    Results
    -------
    srtm_da: DataArray
      DataArray of SRTM stuff
    """
    import os
    import earthaccess
    from glob import glob
    import xrspatial
    import rioxarray as rxr
    import rioxarray.merge as rxrmerge
    from landmapy.habitat import da_bounds

    # Get bounds from gdf. (want to DRY by using part of da_bounds())
    bounds = place_gdf.total_bounds
    bounds = bounds + [x * buffer for x in [-1,-1,1,1]] # buffer around place_gdf
    bounds = tuple(bounds)

    # This gets list of granules. Only need to do once.
    srtm_pattern = os.path.join(elevation_dir, '*.hgt.zip')
    if(not glob(srtm_pattern)):
        earthaccess.login()
        srtm_results = earthaccess.search_data(
            short_name = 'SRTMGL1',
            bounding_box = bounds
        )
        srtm_results = earthaccess.download(srtm_results, elevation_dir)

    srtm_da_list = []
    for srtm_path in glob(srtm_pattern):
        tile_da = rxr.open_rasterio(srtm_path, mask_and_scale=True).squeeze()
        tile_da = tile_da.rio.clip_box(*bounds)
        srtm_da_list.append(tile_da)

    srtm_da = rxrmerge.merge_arrays(srtm_da_list)
    # Make sure we are bounding properly.
    srtm_da = da_bounds(place_gdf, srtm_da, 0.1)

    return srtm_da

# srtm_da = srtm_download(place_gdf, elevation_dir, 0.1)
# srtm_da.plot(cmap='terrain')

def srtm_slope(srtm_da, UTM = 32613):
    """
    Calculate slope from SRTM data.

    Project to UTM to calculate slope, then project back.

    Args:
        srtm_da (da): da with elevation information
        UTM (int or char): UTM value (default is for UTM13N)
    Returns:
        slope_da (da): da with slopes (may be slightly different shape from srtm_da)
    """
    import xrspatial
    import rioxarray as rxr

    orig_crs = srtm_da.rio.crs
    srtm_utm_da = srtm_da.rio.reproject(UTM)
    slope_da = xrspatial.slope(srtm_utm_da).rio.reproject(orig_crs)
    
    return slope_da

# slope_da = srtm_slope(srtm_da, 32613)

def ramp_logic(data, up = (), down = ()):
    """
    Fuzzy ramp logic.

    Args:
        data (da): da with land measurements
        up, down (list of floats, optional): Either 1 (cliff) or 2 (ramp) values for fuzzy on-off
    Returns:
        fuzzy_data (da): Ramp with values between 0 and 1
    """
    import xarray as xr

    # Apply fuzzy logic: data > ramps[0] but it could be < ramps[1] with a ramp
    def ramp(data, fuzzy_data, up, sign=1.0):
        if(isinstance(up, float) | isinstance(up, int)):
            up = (up,)
        if(len(up)):
            fuzzy_data = fuzzy_data * (sign * data >= sign * max(up))
            if(len(up) > 1):
                up = sorted(up[:2])
                diff = up[1] - up[0]
                if(diff > 0):
                    ramp_mask = (data > up[0]) & (data <= up[1])
                    fuzzy_data = fuzzy_data + sign * ramp_mask * (data - up[0]) / diff
        return fuzzy_data

    # Set `fuzzy_data` to 1.0.
    fuzzy_data = xr.full_like(data, 1.0)
    # Ramp up.
    fuzzy_data = ramp(data, fuzzy_data, up, 1.0)
    # Ramp down.
    fuzzy_data = ramp(data, fuzzy_data, down, -1.0)

    return fuzzy_data

# data = x = xr.DataArray([float(i) for i in  range(21)])
# ramp_logic(data, (5.0, 10.0), 15)
