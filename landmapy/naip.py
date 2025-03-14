"""
NAIP Functions.

naip_path: Create NAIP tracts path
download_naip_scenes: Download NAIP Tracts
ndvi_naip_df: Get stats for all NAIP tracts
ndvi_naip_one: Get stats for one NAIP tract (internal)
check_element_in_csv: Check value of element in CSV file (internal)
merge_ndvi_cdc: Merge NDVI and CDC data
"""
def naip_path(data_dir, place = 'chicago'):
    """
    Create NAIP tracts path.
    
    Args:
        data_dir (str): data directory
        place (str): name of place
    Returns:
        naip_index_path (str): address of NAIP tracts
    """
    import os
    
    naip_index_path = os.path.join(data_dir, f'{place}-naip-stats.csv')

    return naip_index_path

# naip_index_path = naip_path(data_dir, 'chicago')

def download_naip_scenes(naip_index_path, tract_cdc_gdf):
    """
    Download NAIP Scene URLs.
    
    Args:
        naip_index_path (str): NAIP index CSV file address
        tract_cdc_gdf (gdf): gdf of combined place and disease
    Returns:
        scene_df (df): naip scenes DataFrame
    """
    import os
    import pandas as pd
    import shapely
    import pystac_client
    from tqdm.notebook import tqdm
    
    # Check for existing data - do not access duplicate tracts
    downloaded_tracts = []
    if os.path.exists(naip_index_path):
        naip_index_df = pd.read_csv(naip_index_path)
        downloaded_tracts = naip_index_df.tract.values
    else:
        # Connect to the planetary computer catalog
        e84_catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1"
        )
        # Convert geometry to lat/lon for STAC
        tract_latlon_gdf = tract_cdc_gdf.to_crs(4326)

        # Download asthma data (only once)
        print('No census tracts downloaded so far')
        # Loop through each census tract
        scene_dfs = []
        for i, tract_values in tqdm(tract_latlon_gdf.iterrows()):
            tract = tract_values.tract2010
            # Check if statistics are already downloaded for this tract
            if not (tract in downloaded_tracts):
                # Retry up to 5 times in case of a momentary disruption
                i = 0
                retry_limit = 5
                while i < retry_limit:
                    # Try accessing the STAC
                    try:
                        # Search for tiles
                        naip_search = e84_catalog.search(
                            collections=["naip"],
                            intersects=shapely.to_geojson(tract_values.geometry),
                            datetime="2021"
                        )
                        
                        # Build dataframe with tracts and tile urls
                        scene_dfs.append(pd.DataFrame(dict(
                            tract=tract,
                            date=[pd.to_datetime(scene.datetime).date() 
                                for scene in naip_search.items()],
                            rgbir_href=[scene.assets['image'].href for scene in naip_search.items()],
                        )))
                        
                        break
                    # Try again in case of an APIError
                    except pystac_client.exceptions.APIError:
                        print(
                            f'Could not connect with STAC server. '
                            f'Retrying tract {tract}...')
                        time.sleep(2)
                        i += 1
                        continue
            
        # Concatenate the url dataframes
        if scene_dfs:
            naip_scenes_df = pd.concat(scene_dfs).reset_index(drop=True)
        else:
            naip_scenes_df = None

    return naip_scenes_df

# naip_index_path = naip_path(data_dir, 'chicago')
# naip_scenes_df = download_naip_scenes(naip_index_path, tract_cdc_gdf)

