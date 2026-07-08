# landmapyr Project Memory

## Project Overview

**landmapyr** is a Python package for land mapping, spatial data analysis, and visualization. It is a companion to the R package [landmapr](https://github.com/byandell-envsys/landmapr), developed alongside the 2024–25 Earth Data Analytics course at CU Boulder's Earth Lab (author: Brian Yandell).

- **Version**: 0.4
- **Install**: `pip install git+https://github.com/byandell-envsys/landmapyr.git`
- **License**: MIT

## Package Structure

Main package lives in `landmapyr/` with 20 modules organized by data source / topic:

| Module | Purpose |
|--------|---------|
| `cdcplaces.py` | CDC disease data & Census tract joins |
| `gbif.py` | GBIF species occurrence data |
| `reflect.py` | Harmonized Landsat-Sentinel satellite reflectance |
| `srtm.py` | SRTM elevation data and slope calculations |
| `thredds.py` | MACA climate projections (THREDDS server) |
| `polaris.py` | POLARIS soil property data |
| `redline.py` | Historical redlining data (Mapping Inequality) |
| `usgs.py` | USGS water monitoring station data |
| `naip.py` | NAIP aerial imagery and NDVI |
| `process.py` | Core raster/vector processing (cloud masking, combining arrays) |
| `explore.py` | Machine learning (decision trees, regression, clustering) |
| `plots.py` | Matplotlib/Seaborn static plotting |
| `hv_plots.py` | HoloViews interactive plotting |
| `gvplot.py` | GeoViews choropleth maps |
| `cached.py` | Caching decorator for expensive computations (pickle) |
| `initial.py` | Project initialization (data directories, robustness settings) |
| `check.py` | CSV validation utilities |
| `legacy.py` | Backward compatibility with deprecation warnings |
| `earthaccess.py` | NASA EarthAccess authentication wrapper |
| `move_images.py` | Image file management utilities |

## Key Dependencies

- **Geospatial**: `geopandas`, `rioxarray`, `cartopy`, `regionmask`
- **Data access**: `earthaccess`, `pygbif`, `dataretrieval`, `pystac-client`
- **Visualization**: `matplotlib`, `seaborn`, `hvplot`, `geoviews`, `holoviews`, `contextily`
- **Data processing**: `xarray`, `xarray-spatial`, `numpy`, `pandas`, `scipy`
- **ML**: `scikit-learn`

## Other Directories

- `docs/` — Quarto (`.qmd`) example projects (madison, buffalo, climate, clustering, sandhill_crane, siberian_crane, big_data, sandhill-crane-migration)
- `notes/` — Development notes and tutorials (fuzzy logic, GBIF, Python classes, project hierarchy)
- `scripts/` — Sample scripts (e.g., USGS White River example)
- `tests/` — Unit tests (`test_lookup.py`, `test_metadata.py`, `verify_qmd_logic.py`); live API calls are skipped in CI
- `test_files/` — Test data
- `strategy.md` — Python coding strategy guide
- `plots.md` — Plotting function documentation

## CI/CD

GitHub Actions runs: `ruff check`, `ruff format`, `mypy landmapyr/`, `pytest tests/`

## Development Patterns

- Decorator-based caching (`cached.py`) for expensive API/compute calls
- `**opts` / `**kwargs` for flexible parameter passing
- Automatic CRS reprojection throughout
- `legacy.py` decorator ensures backward compatibility when functions are refactored
- Modular design: functions organized by data source, not by operation type
