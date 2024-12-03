def redline_gdf(data_dir):
    """
    Read redlining GeoDataFrame from Mapping Inequality.

    Parameters
    ----------
    data_dir: character string
      Name of data directory

    Returns
    -------
    redlining_gdf: GeoDataFrame
      GeoDataFrame
    """
    import os # Interoperable file paths
    import geopandas as gpd # Work with vector data
    
    # Define info for redlining download
    redlining_url = (
        "https://dsl.richmond.edu/panorama/redlining/static"
        "/mappinginequality.gpkg"
    )
    redlining_dir = os.path.join(data_dir, 'redlining')
    os.makedirs(redlining_dir, exist_ok=True)
    redlining_path = os.path.join(redlining_dir, 'redlining.shp')

    # Only download once
    if not os.path.exists(redlining_path):
      redlining_gdf = gpd.read_file(redlining_url)
      redlining_gdf.to_file(redlining_path)

    # Load from file
    redlining_gdf = gpd.read_file(redlining_path)
    
    return redlining_gdf

# redline_map(data_dir)

def plot_redline(redlining_gdf):
    """
    Plot overlay of redlining GeoDataFrame with state boundaries.

    Parameters
    ----------
    redlining_gdf: GeoDataFrame object
      `gdf` with redlining cities

    Returns
    -------
    cropped_da: rxr.DataArray
      Processed raster
    """
    import matplotlib.pyplot as plt
    import geopandas as gpd # Work with vector data
    
    # Download state data using cenpy and read into GeoDataFrame
    state_url = "https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip"
    states_gdf = gpd.read_file(state_url)

    # Calculate the bounding box
    bbox = redlining_gdf.total_bounds
    xmin, ymin, xmax, ymax = bbox

    fig, ax = plt.subplots(figsize=(10, 10))
    states_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    redlining_gdf.plot(ax=ax)

    # Setting the bounds
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    return plt.show()

# plot_redline(redlining_gdf)