def ndvi_naip_one(tract_cdc_gdf, tract, tract_date_gdf):
    """
    Get stats for one NAIP tract.

    Args:
        tract_cdc_gdf (gdf): gdf
        tract (int): tract number
        tract_date_gdf (gdf): gdf

    Returns:
        _type_: _description_
    """
    import numpy as np
    import rioxarray as rxr
    import rioxarray.merge as rxrmerge
    from scipy.ndimage import label
    from scipy.ndimage import convolve

    # Open all images for tract
    tile_das = []
    for _, href_s in tract_date_gdf.iterrows():
        # Open vsi connection to data
        tile_da = rxr.open_rasterio(
            href_s.rgbir_href, masked=True).squeeze()
        
        # Clip data
        boundary = (
            tract_cdc_gdf
            .set_index('tract2010')
            .loc[[tract]]
            .to_crs(tile_da.rio.crs)
            .geometry
        )
        crop_da = tile_da.rio.clip_box(
            *boundary.envelope.total_bounds,
            auto_expand=True)
        clip_da = crop_da.rio.clip(boundary, all_touched=True)
            
        # Compute NDVI
        ndvi_da = (
            (clip_da.sel(band=4) - clip_da.sel(band=1)) 
            / (clip_da.sel(band=4) + clip_da.sel(band=1))
        )

        # Accumulate result
        tile_das.append(ndvi_da)

    # Merge data
    scene_da = rxrmerge.merge_arrays(tile_das)

    # Mask vegetation
    veg_mask = (scene_da>.3)

    # Calculate statistics and save data to file
    total_pixels = scene_da.notnull().sum()
    veg_pixels = veg_mask.sum()

    # Calculate mean patch size
    labeled_patches, num_patches = label(veg_mask)
    # Count patch pixels, ignoring background at patch 0
    patch_sizes = np.bincount(labeled_patches.ravel())[1:] 
    mean_patch_size = patch_sizes.mean()

    # Calculate edge density
    kernel = np.array([
        [1, 1, 1], 
        [1, -8, 1], 
        [1, 1, 1]])
    edges = convolve(veg_mask, kernel, mode='constant')
    edge_density = np.sum(edges != 0) / veg_mask.size
    
    return total_pixels, veg_pixels, mean_patch_size, edge_density

# total_pixels, veg_pixels, mean_patch_size, edge_density = ndvi_naip_one(tract_cdc_gdf, tract, tract_date_gdf)
    
def ndvi_naip_df(naip_index_path, tract_cdc_gdf, naip_scenes_df = None):
    """
    Compute NDVI index for all NAIP tracts.

    Args:
        naip_index_path (str): address of NAIP tracts
        tract_cdc_gdf (gdf): gdf of CDC tracts
        naip_scenes_df (df, optional): df of scenes
    Returns:
        ndvi_stats_df (df): NDVI stats DataFrame
    """
    import os
    import pandas as pd
    from tqdm.notebook import tqdm
    
    # Skip this step if no `scenes_df` data provided. 
    if not naip_scenes_df is None:
        # Loop through the census tracts with URLs
        for tract, tract_date_gdf in tqdm(naip_scenes_df.groupby('tract')):
            # Check each tract to see if it is in `naip_index_path` CSV yet.
            # This may be overkill as each time it checks them all. 
            if not check_element_in_csv(naip_index_path, 'tract', tract):
                total_pixels, veg_pixels, mean_patch_size, edge_density = ndvi_naip_one(tract_cdc_gdf, tract, tract_date_gdf)
                # Add a row to the statistics file for this tract
                pd.DataFrame(dict(
                    tract=[tract],
                    total_pixels=[int(total_pixels)],
                    frac_veg=[float(veg_pixels/total_pixels)],
                    mean_patch_size=[mean_patch_size],
                    edge_density=[edge_density]
                )).to_csv(
                    naip_index_path, 
                    mode='a', 
                    index=False, 
                    header=(not os.path.exists(naip_index_path))
                )

    # Re-load results from file **error seems to be here**
    ndvi_index_df = pd.read_csv(naip_index_path)
    
    return ndvi_index_df

# ndvi_index_df = ndvi_naip_df(naip_index_path, tract_cdc_gdf, naip_scenes_df)

def check_element_in_csv(filename, column_name, target_value):
    """
    Check value of element in CSV file.

    Args:
        filename (str): The path to the CSV file.
        column_name (str): The name of the column to search in.
        target_value: The value to search for.

    Returns:
        bool: True if the element is found, False otherwise.
    """
    import csv

    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row[column_name] == str(target_value):
                    return True
        return False
    except FileNotFoundError:
         return False
    

# is_found = check_element_in_csv(naip_index_path, 'target', 123456789):

def merge_ndvi_cdc(tract_cdc_gdf, ndvi_index_df):
    """
    Merge NDVI and CDC data.

    Args:
        tract_cdc_gdf (gdf): CDC tracts
        ndvi_index_df (df): NDVI stats on tracts
    Returns:
        ndvi_cdc_gdf (gdf): merged data as gdf
    """
    ndvi_cdc_gdf = (
        tract_cdc_gdf
        .merge(
            ndvi_index_df,
            left_on='tract2010', right_on='tract', how='inner')
    )
    return ndvi_cdc_gdf

# ndvi_cdc_gdf = merge_ndvi_cdc(tract_cdc_gdf, ndvi_index_df)
