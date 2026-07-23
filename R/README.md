# `R/` Package Source Directory (`landmapr`)

This directory is designated for the planned R translation (**`landmapr`**) of the `landmapyr` Python package.

> [!NOTE]
> **Status**: R source code translation is planned. No R code has been committed yet.

---

## Planned R Module Structure

Modules will be translated from Python to R in 4 stages based on [`notes/hierarchy.md`](../notes/hierarchy.md) and [`notes/transR.md`](../notes/transR.md):

| Stage | Planned R File | Python Source Module | Key R Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | `process.R` | `process.py` | `terra`, `stars`, `sf` | Planned |
| **Stage 1** | `cached.R` | `cached.py` | `memoise`, `base` | Planned |
| **Stage 1** | `check.R` | `check.py` | `readr`, `dplyr` | Planned |
| **Stage 2** | `srtm.R` | `srtm.py` | `terra` | Planned |
| **Stage 2** | `thredds.R` | `thredds.py` | `stars`, `ncdf4` | Planned |
| **Stage 2** | `polaris.R` | `polaris.py` | `terra` | Planned |
| **Stage 2** | `reflect.R` | `reflect.py` | `terra`, `httr2` | Planned |
| **Stage 3** | `gbif.R` | `gbif.py` | `rgbif`, `sf` | Planned |
| **Stage 3** | `usgs.R` | `usgs.py` | `dataRetrieval`, `sf` | Planned |
| **Stage 3** | `cdcplaces.R` | `cdcplaces.py` | `sf`, `dplyr` | Planned |
| **Stage 3** | `redline.R` | `redline.py` | `sf` | Planned |
| **Stage 4** | `plots.R` | `plots.py` | `ggplot2`, `ggspatial` | Planned |
| **Stage 4** | `hv_plots.R` | `hv_plots.py` / `gvplot.py` | `mapview`, `leaflet` | Planned |

---

## Coding Rules for R Contributors

1. **Assignment**: Always use `<-` for assignment, never `=`.
2. **Explicit Namespaces**: Call package functions using `package::function()` syntax.
3. **Documentation**: Write **Roxygen2** comments (`#'`) above every exported function.
4. **Testing**: Add unit tests in `tests/testthat/test-<module>.R` using `testthat`.

Refer to [vignettes/DeveloperGuide.qmd](../vignettes/DeveloperGuide.qmd) and [DEVELOPER.md](../DEVELOPER.md) for full architectural guidelines.
