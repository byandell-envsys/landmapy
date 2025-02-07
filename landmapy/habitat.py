def da_bounds(place_gdf, da, buffer = 0.1):
    """
    Deprecated: use gdf_da_bounds()
    """
    return gdf_da_bounds(place_gdf, da, buffer)

def soil_url_dict(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200"):
    """
    Deprecated: use landmapy.polaris.soil_url_dict()
    """
    from landmapy import polaris.soil_url_dict
    return polaris.soil_url_dict(place_gdf, soil_var, soil_sum, soil_depth)
    
def merge_soil(place_gdf, soil_var="sand", soil_sum="mean", soil_depth="100_200",
               buffer = 0.1):
    """
    Deprecated: use landmapy.polaris.merge_soil()
    """
    from landmapy import polaris.merge_soil
    return polaris.merge_soil(place_gdf, soil_var, soil_sum, soil_depth, buffer)

def process_maca(sites, scenarios=['pr'], climates=['rcp85', 'rcp45'], years = [2026],
                 buffer = 0.1):
    """
    Deprecated: use landmapy.thredds.process_maca()
    """
    from landmapy import thredds.process_maca
    return thredds.process_maca(sites, scenarios, climates, years, buffer)

def maca_year(maca_df, row=0, year=2027):
    """
    Deprecated: use landmapy.thredds.maca_year()
    """
    from landmapy import thredds.maca_year
    return thredds.maca_year(maca_df, row, year)

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
