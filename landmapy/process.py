"""
Process functions.

Process metadata into raster DataArray,
which is used to process multi-spectral image bands.
Function `process_bands` calls `process_image` and `process_cloud_mask`.
"""
def process_image(uri, bounds_gdf):
    """
    Load, crop, and scale a raster image from earthaccess.

    Args:
        uri (file-like or path-like): File accessor downloaded or obtained from earthaccess
        bounds_gdf (gdf): Area of interest to crop to
    Returns:
        cropped_da (da): Processed raster
    """
    import rioxarray as rxr # Work with raster data

    # Connect to the raster image
    da = rxr.open_rasterio(uri, mask_and_scale=True).squeeze()

    # Get the study bounds
    bounds = (
        bounds_gdf
        .to_crs(da.rio.crs)
        .total_bounds
    )
    
    # Crop
    cropped_da = da.rio.clip_box(*bounds)

    return cropped_da

# process_image(city_files[8], city_gdf).plot()

def process_cloud_mask(cloud_uri, bounds_gdf, bits_to_mask):
    """
    Load an 8-bit Fmask file and create a boolean mask.

    Args:
        uri (file-like or path-like): Fmask file accessor downloaded or obtained from earthaccess
        bounds_gdf (gdf): Area of interest to crop to
        bits_to_mask (list of int): The indices of the bits to mask if set
    Returns:
        cloud_mask (array of int): Cloud mask array of bits
    """
    import numpy as np # Process bit-wise cloud mask

    # Open fmask file
    fmask_da = process_image(cloud_uri, bounds_gdf)

    # Unpack the cloud mask bits
    cloud_bits = (
        np.unpackbits(
            (
                # Get the cloud mask as an array...
                fmask_da.values
                # ... of 8-bit integers
                .astype('uint8')
                # With an extra axis to unpack the bits into
                [:, :, np.newaxis]
            ), 
            # List the least significant bit first to match the user guide
            bitorder='little',
            # Expand the array in a new dimension
            axis=-1)
    )

    cloud_mask = np.sum(
        # Select bits
        cloud_bits[:,:,bits_to_mask], 
        # Sum along the bit axis
        axis=-1
    # Check if any of bits are true
    ) == 0
    
    return cloud_mask

# blue_da = process_image(city_files[1], city_redlining_gdf)
# city_cloud_mask = process_cloud_mask(
#     city_files[-1],
#     city_redlining_gdf,
#     [1, 2, 3, 5])
# blue_da.where(city_cloud_mask).plot()

def process_metadata(city_files):
    """
    Create df of raster data URIs from earthaccess metadata.

    Args:
        city_files (file-like URI): File names from earthaccess
    Returns:
        raster_df (df): DataFrame with the metadata
    """
    import re # Use regular expressions to extract metadata
    import pandas as pd # Group and aggregate

    # Compile a regular expression to search for metadata
    uri_re = re.compile(
        r"HLS\.L30\."
        r"(?P<tile_id>T[0-9A-Z]+)\."  # `tile_id`
        r"(?P<date>\d+)T\d+\.v2\.0\." # `date` as `yyyyjjj` (year and Julian date)
        r"(?P<band_id>.+)\.tif")      # `band_id`
    # Find all the metadata in the file name
    uri_groups = [
        uri_re.search(city_file.full_name).groupdict()
        for city_file in city_files]

    # Create a DataFrame with the metadata
    raster_df = pd.DataFrame(uri_groups)

    # Add the File-like URI to the DataFrame
    raster_df['file'] = city_files

    return raster_df

# raster_df = process_metadata(city_files)
# raster_df.head()

def process_bands(city_gdf, raster_df):
    """
    Process bands from gdf with df metadata.

    Args:
        city_gdf (gdf): GeoDataFrame for a city
        raster_df (df): DataFrame of city metadata
    Returns:
        city_das (da): DataArray with image data
    """
    import re # Use regular expressions to extract metadata
    import pandas as pd # Group and aggregate
    import rioxarray as rxr # Work with raster data
    from rioxarray.merge import merge_arrays # Merge rasters

    # Labels for each band to process
    bands = {
        'B02': 'red',
        'B03': 'green',
        'B04': 'blue',
        'B05': 'nir'
    }
    # Initialize structure for saving images
    city_das = {band_name: [] for band_name in bands.values()}
    print('Loading...')
    for tile_id, tile_df in raster_df.groupby('tile_id'):
        print(tile_id)
        # Load the cloud mask
        fmask_file = tile_df[tile_df.band_id=='Fmask'].file.values[0]
        cloud_mask = process_cloud_mask(
            fmask_file, 
            city_gdf, 
            [1, 2, 3, 5])

        for band_id, row in tile_df.groupby('band_id'):
            if band_id in bands:
                band_name = bands[band_id]
                print(band_id, band_name)
                # Process band
                band_da = process_image(
                    row.file.values[0], 
                    city_gdf)

                # Mask band
                band_masked_da = band_da.where(cloud_mask)

                # Store the resulting DataArray for later
                city_das[band_name].append(band_masked_da)

    print('Done.')

    # Merge all tiles
    city_merged_das = {
        band_name: merge_arrays(das) 
        for band_name, das 
        in city_das.items()}

    return city_merged_das

# city_merged_das = process_bands(city_redlining_gdf, raster_df)
# city_merged_das['green'].plot(cmap='Greens', robust=True)
