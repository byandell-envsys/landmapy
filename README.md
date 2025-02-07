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
| redline | redline_gdf | gdf | read | redline | Read redlining GeoDataFrame from Mapping Inequality |
| redline | plot_gdf_state || plot | plot | Plot overlay of gdf with state boundaries |
| process | process_image | da || process | Load, crop, and scale a raster image from earthaccess |
| process | process_cloud_mask | array || process | Load an 8-bit Fmask file and create a boolean mask |
| process | process_metadata | df || process | Create df of raster data URIs from earthaccess metadata |
| process | process_bands | da || process | Process bands from gdf with df metadata |
| index | plot_index || plot | plot | Show plot of index |
| index | plot_gdf_da || plot | plot | Overlay gdf on da map |
| index | redline_mask | gdf || redline | Create new gdf for redlining using regionmask |
| index | redline_index_gdf | gdf || redline | Merge index stats with redlining gdf into one gdf |
| index | index_grade_hv | hvplot | plot | redline | HV plots for index and grade |
| index | index_tree | decision_tree || redline | Convert categories to numbers |
| index | plot_index_pred | hvplot | plot | redline | Plot the model results |
| habitat | creata_data_dir | char | mkdir | habitat, bigdata, cluster | Create Data Directory if it does not exist |
| habitat | gdf_da_bounds | da ||| Clip bounds from place_gdf on da extended by buffer |
| habitat | ramp_logic | da || process | Fuzzy ramp logic |
| polaris | soil_url_dict | dict | read | POLARIS | Set up soil URLs based on place |
| polaris | merge_soil | da | read | POLARIS | Merge soil data |
| thredds | process_maca | df | read | THREDDS | Process MACA Monthly Data |
| thredds | maca_year | da || THREDDS | Extract and print year data |
| srtm | srtm_download | da | download | SRTM | Download SRTM data and create da |
| srtm | srtm_slope | da || SRTM | Calculate slope from SRTM data |
| redline | plot_redline |||| deprecated: use plot_gdf |
| index | redline_over_index |||| deprecated: use plot_gdf_da |
| index | gdf_over_da |||| deprecated: use plot_gdf_da |
| habitat | da_bounds |||| deprecated: use gdf_da_bounds |
