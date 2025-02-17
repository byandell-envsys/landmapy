"""
Plot Functions with GeoViews.

gvplot_gdf: Plot asthma data as chloropleth
gvplot_chloropleth: Generate a chloropleth with the given color column
gvplot_ndvi_index: Plot NDVI and CDC data
gvplot_resid: Plot model residual
"""
def gvplot_gdf(tract_cdc_gdf):
    """
    Plot asthma data as chloropleth.

    Args:
       tract_cdc_gdf (gdf): combined gdf 
    """
    import geoviews as gv
    from cartopy import crs as ccrs

    tract_cdc_gv = (
        gv.tile_sources.EsriImagery
        * 
        gv.Polygons(
            tract_cdc_gdf.to_crs(ccrs.Mercator()),
            vdims=['asthma', 'tract2010'],
            crs=ccrs.Mercator()
        ).opts(color='asthma', colorbar=True, tools=['hover'])
    ).opts(width=600, height=600, xaxis=None, yaxis=None)

    return tract_cdc_gv

# tract_cdc_gv = gvplot_gdf(tract_cdc_gdf)

def gvplot_chloropleth(gdf, **opts):
    """
    Generate a chloropleth with the given color column.
    
    Args:
        gdf (gdf): GeoDataFrame
    Returns:
        _ (gv_plot): plot
    """
    import geoviews as gv
    from cartopy import crs as ccrs
    
    return gv.Polygons(
        gdf.to_crs(ccrs.Mercator()),
        crs=ccrs.Mercator()
    ).opts(xaxis=None, yaxis=None, colorbar=True, **opts)
    
# gvplot_chloropleth(gdf)
    
def gvplot_ndvi_index(ndvi_cdc_gdf):
    """
    Plot NDVI and CDC data.

    Args:
        ndvi_cdc_gdf (gdf): merged data as gdf
    Returns:
        None
    """
    plot_ndvi = (
        gvplot_chloropleth(ndvi_cdc_gdf, color='asthma', cmap='viridis', title='Asthma')
        + 
        gvplot_chloropleth(ndvi_cdc_gdf, color='edge_density', cmap='Greens', title='Edge Density')
    )
    
    return plot_ndvi
    
# gvplot_ndvi_index(tract_cdc_gdf, ndvi_index_df)

def gvplot_resid(model_df, reg, yvar='log_asthma', xvar=['edge_density', 'mean_patch_size']):
    """
    Plot model residual
    
    Args:
        model_df (df): model object
        reg (LinearRegression): LinearRegression object
        yvar (str, optional): y variable name. Defaults to 'asthma'.
    Returns:
        resid_gv (gv_plot): plot
    """
    import numpy as np
    
    model_df[f'pred_{yvar}'] = np.exp(reg.predict(model_df[xvar]))
    model_df['err_yvar'] = model_df[f'pred_{yvar}'] - model_df[yvar]

    # Plot error geographically as a chloropleth
    resid_gv = (
        gvplot_chloropleth(model_df, color='err_yvar', cmap='RdBu', title="Residuals for Asthma")
        .redim.range(err_yvar=(-.3, .3))
        #.opts(frame_width=600, aspect='equal')
    )
    
    return resid_gv

# gvplot_resid(model_df, yvar='asthma')

