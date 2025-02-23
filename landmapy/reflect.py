"""
Reflectance Functions.

read_wbd_file: Read WBD File using cache key
read_delta_gdf: Read Delta WBD using cache decorator
compute_reflectance_da: Connect to files over VSI, crop, cloud mask, and wrangle
merge_and_composite_arrays: Merge and Composite Arrays
reflectance_kmeans: KMeans Clusters for Reflectance Bands
reflectance_range: Check ranges of bands
reflectance_rgb: RGB saturation of reflectance
"""
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

@cached('delta_reflectance_da_df')
def compute_reflectance_da(search_results, boundary_gdf):
    """
    Connect to files over VSI, crop, cloud mask, and wrangle.
    
    Returns a single reflectance DataFrame 
    with all bands as columns and
    centroid coordinates and datetime as the index.
    
    Args:
        file_df (df): File connection and metadata (datetime, tile_id, band, and url)
        boundary_gdf (gdf): Boundary use to crop the data
    Returns:
        granule_da_df (df): Single granule reflectance
    """
    from landmapy.earthaccess import get_earthaccess_links
    import rioxarray as rxr
    import numpy as np
    import pandas as pd
    from tqdm.notebook import tqdm

    def open_dataarray(url, boundary_proj_gdf, scale=1, masked=True):
        # Open masked DataArray
        da = rxr.open_rasterio(url, masked=masked).squeeze() * scale
        
        # Reproject boundary if needed
        if boundary_proj_gdf is None:
            boundary_proj_gdf = boundary_gdf.to_crs(da.rio.crs)
            
        # Crop
        cropped = da.rio.clip_box(*boundary_proj_gdf.total_bounds)
        return cropped
    
    def compute_quality_mask(da, mask_bits=[1, 2, 3]):
        """Mask out low quality data by bit."""
        # Unpack bits into a new axis
        bits = (
            np.unpackbits(
                da.astype(np.uint8), bitorder='little'
            ).reshape(da.shape + (-1,))
        )

        # Select the required bits and check if any are flagged
        mask = np.prod(bits[..., mask_bits]==0, axis=-1)
        return mask

    file_df = get_earthaccess_links(search_results)
    
    granule_da_rows= []
    boundary_proj_gdf = None

    # Loop through each image
    group_iter = file_df.groupby(['datetime', 'tile_id'])
    for (datetime, tile_id), granule_df in tqdm(group_iter):
        print(f'Processing granule {tile_id} {datetime}')
              
        # Open granule cloud cover
        cloud_mask_url = (
            granule_df.loc[granule_df.band=='Fmask', 'url']
            .values[0])
        cloud_mask_cropped_da = open_dataarray(cloud_mask_url, boundary_proj_gdf, masked=False)

        # Compute cloud mask
        cloud_mask = compute_quality_mask(cloud_mask_cropped_da)

        # Loop through each spectral band
        da_list = []
        df_list = []
        for i, row in granule_df.iterrows():
            if row.band.startswith('B'):
                # Open, crop, and mask the band
                band_cropped = open_dataarray(
                    row.url, boundary_proj_gdf, scale=0.0001)
                band_cropped.name = row.band
                # Add the DataArray to the metadata DataFrame row
                row['da'] = band_cropped.where(cloud_mask)
                granule_da_rows.append(row.to_frame().T)
    
    # Reassemble the metadata DataFrame
    return pd.concat(granule_da_rows)

# reflectance_da_df = compute_reflectance_da(results, delta_gdf)

@cached('delta_reflectance_da')
def merge_and_composite_arrays(granule_da_df):
    """
    Merge and Composite Arrays.

    Args:
        granule_da_df (df): dataframe with granule information
    Returns:
        da: data array with merged band information
    """
    from tqdm.notebook import tqdm
    import rioxarray.merge as rxrmerge
    import xarray as xr    

    # Merge and composite and image for each band
    df_list = []
    da_list = []
    for band, band_df in tqdm(granule_da_df.groupby('band')):
        merged_das = []
        for datetime, date_df in tqdm(band_df.groupby('datetime')):
            # Merge granules for each date
            merged_da = rxrmerge.merge_arrays(list(date_df.da))
            # Mask negative values
            merged_da = merged_da.where(merged_da>0)
            merged_das.append(merged_da)
            
        # Composite images across dates
        composite_da = xr.concat(merged_das, dim='datetime').median('datetime')
        composite_da['band'] = int(band[1:])
        composite_da.name = 'reflectance'
        da_list.append(composite_da)
        
    return xr.concat(da_list, dim='band')

# reflectance_da = merge_and_composite_arrays(reflectance_da_df)

def reflectance_kmeans(reflectance_da):
    """
    KMeans Clusters for Reflectance Bands.
    
    Args:
        reflectance_da (da): data array of reflectance information
    Returns:
        model_df (df): data frame with band data and clusters
    """
    import pandas as pd
    from sklearn.cluster import KMeans

    # Convert spectral DataArray to a tidy DataFrame
    # Each band gets its own column.
    model_df = reflectance_da.to_dataframe().reflectance.unstack('band')
    # Drop bands 10,11 and NA values.
    model_df = model_df.drop(columns=[10, 11]).dropna()

    # Running the fit and predict functions at the same time.
    # We can do this since we don't have target data.
    # Could use silouette plot to pick number of clusters.
    # See earlier demo (canvas?).
    prediction = KMeans(n_clusters=6).fit_predict(model_df.values)

    # Add the predicted values back to the model DataFrame
    model_df['clusters'] = prediction
    return model_df

# model_df = reflectance_model(reflectance_da)

def reflectance_range(model_df):
    """
    Check ranges of bands.
    
    Args:
        model_df (df): data frame with band data and clusters
    Returns
        minmax_df (df): data frame with min and max
    """
    import pandas as pd
    return pd.DataFrame({'min': model_df.min(), 'max': model_df.max()})

# reflectance_range(model_df)

def reflectance_rgb(reflectance_da):
    """
    RGB saturation of reflectance.
    
    Args:
        reflectance_da (da): data array of reflectance information
    Returns:
        rgb_sat (da): rescaled to 0-255 with saturation
    """
    import numpy as np

    rgb = reflectance_da.sel(band=[4, 3, 2])
    rgb_uint8 = (rgb * 255).astype(np.uint8).where(rgb!=np.nan)
    rgb_bright = rgb_uint8 * 10 # rescale to see color contrast better
    rgb_sat = rgb_bright.where(rgb_bright < 255, 255) # max out at 255 saturation
    return rgb_sat

# rgb_sat = reflectance_rgb(reflectance_da)
