"""
Habitat Functions.

robust_code: Make code robust to interruptions
create_data_dir: Create Data Directory if it does not exist
gdf_da_bounds: Clip bounds from place_gdf on da extended by buffer (internal)
ramp_logic: Fuzzy ramp logic
"""
def robust_code():
    """
    Make code robust to interruptions.
    """
    import os
    import warnings
        
    warnings.simplefilter('ignore')

    # Prevent GDAL from quitting due to momentary disruptions
    os.environ["GDAL_HTTP_MAX_RETRY"] = "5"
    os.environ["GDAL_HTTP_RETRY_DELAY"] = "1"

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
