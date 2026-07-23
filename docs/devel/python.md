---
title: "Python Technical Developer Guide"
author: "Brian Yandell"
date: "2026-07-23"
format: html
---

# Python Technical Developer Guide

This document serves as the extended technical developer guide for the **`landmapyr`** Python package. It details internal data flow pipelines, array manipulation logic, machine learning workflows, visualization wrappers, caching decorators, and testing standards.

---

## 1. Overview & Installation

`landmapyr` is designed for environment and land mapping analysis using modern Python spatial libraries (`xarray`, `rioxarray`, `geopandas`, `scikit-learn`, `cartopy`).

### Developer Setup

```bash
git clone https://github.com/byandell-envsys/landmapyr.git
cd landmapyr
pip install -e ".[dev]"
```

Dependencies are declared in [`pyproject.toml`](file:///Users/brianyandell/Documents/GitHub/landmapyr/pyproject.toml).

---

## 2. Core Spatial Processing Pipeline (`process.py`)

The [`process.py`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/process.py) module is the foundational raster engine of `landmapyr`. Higher-level integration modules (`srtm`, `thredds`, `polaris`) depend on its array clipping and masking utilities.

### Key Functions

- `clip_gdf_da_bounds(gdf, da)`: Clips a `rioxarray.DataArray` `da` to the bounding box of a `geopandas.GeoDataFrame` `gdf`, ensuring CRS alignment via `da.rio.reproject_match()` or `gdf.to_crs()`.
- `cloud_mask(da, qa_band)`: Applies cloud and shadow bitmask filtering to reflectance DataArrays using QA band flags.
- `combine_arrays(da_list)`: Merges spatial `xarray.DataArray` objects along coordinate bounds, aligning pixel grids.

```python
import geopandas as gdf
from landmapyr.process import clip_gdf_da_bounds

# Example usage
clipped_da = clip_gdf_da_bounds(my_gdf, my_data_array)
```

---

## 3. Data Ingestion & API Modules

`landmapyr` provides specialized interfaces for environmental data providers:

### NASA EarthAccess & Surface Reflectance (`earthaccess.py`, `reflect.py`)
- `earthaccess.py` wraps `earthaccess` authentication and granule queries for NASA datasets (such as Harmonized Landsat-Sentinel HLS).
- `reflect.py` downloads HLS tiles, applies cloud masking, and caches results to local disk using `@cached_result`.

### Soil, Climate & Elevation (`polaris.py`, `thredds.py`, `srtm.py`)
- `polaris.py`: Queries POLARIS 30m soil property tiles (pH, organic matter, clay, sand, silt) and clips rasters using `process.clip_gdf_da_bounds`.
- `thredds.py`: Subsets MACA climate projections via THREDDS NetCDF OPeNDAP servers.
- `srtm.py`: Fetches SRTM 30m elevation tiles, computes terrain slope and aspect using `xarray-spatial` or `scipy.ndimage`.

### Species & Water Data (`gbif.py`, `usgs.py`, `cdcplaces.py`, `redline.py`, `naip.py`)
- `gbif.py`: Queries GBIF API via `pygbif`, filters species occurrences by coordinate uncertainty, and returns a spatial `GeoDataFrame`.
- `usgs.py`: Interfaces with USGS NWIS via `dataretrieval`, building streamflow time series and interactive HoloViews charts.
- `cdcplaces.py`: Downloads CDC PLACES census tract health data and performs spatial joins with tract boundaries.
- `redline.py`: Fetches historical HOLC redlining polygons from Mapping Inequality.
- `naip.py`: Searches NAIP aerial imagery STAC endpoints and calculates NDVI rasters (`(NIR - Red) / (NIR + Red)`).

---

## 4. Machine Learning & Statistical Modeling (`explore.py`)

The [`explore.py`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/explore.py) module bridges spatial raster arrays and `scikit-learn` models:

- **Data Reshaping**: Converts 2D/3D `xarray.DataArray` stacks into 2D feature matrices (`n_samples`, `n_features`), dropping NaNs.
- **Decision Trees & Regression**: Fits `DecisionTreeRegressor` or `LinearRegression` on environmental predictor layers (e.g. elevation, climate, soil) against target variables.
- **Clustering**: Applies `KMeans` or spatial clustering to multi-spectral raster layers and reconstructs clustered 2D spatial rasters.

---

## 5. Visualization Architecture

`landmapyr` offers three distinct plotting modules depending on rendering requirements:

1. **Static Plots ([`plots.py`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/plots.py))**:
   - Built on `matplotlib`, `cartopy`, and `contextily`.
   - Provides automatic map projection setup (`ccrs.PlateCarree()`, `ccrs.Mercator()`) and background map tile basemaps (Stamen, OpenStreetMap).

2. **Interactive HoloViews ([`hv_plots.py`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/hv_plots.py))**:
   - Built on `hvplot` and `holoviews`.
   - Generates interactive zoomable raster images (`hvplot.quadmesh`) and vector overlays.

3. **GeoViews Choropleths ([`gvplot.py`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/gvplot.py))**:
   - Generates interactive spatial choropleth maps (`geoviews.Polygons`) for polygon datasets like census tracts or redlining maps.

---

## 6. Caching & Deprecation Management

### Disk Caching (`cached.py`)
- Uses Python `pickle` serialization to cache expensive spatial API downloads or computations in `~/.landmapyr_cache` or local project data directories.
- Decorator `@cached_result` computes a hash of function inputs and reloads precomputed results on subsequent invocations.

### Deprecation Decorator (`legacy.py`)
- Decorator `create_deprecated_alias(new_func, old_name, new_name)` allows smooth function renaming while issuing a `DeprecationWarning` to users.

---

## 7. Testing & Quality Assurance

The test suite lives in `tests/`:

- **Unit Tests**: Test data transformations, array clipping, and logic in isolation.
- **API Tests**: Network-dependent tests (e.g. GBIF, USGS, NASA) use `pytest.mark.skip` or offline test data in `test_files/` during CI execution.

Run the test suite:
```bash
pytest tests/
```

Check formatting and types:
```bash
ruff check .
ruff format --check .
mypy landmapyr/
```
