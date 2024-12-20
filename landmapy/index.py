"""
Index functions.

Plot map for created index and overlay with redlining grades.
Mask map by redline grades and create a `GeoDataFrame`.
Fit a tree model and compare maps.
"""
def redline_over_index(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Deprecated. Use gdf_over_da
    """
    return gdf_over_da(place_gdf, index_da, edgecolor, cmap)

def plot_index(index_da, city):
    """
    Show plot of index.

    Parameters
    ----------
    index_da: DataArray
      DataArray containing NDVI index for city
    city: character string
      Name of selected city
    """
    import matplotlib.pyplot as plt # Overlay raster and vector data

    #Plot the ndvi_da to see CRS
    index_da.plot(
        cbar_kwargs={"label": "NDVI"},
        robust=True)
    plt.gca().set(
        title = city + ' NDVI',
        xlabel='',
        ylabel='')
    plt.show()

# plot_index(index_da, city)

def gdf_over_da(place_gdf, index_da, edgecolor='black', cmap='terrain'):
    """
    Overlay GeoDataFrame on DataArray map.
    
    Default `cmap` is 'viridis`;
    See <https://matplotlib.org/stable/users/explain/colors/colormaps.html>.

    Parameters
    ----------
    place_gdf: GeoDataFrame
      GeoDataFrame for redlined city
    index_da: DataArray
      DataArray containing NDVI index for city
    city: character string
      Name of selected city
    edgecolor: character string
      Name of color for edges of `place_gdf`
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

# gdf_over_da(place_gdf, index_da)

def redline_mask(place_gdf, index_da):
    """
    Define new variable for denver redlining mask, using regionmask.
    
    Parameters
    ----------
    place_gdf: GeoDataFrame
      GeoDataFrame for redlined city
    index_da: DataArray
      DataArray containing NDVI index for city
    
    Returns
    -------
    redlining_mask: GeoDataFrame
      GeoDataFrame with `regionmask` applied.
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

def redline_index_gdf(redlining_gdf, ndvi_stats):
    """
    Merge NDVI stats with redlining geometry into one GeoDataFrame and plot.
        
    Parameters
    ----------
    redlining_gdf: GeoDataFrame
      GeoDataFrame for redlined city
    ndvi_stats: DataArray
      DataArray with zonal stats
    
    Returns
    -------
    redlining_ndvi_gdf: GeoDataFrame
      GeoDataFrame with zonal stats.
    """
    import pandas as pd

    redlining_ndvi_gdf = redlining_gdf.merge(
        ndvi_stats.set_index('zone'),
        left_index=True, right_index=True)
    
    # Change grade to ordered Categorical for plotting
    redlining_ndvi_gdf.grade = pd.Categorical(
        redlining_ndvi_gdf.grade,
        ordered=True,
        categories=['A', 'B', 'C', 'D'])

    # Drop rows with NA grades
    redlining_ndvi_gdf = redlining_ndvi_gdf.dropna()

    return redlining_ndvi_gdf

# redlining_ndvi_gdf = redline_index_gdf(redlining_gdf, ndvi_stats)
    
def index_grade_hv(redlining_ndvi_gdf, city):
    """
    HV plots for index and grade.
            
    Parameters
    ----------
    redlining_ndvi_gdf: GeoDataFrame
      GeoDataFrame with zonal stats.
    city: character string
      Name of selected city
    
    Returns
    -------
    ndvi_hv, grade_hv: hvplot
      HV plot objects for mean index and redline grade.
    """
    import hvplot.pandas # Interactive plots with pandas
    
    ndvi_hv = redlining_ndvi_gdf.hvplot(
        c='mean', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = city + ' Mean NDVI',
        clabel='Mean NDVI', cmap='Greens')
    
    grade_hv = redlining_ndvi_gdf.hvplot(
        c='grade', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        title = city + ' Redlining Grades',
        cmap='cet_diverging_bwr_20_95_c54')

    return ndvi_hv, grade_hv

# ndvi_hv, grade_hv = index_grade_hv(redlining_ndvi_gdf)

def index_tree(redlining_ndvi_gdf):
    """
    Convert categories to numbers
            
    Parameters
    ----------
    redlining_ndvi_gdf: GeoDataFrame
      GeoDataFrame with zonal stats.
    
    Returns
    -------
    tree_classifier: decision_tree
      Decision tree for classifier.
    """
    from sklearn.tree import DecisionTreeClassifier

    redlining_ndvi_gdf['grade_codes'] = (
        redlining_ndvi_gdf.grade.cat.codes)

    # Fit model
    tree_classifier = DecisionTreeClassifier(max_depth=2).fit(
        redlining_ndvi_gdf[['mean']],
        redlining_ndvi_gdf.grade_codes)
    
    return tree_classifier

# tree_classifier = index_tree(redlining_ndvi_gdf)

def plot_index_pred(redlining_ndvi_gdf, tree_classifier, city):
    """
    Plot the model results.
            
    Parameters
    ----------
    redlining_ndvi_gdf: GeoDataFrame
      GeoDataFrame with zonal stats.
    tree_classifier: decision_tree
      Decision tree for classifier.
    city: character string
      Name of selected city
    
    Returns
    -------
    pred_hv: hvplot
      HV plot object for tree classifier.
    """
    import hvplot.pandas # Interactive plots with pandas
    
    # Predict grades for each region
    redlining_ndvi_gdf ['predictions'] = (
        tree_classifier.predict(redlining_ndvi_gdf[['mean']]))

    # Subtract actual grades from predicted grades
    redlining_ndvi_gdf['error'] = (
        redlining_ndvi_gdf ['predictions'] - redlining_ndvi_gdf ['grade_codes'])

    # Plot the calculated prediction errors as a chloropleth
    pred_hv = redlining_ndvi_gdf.hvplot(
        c='error', geo=True,
        xaxis='Longitude', yaxis='Latitude',
        clabel='Predicted Grades Error',
        title = city + ' Calculated Prediction Errors')

    return pred_hv

# pred_hv = plot_treepred(redlining_ndvi_gdf, tree_classifier, city)
