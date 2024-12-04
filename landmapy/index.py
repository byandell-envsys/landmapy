def plot_index(city_ndvi_da, city):
    """Plot Index."""
    import matplotlib.pyplot as plt # Overlay raster and vector data
    #Plot the ndvi_da to see CRS
    city_ndvi_da.plot(
        cbar_kwargs={"label": "NDVI"},
        robust=True)
    plt.gca().set(
        title = city + ' NDVI',
        xlabel='',
        ylabel='')
    plt.show()

# plot_index(city_ndvi_da, city)

def redline_over_index(city_redlining_gdf, city_ndvi_da):
    """Overlay redlining grades on NDVI map."""
    import cartopy.crs as ccrs # CRSs
    import matplotlib.pyplot as plt # Overlay raster and vector data

    city_plot_gdf = city_redlining_gdf.to_crs(ccrs.Mercator())
    ndvi_plot_da = city_ndvi_da.rio.reproject(ccrs.Mercator())

    ndvi_plot_da.plot(vmin=0, robust=True)
    city_plot_gdf.plot(ax=plt.gca(), color='none')
    plt.gca().set(
        xlabel='', ylabel='', xticks=[], yticks=[])
    plt.show()

# redline_over_index(city_redlining_gdf, city_ndvi_da)

def redline_mask(city_redlining_gdf, city_ndvi_da):
    """Define new variable for denver redlining mask, using regionmask."""
    import regionmask # Convert shapefile to mask
    redlining_mask = regionmask.mask_geopandas(
        # Put gdf in same CRS as raster
        city_redlining_gdf.to_crs(city_ndvi_da.rio.crs),
        # x and y coordinates from raster data x=504 y=447
        city_ndvi_da.x, city_ndvi_da.y,
        # The regions do not overlap
        overlap=False,
        # We're not using geographic coordinates
        wrap_lon=False)
    
    return redlining_mask

# redlining_mask = redline_mask(city_redlining_gdf, city_ndvi_da)

def index_hv_plot(redlining_gdf, ndvi_stats, city):
    """Merge  NDVI stats with redlining geometry into one GeoDataFrame and plot."""
    import hvplot.pandas # Interactive plots with pandas
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
    
    # HV Plots
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

# ndvi_hv, grade_hv = ndvi_hv_plot(redlining_gdf, ndvi_stats, city)

def index_tree(redlining_ndvi_gdf):
    """# Convert categories to numbers"""
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.model_selection import train_test_split, cross_val_score

    redlining_ndvi_gdf['grade_codes'] = (
        redlining_ndvi_gdf.grade.cat.codes)

    # Fit model
    tree_classifier = DecisionTreeClassifier(max_depth=2).fit(
        redlining_ndvi_gdf[['mean']],
        redlining_ndvi_gdf.grade_codes)
    
    return tree_classifier

# tree_classifier = index_tree(redlining_ndvi_gdf)

def plot_index_pred(redlining_ndvi_gdf, tree_classifier, city):
    """Plot the model results."""
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