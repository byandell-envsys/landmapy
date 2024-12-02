def process_image(uri, bounds_gdf):
    """
    Load, crop, and scale a raster image from earthaccess

    Parameters
    ----------
    uri: file-like or path-like
      File accessor downloaded or obtained from earthaccess
    bounds_gdf: gpd.GeoDataFrame
      Area of interest to crop to

    Returns
    -------
    cropped_da: rxr.DataArray
      Processed raster
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

# process_image(denver_files[8], denver_redlining_gdf).plot()

def process_cloud_mask(cloud_uri, bounds_gdf, bits_to_mask):
    """
    Load an 8-bit Fmask file and process to a boolean mask

    Parameters
    ----------
    uri: file-like or path-like
      Fmask file accessor downloaded or obtained from earthaccess
    bounds_gdf: gpd.GeoDataFrame
      Area of interest to crop to
    bits_to_mask: list of int
      The indices of the bits to mask if set

    Returns
    -------
    cloud_mask: np.array
      Cloud mask
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

# blue_da = process_image(denver_files[1], denver_redlining_gdf)
# denver_cloud_mask = process_cloud_mask(
#     denver_files[-1],
#     denver_redlining_gdf,
#     [1, 2, 3, 5])
# blue_da.where(denver_cloud_mask).plot()