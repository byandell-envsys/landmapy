from landmapy.cached import cached

@cached('wbd_08')
def read_wbd_file(wbd_filename, huc_level, cache_key):
    """
    Read WBD File using cache key.
    
    Args:
        wbd_filename (str): WBD file name 
        huc_level (int): HUC level
        cache_key (str): cache key to `cached` decorator
    Returns:
        wbd_gdf (gdf): GeoDataFrame
    """
    import os
    import earthpy as et
    import geopandas as gpd

    # Download and unzip
    wbd_url = (
        "https://prd-tnm.s3.amazonaws.com"
        "/StagedProducts/Hydrography/WBD/HU2/Shape/"
        f"{wbd_filename}.zip")
    wbd_dir = et.data.get_data(url=wbd_url)
                  
    # Read desired data
    wbd_path = os.path.join(wbd_dir, 'Shape', f'WBDHU{huc_level}.shp')
    wbd_gdf = gpd.read_file(wbd_path, engine='pyogrio')
    return wbd_gdf

# read_wbd_file(wbd_filename, huc_level, cache_key)

def read_delta_gdf(huc_level=12, watershed='080902030506'):
    """
    Read Delta WBD using cache decorator.

    Args:
        huc_level (int): HUC level
        watershed (str): watershed ID
    Return:
        delta_gdf (gdf): gdf of delta
    """
    wbd_gdf = read_wbd_file(
        "WBD_08_HU2_Shape", huc_level, cache_key=f'hu{huc_level}')

    delta_gdf = (
        wbd_gdf[wbd_gdf[f'huc{huc_level}']
        .isin([watershed])]
        .dissolve()
    )
    return delta_gdf

# delta_gdf = read_delta_gdf(12)

def hvplot_delta_gdf(delta_gdf, width=600, height=300):
    """
    HV Plot Delta GDF
    
    Args:
        delta_gdf (gdf): area to overlay on topomap
        width (int, optional): width
        height (int, optional): height
    Returns:
        delta_hv (hvplot): HV Plot
    """
    import cartopy.crs as ccrs
    import hvplot.pandas
    import hvplot.xarray

    delta_hv = (
        delta_gdf.to_crs(ccrs.Mercator())
        .hvplot(
            alpha=.2, fill_color='white', 
            tiles='EsriImagery', crs=ccrs.Mercator())
        .opts(width=width, height=height)
    )
    return delta_hv

# hvplot_delta_gdf(delta_gdf)

def plot_delta_gdf(delta_gdf):
    """
    Plot Delta GDF.
    
    Args:
        delta_gdf (gdf): area to overlay on topomap
    Returns:
        delta_hv (hvplot): HV Plot
    """
    import matplotlib.pyplot as plt
    import contextily as ctx

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    place_plot = delta_gdf.plot(ax=ax, edgecolor="black", color="none")
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=delta_gdf.crs.to_string())
    
    plt.show()
    
# plot_delta_gdf(delta_gdf)
