"""
THREDDS Functions.

process_maca: Process MACA Monthly Data
maca_year: Extract and print year data
"""
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
        info_df (df): info with parameters
        maca_da_list (list): list of da with values across scenarios, climates, and years
    """
    import rioxarray as rxr
    import xarray as xr
    import pandas as pd
    import geopandas as gpd
    from math import floor, ceil
    from landmapy.process import gdf_da_bounds
    
    def convert_lonlat(longitude):
        return ((longitude + 180) % 360) - 180
    
    year_min = floor((min(years) - 1) // 5) * 5 + 1
    year_max = ceil((max(years) - 1) // 5) * 5 + 5
    print("Years:", year_min, year_max)
    
    maca_da_list = []
    info = []
    for site_name, site_gdf in sites.items():
        for scenario in scenarios:
            for climate in climates:
                periods = []
                for year in range(year_min, year_max, 5):
                    year_end = year + 4
                    maca_url = (
                        "http://thredds.northwestknowledge.net:8080/"
                        "thredds/dodsC/MACAV2/BNU-ESM/"
                        "macav2metdata_"
                        f"{scenario}_BNU-ESM_r1i1p1_{climate}"
                        f"_{year}_{year_end}_CONUS_monthly.nc")
                    # Read data and set up coordinates.
                    maca_da_year = (
                        xr.open_dataset(maca_url, mask_and_scale=True)
                        .squeeze()
                        .precipitation)
                    maca_da_year = maca_da_year.rio.write_crs("EPSG:4326")
                    maca_da_year = maca_da_year.assign_coords(
                        lon = ("lon", [convert_lonlat(l) for l in maca_da_year.lon.values]),
                        lat = ("lat", [convert_lonlat(l) for l in maca_da_year.lat.values]))
                    maca_da_year = maca_da_year.rio.set_spatial_dims(x_dim='lon', y_dim='lat')
                    # Clip bounds.
                    maca_da_year = gdf_da_bounds(site_gdf, maca_da_year, buffer)
                    periods.append(maca_da_year)
                # Concatenate and resample over years.
                maca_da = (
                    xr.concat(periods, dim='time')
                    .sortby('time')
                    .resample({'time': 'YE'})
                    .sum()
                    .rio.write_crs(4326))
                # Append info and DataArray.
                info.append(dict(
                    site_name = site_name,
                    scenario = scenario,
                    climate = climate))
                maca_da_list.append(maca_da)

    # Create invo DataFrame and MACA values DataArray from lists.
    info_df = pd.DataFrame(info)

    return info_df, maca_da_list

# info_df, maca_da_list = process_maca({'buffalo': buffalo_gdf}, ['pr'], ['rcp85', 'rcp45'], [2026], 0.1)

def maca_year(maca_da, year=2027):
    """
    Extract and print year data.

    Args:
        maca_da (da): DataArray with MACA data by row
    Returns:
        maca_year (da): da for year and row selected.
    """
    # Calculate the total annual precipitation for each year?
    # maca_annual = maca_yearly_da.groupby('year').sum(["lat", "lon"])

    maca_year = maca_da.sel(time=f'{year}-12-31')
    maca_year = maca_year.rio.write_crs("EPSG:4326")

    return maca_year
    
# maca_2010 = maca_year(maca_da[0], 2010)
# from landmapy.plot import plot_gdf_da
# plot_gdf_da(buffalo_gdf, maca_2010, edgecolor="white")
