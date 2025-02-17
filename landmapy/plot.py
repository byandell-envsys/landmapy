"""
Plot Functions with matplotlib.pyplot.

plot_index: Plot index DataArray
plot_gdf_da: Overlay gdf on da map
plot_gdf_state: Plot overlay of redlining GeoDataFrame with state boundaries
""" 
def plot_index(index_da, place, index='NDVI'):
    """
    Plot index DataArray.

    Args:
        index_da (da): index for place
        place (char): Name of selected place
        index (char, optional): index type
    """
    import matplotlib.pyplot as plt # Overlay raster and vector data

    #Plot the index_da to see CRS
    index_da.plot(
        cbar_kwargs={"label": place},
        robust=True)
    plt.gca().set(
        title = f'{place} {index}',
        xlabel='',
        ylabel='')
    plt.show()

# plot_index(index_da, place)

def plot_gdf_da(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Overlay gdf on da map.
    
    Default `cmap` is 'viridis`;
    See <https://matplotlib.org/stable/users/explain/colors/colormaps.html>.

    Args:
        place_gdf (gdf): gdf for place
        index_da (da): index for place
        edgecolor (char, optional): Name of color for edges of gdf
        cmap (char, optional): color map
    """
    import cartopy.crs as ccrs # CRSs
    import matplotlib.pyplot as plt # Overlay raster and vector data

    # Plot index.
    index_da = index_da.rio.reproject(ccrs.Mercator())
    index_da.plot(vmin=0, robust=True, cmap=cmap)
    # Plot place outline
    for idx in range(0, len(place_gdf)):
      #print(buffalo_gdf.iloc[[idx]])
      place_idx_gdf = place_gdf.iloc[[idx]].to_crs(ccrs.Mercator())
      # Use color column from place_gdf if provided
      if 'color' in place_idx_gdf.columns:
          edgecolor = place_idx_gdf['color'].values[0]
      place_idx_gdf.boundary.plot(ax=plt.gca(), color=edgecolor)
    # Strip labels and ticks of and plot.
    plt.gca().set(
        xlabel='', ylabel='', xticks=[], yticks=[])
    plt.show()

# plot_gdf_da(place_gdf, index_da)

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
