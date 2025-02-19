# landmapy

## Land Mapping Python Package

The `landmapy` package is being built as a complement to the 2024-25
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
It seems fairly self-contained, but seemed to stop development in 2021.
For instance, is uses
[rasterio](https://github.com/rasterio/rasterio),
which seems to now be superceded by
[rioxarray](https://corteva.github.io/rioxarray).
Still there are some interesting ideas here that are still being used.

This is somewhat a companion to my R package
[landmapr](https://github.com/byandell-envsys/landmapr).
They are being developed in parallel, with somewhat different goals.
Right now, focus is on the python package to keep up with the
[Earth Data Analytics](https://github.com/byandell-envsys/EarthDataAnalytics)
course.

## Use Cases

This python package was begun in nov-dec 2024 as I found
the project tools growing.
I got some initial advice from EDA staff, then learned by
doing and looking at other tools.
To date, this package has been used in the following projects:

- [Clustering: Classify land cover for Mississippi Delta](https://github.com/earthlab-education/clustering-byandell)
(in progress)
- [Big-Data: Urban Greenspace and Asthma Prevalence](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data.md)
- [Habitat: Buffalo Grasslands Habitat Suitability](https://github.com/byandell-envsys/habitatSuitability/blob/main/buffalo.md)
- [Redlining: Predicting NDVI for Madison](https://github.com/earthlab-education/fundamentals-04-redlining-byandell/blob/main/notebooks/madison.ipynb)

These are all craft pieces, with increasing use of functions.
More recent projects shifted from a
[Jupyter notebook](https://jupyter.org/) (`project.ipynb`)
to a
[Quarto](https://quarto.org/)
document `project.qmd` that is rendered as
[Markdown](https://quarto.org/docs/authoring/markdown-basics.html)
file `project.md` with accompanying `*.png` figures in
`project_files/figure-markdown/`
using the shell command

```
$ quarto render project.qmd --t markdown
```

## Goals

### Goal of EDA project

- Organize tools by topic (module) & function
- Build Quarto & Markdown environs
- Viz data patterns with `ggplot` ([plotnine](https://plotnine.org/))
- Explore stats to prioritize interesting patterns, not to test
- Collaborate with others to improve & share
- Develop [Shiny modular interactive apps](https://byandell.github.io/Shining-Light-on-data/)
(see my examples in
[Shiny Apps](https://github.com/AttieLab-Systems-Genetics/Documentation/blob/main/ShinyApps.md))

### Broader goal

- Collaborate widely
- Share via self-documented training examples
- Viz data patterns to improve insight
- Explore AI tool environment
- [Evole data as a verb](https://byandell.github.io/Data-Evolve/)

## Package Modules and Functions
  
<details>
<summary>Plot Data</summary>
<br>

Several
[HoloViews](https://holoviews.org/)
and
[GeoViews](https://geoviews.org/)
functions have arisen and are included.
These are cool functions and easy to manipulate or render interactively,
but they generate massive image objects--Mb vs Kb for
[matplotlib.pyplot](https://matplotlib.org/stable/tutorials/pyplot.html)
similar image objects.
In some cases, I have created the simpler objects, in order to generate
simpler `qmd` and `md` pages.


| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| ggplot | coming... |
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
| plot | plot_gdfs_map || plot | plot | Create Row of Plots |
| plot | plot_index || plot | plot | Show plot of index |
| plot | plot_matrix || plot | plot | Plot of model matrix |
| plot | plot_train_test || plot | plot | Plot test fit |
  
</details>
<details>
<summary>Access Data with APIs</summary>
<br>

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| cdcplaces | download_cdc_disease | df | download | CDC Places | Download CDC Disease data |
| cdcplaces | download_census_tract | gdf | download | CDC Places | Download the census tracts |
| cdcplaces | join_tract_cdc | gdf | merge | CDC Places | Join Census Tract and CDC Disease Data |
| cdcplaces | shp_tract_path | str || CDC Places | Set tract path |
| polaris | soil_url_dict | dict | read | POLARIS | Set up soil URLs based on place |
| polaris | merge_soil | da | read | POLARIS | Merge soil data |
| redline | redline_gdf | gdf | read | redline | Read redlining GeoDataFrame from Mapping Inequality |
| redline | redline_mask | gdf || redline | Create new gdf for redlining using regionmask |
| redline | redline_index_gdf | gdf || redline | Merge index stats with redlining gdf into one gdf |
| srtm | srtm_download | da | download | SRTM | Download SRTM data and create da |
| srtm | srtm_slope | da || SRTM | Calculate slope from SRTM data |
| thredds | process_maca | df | read | THREDDS | Process MACA Monthly Data |
| thredds | maca_year | da || THREDDS | Extract and print year data |
  
</details>
<details>
<summary>Explore Data</summary>
<br>

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| explore | index_tree | decision_tree || explore | Convert categories to numbers |
| explore | ramp_logic | da || explore | Fuzzy ramp logic |
| explore | train_test | nparray || explore | Model fit using train and test sets |
| explore | var_trans | df || explore | Variable Selection and Transformation |
  
</details>
<details>
<summary>Set up Data Mechanics</summary>
<br>

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| initial | creata_data_dir | char | mkdir | habitat, bigdata, cluster | Create Data Directory if it does not exist |
| initial | robust_code || setup | Make code robust to interruptions |
| check | header_csv
| check | get_last_row_csv
| check | check_element_in_csv 
| check | check_naip_tracts
| process | da2gdf |
| process | gdf_da_bounds | da ||| Clip bounds from place_gdf on da extended by buffer | 
| process | process_bands | da || process | Process bands from gdf with df metadata |
| process | process_cloud_mask | array || process | Load an 8-bit Fmask file and create a boolean mask |
| process | process_image | da || process | Load, crop, and scale a raster image from earthaccess |
| process | process_metadata | df || process | Create df of raster data URIs from earthaccess metadata |
