# `landmapyr` Developer Guides & Planning Record

This document consolidates the blueprint prompts, approved implementation plan, and execution walkthrough for establishing the Developer Guide architecture in the `landmapyr` repository.

---

## 1. Blueprint Prompts

*Source: [`Documentation/prompts/devel_guide.md#hybrid-r--python-projects`](https://github.com/byandell/Documentation/blob/main/prompts/devel_guide.md#hybrid-r--python-projects)*

### Hybrid R & Python Projects Blueprint

In research repositories (like `geyser` or `landmapyr`), R and Python code sit side-by-side. The developer guide must reconcile both ecosystems, outlining boundaries and interfaces.

#### Three-Tier Documentation Strategy

1. **Root Repository Guide (`DEVELOPER.md`)**: Primary entry point for developers. Documents shared architecture, cross-language module mappings, execution entry points, setup commands (`pip install -e .` and `devtools::load_all()`), and data routing.
2. **R Package Sub-Guide (`vignettes/DeveloperGuide.qmd`)**: Master vignette for R package compilation and articles rendering. Focuses on R spatial packages (`terra`, `stars`, `sf`), `roxygen2` documentation, and `testthat` testing.
3. **Python Package Sub-Guide (`docs/devel/python.md` & `landmapyr/README.md`)**: Housed in `docs/devel/python.md` for web/Quarto site rendering and `landmapyr/README.md` as an in-source developer reference for Python package developers.
4. **Planning & Execution Record (`guides.md`)**: Consolidates initial blueprint prompts, implementation plan, and execution walkthrough for auditability.

---

## 2. Implementation Plan

*Approved Plan for `landmapyr` Developer Guide*

### Overview & Objectives
`landmapyr` is a dual-ecosystem project featuring an active Python package (v0.4, 20 modules) and planned R translation (`landmapr` in `R/`).

The goals are:
1. Create a primary **`DEVELOPER.md`** file in the repository root acting as the developer architecture entry point for both Python and planned R codebases.
2. Establish a clear dual-housing strategy for language-specific sub-guides:
   - **Python Sub-Guides**: `docs/devel/python.md` (site rendering) and `landmapyr/README.md` (in-source reference).
   - **Planned R Sub-Guides**: `vignettes/DeveloperGuide.qmd` (R vignette) and `R/README.md` (in-source reference).
3. Update `README.md` to reference `DEVELOPER.md` and `guides.md`.

---

## 3. Walkthrough & Execution Record

*Completed Work Summary & Verification*

### Summary of Created & Updated Files

1. **[`DEVELOPER.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/DEVELOPER.md)**:
   - Master root architecture guide detailing the 3-level module hierarchy for Python (`cached`, `process`, `earthaccess`, `check`, `cdcplaces`, `gbif`, `redline`, `usgs`, `naip`, `explore`, `plots`, `hv_plots`, `gvplot`, `initial`, `srtm`, `thredds`, `polaris`, `reflect`, `legacy`, `__init__`).
   - Planned R translation strategy (`landmapr` in `R/`) based on `notes/transR.md`, `notes/hierarchy.md`, and `notes/transCritic.md`.
   - Side-by-side R vs. Python dependency and function cross-reference table.
   - Spatial data pipelines (`xarray`, `rioxarray`, `geopandas`), API interfaces, caching (`cached.py`), and test setup (`pytest`, `ruff`, `mypy`).

2. **[`guides.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/guides.md)**:
   - Consolidated record of prompts, implementation plan, and walkthrough.

3. **[`docs/devel/python.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/docs/devel/python.md)**:
   - Extensive Python technical developer guide rendered on the Quarto site.

4. **[`landmapyr/README.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/README.md)**:
   - Sub-directory developer reference inside the Python package source directory.

5. **[`vignettes/DeveloperGuide.qmd`](file:///Users/brianyandell/Documents/GitHub/landmapyr/vignettes/DeveloperGuide.qmd)**:
   - Planned R package developer guide vignette documenting R spatial package standards (`terra`, `stars`, `sf`, `mapview`), `roxygen2`, `testthat`, and translation hierarchy.

6. **[`R/README.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/R/README.md)**:
   - In-source developer reference for the planned `R/` source folder.

7. **[`README.md`](file:///Users/brianyandell/Documents/GitHub/landmapyr/README.md)**:
   - Updated with direct links to `DEVELOPER.md` and `guides.md`.

---

## Document Links

- 📘 [Root Developer Guide (`DEVELOPER.md`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/DEVELOPER.md)
- 🐍 [Python Developer Guide (`docs/devel/python.md`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/docs/devel/python.md)
- 📦 [Python Package Source Reference (`landmapyr/README.md`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/README.md)
- 📖 [Planned R Vignette Guide (`vignettes/DeveloperGuide.qmd`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/vignettes/DeveloperGuide.qmd)
- 🛠️ [Planned R Package Source Reference (`R/README.md`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/R/README.md)
- 🏠 [Repository README (`README.md`)](file:///Users/brianyandell/Documents/GitHub/landmapyr/README.md)
