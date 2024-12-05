"""
Package landmapy.

Functions:
    redline.redline_gdf(data_dir)
    redline.plot_redline(redlining_gdf)
    process.process_image(uri, bounds_gdf)
    process.process_cloud_mask(cloud_uri, bounds_gdf, bits_to_mask)
    process.process_metadata(city_files)
    process.process_bands(city_gdf, raster_df)
    index.plot_index(city_ndvi_da, city)
    index.redline_over_index(city_redlining_gdf, city_ndvi_da)
    index.redline_mask(city_redlining_gdf, city_ndvi_da)
    index.redline_index_gdf(redlining_gdf, ndvi_stats)
    index.index_grade_hv(redlining_ndvi_gdf, city)
    index.index_tree(redlining_ndvi_gdf)
    index.plot_index_pred(redlining_ndvi_gdf, tree_classifier, city)
"""