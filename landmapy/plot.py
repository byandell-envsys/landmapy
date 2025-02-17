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

def plot_gdf_esri(place_gdf, index='asthma'):
    """
    GV Plot of place index as chloropleth.

    Args:
       place_gdf (gdf): combined gdf 
       index (str, optional): index column name
    """
    import contextily as ctx
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 10))

    place_plot = place_gdf.plot(column=index, ax=ax, edgecolor="black", cmap='Blues')

    # Add Esri Imagery basemap
    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, crs=place_gdf.crs.to_string())

    # Add a color bar
    cbar = plt.colorbar(place_plot.collections[0], ax=ax, orientation='vertical')
    cbar.set_label(f'{index.title()} Intensity')  # Set the label for the color bar

    # Show the plot
    plt.show()
    
# plot_gdf_esri(place_gdf)

def plot_matrix(model_df):
    """
    HV plot of model matrix

    Args:
        model_df (df): model DataFrame
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.pairplot(model_df.iloc[:, [1,2,3]])
    plt.show()
    
# plot_matrix(model_df)

def plot_train_test(y_test, index='asthma'):
    """
    Plot test fit.

    Args:
        y_text (nparray): test dataset
    """
    import matplotlib.pyplot as plt
    import numpy as np


    # Plot measured vs. predicted asthma prevalence with a 1-to-1 line
    # **note: has asthma 
    y_max = y_test[index].max()
    
    x = y_test[index]
    y = y_test[f'pred_{index}']
    
    plt.scatter(x, y, alpha=0.6, linewidth=0.5)

    # Add labels and title
    plt.xlabel(f'Measured Adult {index.title()} Prevalence')
    plt.ylabel('Predicted Adult {index.title()} Prevalence')
    plt.title('Linear Regression Performance - Testing Data')

    # Set x and y limits
    plt.xlim(0, y_max)
    plt.ylim(0, y_max)

    # Add an identity line
    identity_line = np.linspace(0, y_max, 100)
    plt.plot(identity_line, identity_line, color='blue', linestyle='--', linewidth=1)
    plt.show()

# plot_train_test(y_test)
