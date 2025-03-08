# landmapy

- [landmapy](#landmapy)
  - [Land Mapping Python Package](#land-mapping-python-package)
    - [Install and Import](#install-and-import)
    - [Collaboration](#collaboration)
  - [Use Cases](#use-cases)
    - [Example use with Habitat Project](#example-use-with-habitat-project)
  - [Goals](#goals)
    - [Goal of EDA project](#goal-of-eda-project)
    - [Broader goal](#broader-goal)
    - [Technical goal](#technical-goal)
  - [Package Modules and Functions](#package-modules-and-functions)

Additional links:

- [References](references.md)
- [Coding Strategy](strategy.md)
- [EDA Notes](notes.md)
  
## Land Mapping Python Package

The `landmapy` package is being built as a complement to the 2024-25
[Earth Data Analytics](https://github.com/byandell-envsys/EarthDataAnalytics)
course taught through the
[Earth Lab](https://earthlab.colorado.edu/).
Special thanks to [Elsa Culler](https://eculler.github.io/) as well as
[Nate Quarderer](https://github.com/nquarder),
[Lilly Jones-Sanovia](https://github.com/yawapi),
[Alison Post](https://akpost21.github.io/),
and
[Katherine Siegel](https://katherinesiegel.github.io/).
I am
[Brian Yandell](https://byandell.github.io/).

Interestingly, Earth Lab members developed a Python package a few years ago,
[earthpy](https://earthpy.readthedocs.io)
([GitHub repo](https://github.com/earthlab/earthpy)).
It seems fairly self-contained, but may have some dated features.
For instance, is uses
[rasterio](https://github.com/rasterio/rasterio),
which seems to now be superceded by
[rioxarray](https://corteva.github.io/rioxarray).
Still there are some interesting and subtle ideas here that are worth exploring.

This is somewhat a companion to my R package
[landmapr](https://github.com/byandell-envsys/landmapr).
They are being developed in parallel, with somewhat different goals.
Right now, focus is on the python package to keep up with the
[Earth Data Analytics](https://github.com/byandell-envsys/EarthDataAnalytics)
course.

### Install and Import

From within python, you can install this package directly
from GitHub:

```
pip install git+https://github.com/byandell-envsys/landmapy.git
```

Then you would use `import landmapy`,
or more likely `from landmapy.<module> import <function>`
to import desired functions.

I for now use my local machine cloned copy of the package in
`~/Documents/GitHub/landmapy` and the python command

```
pip install ~/Documents/GitHub/landmapy
```

### Collaboration

I am happy to collaborate on development of this package.
Please contact me and/or create issues.
If you want to become more involved, contact me, fork the repo,
modify (in a tame way, please) and submit pull requests.

## Use Cases

This python package was begun in nov-dec 2024 as I found
the project tools growing.
EDA staff offered draft code for tools to the class,
which I adapted and expanded, based on their advice.
I learned by doing and looking at other tools,
developing my own
[Coding Strategy](strategy.md).
To date, this package has been used in the following 
[EDA projects](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/README.md#projects)
(with modules other than
[initial](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/initial.py)
and plot modules):

- [Habitat2: Buffalo Grasslands Habitat Suitability](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/climate.md)
  - [polaris](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/polaris.py),
[srtm](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/srtm.py),
[thredds](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/thredds.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Clustering: Classify land cover for Mississippi Delta](https://github.com/earthlab-education/clustering-byandell)
  - [reflect](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/reflect.py)
- [Big-Data: Urban Greenspace and Asthma Prevalence](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data.md)
  - [naip](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/naip.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Habitat: Buffalo Grasslands Habitat Suitability](https://github.com/byandell-envsys/habitatSuitability/blob/main/buffalo.md)
  - [polaris](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/polaris.py),
[srtm](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/srtm.py),
[thredds](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/thredds.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Redlining: Predicting NDVI for Madison](https://github.com/earthlab-education/fundamentals-04-redlining-byandell/blob/main/notebooks/madison.ipynb)
  - [redline](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/redline.py),
[process](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/process.py),
[explore](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/explore.py)
- [Species: Crane Migration Maps](https://github.com/earthlab-education/species-distribution-coding-challenge-byandell)
  - [gbif](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/gbif.py)

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
$ quarto render project.qmd -t markdown
```

Some of these were derived from Python notebooks using the convert command

```
$ quarto convert project.ipynb
```

With care (see `Plot Data` section of
[Package Modules and Functions](#package-modules-and-functions) below),
the resulting markdown `project.md` and `*.png` figures
are compact (Kb, not Mb) and can be pushed to GitHub for ready viewing and sharing.
Note that I set up the
[.gitignore](https://github.com/earthlab-education/big-data-byandell/blob/main/.gitignore)
file to ignore `*_files/` folders;
commenting this line out briefly to enable commiting the png
files (followed by uncommenting `*_files/`) is a handy way
to incorporate figures into the `project.md` once committed and pushed to GitHub.
See in addition further
[References](https://github.com/byandell-envsys/landmapy/blob/main/references.md).

### Example use with Habitat Project

In a sense, this package enables me to off-load pages of code, replacing them by one-line commands. These basically look like `pseudocode`, but are actually functional. For instance, for the Habitat Suitability project last December (and now being revisited), here is the beginning.

First I visited [USFS Geospatial Data Discovery: National Grassland Units (Feature Layer)](https://data-usfs.hub.arcgis.com/datasets/usfs::national-grassland-units-feature-layer/explore) and manually downloaded the GeoJSON file from DataSet into directory `~/earth-analytics/data/habitat`. Then I did the following steps, shown below in code:

```
# Install `landmapy` package.
pip install --quiet git+https://github.com/byandell-envsys/landmapy.git

# Import needed libraries.
import geopandas as gpd # read geojson file into gdf
from landmapy.initial import create_data_dir # create (or retrieve) data directory
from landmapy.plot import plot_gdf_state # plot gdf with state overlay

data_dir = create_data_dir('habitat')
# Read all grasslands GeoJSON into `grassland_gdf`.
grassland_url = f"{data_dir}/National_Grassland_Units_(Feature_Layer).geojson"
grassland_gdf = gpd.read_file(grassland_url)
# Subset to desired locations.
buffalo_gdf = grassland_gdf.loc[grassland_gdf['GRASSLANDNAME'].isin(
        ["Buffalo Gap National Grassland", "Oglala National Grassland"])]
plot_gdf_state(buffalo_gdf)
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
- [Evolve data as a verb](https://byandell.github.io/Data-Evolve/)

### Technical goal

- Rationalize plots more
  - Fewer routines that are more flexible
  - plot, hvplot/gvplot analogs
  - ggplot widgets to visualize relationships
  - overlays, side-by-side, over time movies/sliders
- Better grasp of moving between da, df, gdf, other
  - Should lead to simpler plot options
- Algebra on images
  - visualize in lat/lon/elev space
  - explore multiple measurements

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
In some cases, I have created simpler plot functions to generate
simpler `qmd` and `md` pages. For instance

```
#| label: fig-resid
from landmapy.plot import plot_gdfs_map
plot_gdfs_map(logndvi_cdc_gdf, column=['asthma','resid','edge_density'], color=['Blues','RdBu','Greens'])
```

generates a small (168Kb) named figure,
[big-data_files/figure-markdown/fig-resid-output-1.png](https://github.com/earthlab-education/big-data-byandell/blob/main/big-data_files/figure-markdown/fig-resid-output-1.png)
with optional accompanying figure caption (via a line `#| fig-cap: "Blah Blah"`).
An alternative is the fancier GeoViews/HoloViews,
which generates a larger (Mb) object that is embedded in the Markdown,
making it too big to render on GitHub. Here is that code:

```
import holoviews as hv
from landmapy.gvplot import gvplot_ndvi_index, gvplot_resid

model_fit = gvplot_ndvi_index(ndvi_cdc_gdf)
resid = gvplot_resid(logndvi_cdc_gdf, reg, yvar='asthma')
models_gv = (model_fit[0] + resid + model_fit[1])
hv.save(models_gv, 'bigdata_model.html')
```

Below are current plot functions:

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| ggplot | coming... |
| gvplot | gvplot_gdf | gvplot | plot | plot | Plot asthma data as chloropleth |
| gvplot | gvplot_chloropleth | gvplot | plot | plot | Generate a chloropleth with the given color column |
| gvplot | gvplot_ndvi_index | gvplot | plot | plot | Plot NDVI and CDC data |
| gvplot | gvplot_resid | gvplot | plot | plot | Plot model residual |
| hvplot | hvplot_cluster || hvplot | plot | Plot of RGB and Clusters |
| hvplot | hvplot_delta_gdf | hvplot | plot | plot | HV Plot Delta GDF |
| hvplot | hvplot_matrix | hvplot | plot | plot | Plot of model matrix |
| hvplot | hvplot_tract_gdf | hvplot | plot | plot | Plot census tracts with satellite imagery background |
| hvplot | hvplot_train_test | hvplot | plot | plot | Plot test fit |
| hvplot | hvplot_index_grade | hvplot | plot | plot | Plots for index and grade |
| hvplot | hvplot_index_pred | hvplot | plot | plot | Plot the model results |
| plot | plot_cluster || plot | plot | Plot of RGB and Clusters |
| plot | plot_delta_gdf | plot | plot | plot | HV Plot Delta GDF |
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
| gbif | count_monthly_ecoregions | gdf || GBIF | Count the observations in each ecoregion each month |
| gbif | count_yearly_ecoregions | gdf || GBIF | Count the observations in each ecoregion each year |
| gbif | download_gbif | str | download | GBIF | Download GBIF Entries as CSV file (only once) |
| gbif | ecoregions | gdf || GBIF | Get ecoregion boundary as gdf |
| gbif | gbif_credentials || environ | GBIF | Set up GBIF Credentials |
| gbif | gbif_monthly | gdf || GBIF | Extract monthly data as gdf |
| gbif | gbif_species_key | str || GBIF | Get GBIF Species Key |
| gbif | join_ecoregions_monthly | gdf || GBIF | Join ecoregions with monthly gbif data for species |
| gbif | join_occurrence | gdf || GBIF | Join Ecoregions and Occurrence |
| gbif | load_gbif | df || GBIF | Load the GBIF data |
| gbif | simplify_ecoregions_gdf | gdf || GBIF | Create a simplified GeoDataFrame for plot |
| polaris | merge_soil | da | read | POLARIS | Merge soil data |
| polaris | soil_url_dict | dict | read | POLARIS | Set up soil URLs based on place |
| redline | redline_gdf | gdf | read | redline | Read redlining GeoDataFrame from Mapping Inequality |
| redline | redline_index_gdf | gdf || redline | Merge index stats with redlining gdf into one gdf |
| redline | redline_mask | gdf || redline | Create new gdf for redlining using regionmask |
| reflect | compute_reflectance_da | function || reflect | Connect to files over VSI, crop, cloud mask, and wrangle |
| reflect | merge_and_composite_arrays | function || reflect | Merge and Composite Arrays |
| reflect | read_delta_gdf | gdf | read | delta | Read Delta WBD using cache decorator |
| reflect | read_wbd_file | gdf | read | eelta |  Read WBD File using cache key |
| reflect | reflectance_kmeans | df || reflect | KMeans Clusters for Reflectance Bands |
| reflect | reflectance_range | df || reflect | Check ranges of bands |
| reflect | reflectance_rgb | da || reflect | RGB saturation of reflectance |
| srtm | srtm_download | da | download | SRTM | Download SRTM data and create da |
| srtm | srtm_slope | da || SRTM | Calculate slope from SRTM data |
| thredds | maca_year | da || THREDDS | Extract and print year data |
| thredds | process_maca | df | read | THREDDS | Process MACA Monthly Data |
  
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

Initial module is useful for beginning of project.
Process module has various mechanics that might belong elsewhere but seem broad in scope.
Cached module is a
[decorator](https://www.geeksforgeeks.org/decorators-in-python/)
used in
[reflect.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/reflect.py)
to simplify caching of time-expensive objects
(see
[EDA Reference Python Coding: Decorators](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/references.md#decorators)
for references).
Check module is for checking parts of objects, at this point CSVs.

| module | function | return | effect | project | description |
|--------|----------|--------|--------|---------|-------------|
| initial | creata_data_dir | char | mkdir || Create Data Directory if it does not exist |
| initial | robust_code || setup || Make code robust to interruptions |
| cached | cached | function | decorator | reflect | A decorator to cache function results |
| check | header_csv | str ||| Header of CSV file |
| check | get_last_row_csv | str ||| Check Last Row of CSV File |
| check | check_element_in_csv | bool ||| Check value of element in CSV file | 
| check | check_naip_tracts | df || NAIP | Check if NAIP tracts stored |
| process | da2gdf | gdf ||| Convert a DataArray to a GeoDataFrame using rioxarray and geopandas |
| process | clip_gdf_da_bounds | da ||| Clip bounds from place_gdf on da extended by buffer | 
| process | process_bands | da || process | Process bands from gdf with df metadata |
| process | process_cloud_mask | array || process | Load an 8-bit Fmask file and create a boolean mask |
| process | process_image | da || process | Load, crop, and scale a raster image from earthaccess |
| process | process_metadata | df || process | Create df of raster data URIs from earthaccess metadata |
