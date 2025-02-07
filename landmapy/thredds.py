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
    from landmapy.habitat import gdf_da_bounds
    
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
                    maca_da = gdf_da_bounds(site_gdf, maca_da, buffer)
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
