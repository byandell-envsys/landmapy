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
