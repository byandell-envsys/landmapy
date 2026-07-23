# `landmapyr/` Package Source Directory

This directory contains the Python source code for the **`landmapyr`** package (version 0.4).

---

## Source Module Index

The package consists of 20 modules organized in a 3-level dependency hierarchy:

### Level 1: Foundation Modules (No Internal Imports)
- [`cached.py`](cached.py): Disk caching decorator (`@cached_result`) using `pickle`.
- [`process.py`](process.py): Core raster operations (`clip_gdf_da_bounds`, `cloud_mask`, `combine_arrays`).
- [`earthaccess.py`](earthaccess.py): NASA EarthAccess authentication and granule retrieval.
- [`check.py`](check.py): CSV header and data validation utilities.
- [`cdcplaces.py`](cdcplaces.py): CDC PLACES health data downloads and tract spatial joins.
- [`gbif.py`](gbif.py): GBIF species occurrence data query and cleaning.
- [`redline.py`](redline.py): Historical HOLC redlining data acquisition.
- [`usgs.py`](usgs.py): USGS NWIS streamflow data retrieval.
- [`naip.py`](naip.py): NAIP aerial imagery STAC search and NDVI calculation.
- [`explore.py`](explore.py): Spatial machine learning models (scikit-learn decision trees, regression, clustering).
- [`plots.py`](plots.py): Matplotlib + Cartopy static mapping.
- [`hv_plots.py`](hv_plots.py): HVPlot + HoloViews interactive spatial visualization.
- [`gvplot.py`](gvplot.py): GeoViews choropleth maps.
- [`initial.py`](initial.py): Environment initialization and directory setup.

### Level 2: Mid-Level Integration Modules
- [`srtm.py`](srtm.py): SRTM elevation and slope analysis (imports `process`).
- [`thredds.py`](thredds.py): MACA climate projection query from THREDDS (imports `process`).
- [`polaris.py`](polaris.py): POLARIS soil property rasters (imports `process`).
- [`reflect.py`](reflect.py): Harmonized Landsat-Sentinel surface reflectance (imports `cached`, `earthaccess`).

### Level 3: Interaction & Legacy
- [`legacy.py`](legacy.py): Deprecation decorator (`create_deprecated_alias`) for backward compatibility.
- [`__init__.py`](__init__.py): Package exports and docstrings.

---

## Developer Guidelines

- **Code Style**: Follow PEP 8 guidelines. Enforced via `ruff check .` and `ruff format .`.
- **Type Hints**: Use type annotations for function signatures. Verified via `mypy landmapyr/`.
- **Docstrings**: Write descriptive docstrings for all exported functions detailing parameters and return types.
- **Testing**: Add corresponding unit tests in `tests/` for new functionality.

For full architectural documentation, refer to the root [DEVELOPER.md](../DEVELOPER.md) and [docs/devel/python.md](../docs/devel/python.md).
