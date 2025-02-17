# landmapy

Land Mapping Python Package

Built as a complement to the 2024-25
[Earth Data Analytics](https://github.com/byandell-envsys/EarthDataAnalytics)
course taught through the
[Earth Lab](https://earthlab.colorado.edu/).
Special thanks to [Elsa Culler](https://eculler.github.io/) as well as
[Nate Quarderer](https://github.com/nquarder),
[Lilly Jones-Sanovia](https://github.com/yawapi),
and
[Alison Post](https://akpost21.github.io/).

Interestingly, Earth Lab members developed a Python package a few years ago,
[earthpy](https://earthpy.readthedocs.io)
([GitHub repo](https://github.com/earthlab/earthpy)).
It seems fairly self-contained, but stopped development in 2021.
For instance, is uses
[rasterio](https://github.com/rasterio/rasterio),
which seems to now be superceded by
[rioxarray](https://corteva.github.io/rioxarray).
Still there are some interesting ideas here.

This is somewhat a companion to by R package
[landmapr](https://github.com/byandell-envsys/landmapr).
They are being developed in parallel, with somewhat different goals.

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| initial | creata_data_dir | char | mkdir | habitat, bigdata, cluster | Create Data Directory if it does not exist |
| initial | robust_code || setup | Make code robust to interruptions |
||
| gvplot | gvplot_gdf | gvplot | plot | plot | Plot asthma data as chloropleth |
| gvplot | gvplot_chloropleth | gvplot | plot | plot | Generate a chloropleth with the given color column |
| gvplot | gvplot_ndvi_index | gvplot | plot | plot | Plot NDVI and CDC data |
| gvplot | gvplot_resid | gvplot | plot | plot | Plot model residual |
| hvplot | hvplot_matrix | hvplot | plot | plot | Plot of model matrix |
| hvplot | hvplot_tract_gdf | hvplot | plot | plot | Plot census tracts with satellite imagery background |
| hvplot | hvplot_train_test | hvplot | plot | plot | Plot test fit |
| hvplot | hvplot_index_grade | hvplot | plot | plot | Plots for index and grade |
| hvplot | hvplot_index_pred | hvplot | plot | plot | Plot the model results |
| plot | plot_gdf_da || plot | plot | Overlay gdf on da map |
| plot | plot_gdf_state || plot | plot | Plot overlay of gdf with state boundaries |
| plot | plot_index || plot | plot | Show plot of index |
||
| explore | index_tree | decision_tree || explore | Convert categories to numbers |
| explore | ramp_logic | da || explore | Fuzzy ramp logic |
| explore | var_trans | df || explore | Variable Selection and Transformation |
| explore | train_test | nparray || explore | Model fit using train and test sets |
| process | gdf_da_bounds | da ||| Clip bounds from place_gdf on da extended by buffer | 
| process | process_bands | da || process | Process bands from gdf with df metadata |
| process | process_cloud_mask | array || process | Load an 8-bit Fmask file and create a boolean mask |
| process | process_image | da || process | Load, crop, and scale a raster image from earthaccess |
| process | process_metadata | df || process | Create df of raster data URIs from earthaccess metadata |
||
| polaris | soil_url_dict | dict | read | POLARIS | Set up soil URLs based on place |
| polaris | merge_soil | da | read | POLARIS | Merge soil data |
| redline | redline_gdf | gdf | read | redline | Read redlining GeoDataFrame from Mapping Inequality |
| redline | redline_mask | gdf || redline | Create new gdf for redlining using regionmask |
| redline | redline_index_gdf | gdf || redline | Merge index stats with redlining gdf into one gdf |
| srtm | srtm_download | da | download | SRTM | Download SRTM data and create da |
| srtm | srtm_slope | da || SRTM | Calculate slope from SRTM data |
| thredds | process_maca | df | read | THREDDS | Process MACA Monthly Data |
| thredds | maca_year | da || THREDDS | Extract and print year data |
