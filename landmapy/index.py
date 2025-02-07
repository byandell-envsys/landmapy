"""
Index functions.

Plot map for created index and overlay with redlining grades.
Mask map by redline grades and create a `GeoDataFrame`.
Fit a tree model and compare maps.
"""
def redline_over_index(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Deprecated. Use gdf_da
    """
    return plot_gdf_over_da(place_gdf, index_da, edgecolor, cmap)

def gdf_over_da(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Deprecated. Use plot_gdf_da
    """
    return plot_gdf_da(place_gdf, index_da, edgecolor, cmap)

def plot_index(index_da, place, index='NDVI'):
    """
    Show plot of index.

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

def redline_mask(place_gdf, index_da):
    """
    Create new gdf for redlining using regionmask.
    
    Args:
        place_gdf (gdf): gdf for redlined place
        index_da (da): index for place
    Returns:
        redlining_mask (gdf): gdf with `regionmask` applied.
    """
    import regionmask # Convert shapefile to mask

    redlining_mask = regionmask.mask_geopandas(
        # Put gdf in same CRS as raster
        place_gdf.to_crs(index_da.rio.crs),
        # x and y coordinates from raster data x=504 y=447
        index_da.x, index_da.y,
        # The regions do not overlap
        overlap=False,
        # We're not using geographic coordinates
        wrap_lon=False)
    
    return redlining_mask

# redlining_mask = redline_mask(place_gdf, index_da)

def redline_index_gdf(redlining_gdf, index_stats):
    """
    Merge index stats with redlining gdf into one gdf.
        
    Args:
        redlining_gdf (gdf): gdf for redlined place
        index_stats (da): da with zonal stats
    Returns:
        redlining_index_gdf (gdf): gdf with zonal stats
    """
    import pandas as pd

    redlining_index_gdf = redlining_gdf.merge(
        index_stats.set_index('zone'),
        left_index=True, right_index=True)
    
    # Change grade to ordered Categorical for plotting
    redlining_index_gdf.grade = pd.Categorical(
        redlining_index_gdf.grade,
        ordered=True,
        categories=['A', 'B', 'C', 'D'])

    # Drop rows with NA grades
    redlining_index_gdf = redlining_index_gdf.dropna()

    return redlining_index_gdf

# redlining_index_gdf = redline_index_gdf(redlining_gdf, index_stats)
    
def index_grade_hv(redlining_index_gdf, place, index='NDVI'):
    """
    HV plots for index and grade.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
        place (char): Name of selected place
        index (char, optional): index name
    Returns:
        index_hv, grade_hv (hvplot): HV plot objects for mean index and redline grade
    """
    import hvplot.pandas # Interactive plots with pandas
    
    index_hv = redlining_index_gdf.hvplot(
        c='mean', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = f'{place} Mean {index}',
        clabel=f'Mean {index}', cmap='Greens')
    
    grade_hv = redlining_index_gdf.hvplot(
        c='grade', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = place + ' Redlining Grades',
        cmap='cet_diverging_bwr_20_95_c54')

    return index_hv, grade_hv

# index_hv, grade_hv = index_grade_hv(redlining_index_gdf)

def index_tree(redlining_index_gdf):
    """
    Convert categories to numbers.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
    Returns:
        tree_classifier (decision_tree): Decision tree for classifier
    """
    from sklearn.tree import DecisionTreeClassifier

    redlining_index_gdf['grade_codes'] = (
        redlining_index_gdf.grade.cat.codes)

    # Fit model
    tree_classifier = DecisionTreeClassifier(max_depth=2).fit(
        redlining_index_gdf[['mean']],
        redlining_index_gdf.grade_codes)
    
    return tree_classifier

# tree_classifier = index_tree(redlining_index_gdf)

def plot_index_pred(redlining_index_gdf, tree_classifier, place):
    """
    Plot the model results.
            
    Args:
        redlining_index_gdf (gdf): gdf with zonal stats
        tree_classifier (decision_tree): Decision tree for classifier
        place (char): Name of selected place
    Returns:
        pred_hv (hvplot): HV plot object for tree classifier
    """
    import hvplot.pandas # Interactive plots with pandas
    
    # Predict grades for each region
    redlining_index_gdf ['predictions'] = (
        tree_classifier.predict(redlining_index_gdf[['mean']]))

    # Subtract actual grades from predicted grades
    redlining_index_gdf['error'] = (
        redlining_index_gdf ['predictions'] - redlining_index_gdf ['grade_codes'])

    # Plot the calculated prediction errors as a chloropleth
    pred_hv = redlining_index_gdf.hvplot(
        c='error', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        clabel='Predicted Grades Error',
        title = place + ' Calculated Prediction Errors')

    return pred_hv

# pred_hv = plot_index_pred(redlining_index_gdf, tree_classifier, place)
