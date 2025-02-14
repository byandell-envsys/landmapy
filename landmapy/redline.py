"""
Redline functions.

redline_gdf: Read redlining GeoDataFrame from Mapping Inequality
plot_gdf_state: Plot overlay of redlining GeoDataFrame with state boundaries
"""
def plot_redline(place_gdf):
    """
    Deprecated. plot_gdf
    """
    return plot_gdf_state(place_gdf)

def redline_gdf(data_dir):
    """
    Read redlining GeoDataFrame from Mapping Inequality.

    Args:
        data_dir (char): Name of data directory
    Returns:
        place_gdf (gdf): GeoDataFrame for place
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
      place_gdf = gpd.read_file(redlining_url)
      place_gdf.to_file(redlining_path)

    # Load from file
    place_gdf = gpd.read_file(redlining_path)
    
    return place_gdf

# place_gdf = redline_gdf(data_dir)

# redline_map(data_dir)

def plot_gdf_state(place_gdf):
    """
    Plot overlay of redlining GeoDataFrame with state boundaries.

    Args:
        place_gdf (gdf): gdf with redlining cities
    Returns:
        cropped_da (da): Processed raster da
    """
    import matplotlib.pyplot as plt
    import geopandas as gpd # Work with vector data
    
    # Download state data using cenpy and read into GeoDataFrame
    state_url = "https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip"
    states_gdf = gpd.read_file(state_url)

    # Calculate the bounding box
    bbox = place_gdf.total_bounds
    xmin, ymin, xmax, ymax = bbox

    fig, ax = plt.subplots(figsize=(10, 10))
    states_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    place_gdf.plot(ax=ax)

    # Setting the bounds
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

    return plt.show()

# plot_gdf_state(place_gdf)
