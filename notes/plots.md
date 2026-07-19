# Documentation of Improvements to Static and Dynamic Plots

**Prompt:**
What improvements have been made to the static and dynamic plotting routines in `landmapyr`? Document the additions, fixes, and visual alignment between static and dynamic visualizations.

**Response:**

The visualization capabilities in the `landmapyr` package have been upgraded to provide better visual consistency between static (Matplotlib/contextily) and dynamic (HoloViews/GeoViews) maps, and to correct scale representation bugs in statistical diagnostics.

## 1. Additions to Static Plots

* **`plot_tract_gdf(place_tract_gdf)`**: Added a new static plotting function to [plots.py](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/plots.py) that mirrors the styling of the dynamic `hvplot_tract_gdf` function.
  * **Visual Style**: Renders tract boundaries with a transparent fill (`facecolor="none"`) and orange edges (`edgecolor="orange"`).
  * **Basemap**: Overlays the vector boundaries on an ESRI World Imagery satellite base map using `contextily` (`ctx.providers.Esri.WorldImagery`).
  * **Usage**: Ideal for rendering static figures of census tracts on satellite backgrounds without needing external health columns.

## 2. Improvements to Dynamic Plots

* **Background Map Integration in `gvplot_chloropleth`**: Previously, the dynamic GeoViews maps produced by `gvplot_ndvi_index` and `gvplot_resid` lacked background tiles.
  * **Improvement**: Modified `gvplot_chloropleth()` in [gvplot.py](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/gvplot.py) to multiply all generated polygons by OpenStreetMap tiles (`gv.tile_sources.OSM`).
  * **Effect**: Ensures that every dynamically generated panel displays a clear base map, matching the OpenStreetMap basemaps used in static multipanel plots.

## 3. Scale and Colormap Alignment for Residual Plots

* **Scale Mismatch Bug Fix in `train_test`**:
  * **Issue**: The residual calculation in `train_test()` within [explore.py](file:///Users/brianyandell/Documents/GitHub/landmapyr/landmapyr/explore.py) was subtracting the log-scale actual target (`log_asthma`, values ~2) from the exponentiated prediction (`pred`, original scale, values ~10). This produced residuals of ~8, saturating both the static colormap and the dynamic GeoViews colormap (range hardcoded to `[-0.3, 0.3]`).
  * **Fix**: Aligned the scales by calculating residuals entirely on the log scale:
    ```python
    model_df["resid"] = np.log(model_df["pred"]) - model_df[f"{trans}_{resp}"]
    ```
  * **Effect**: Residual values now correctly fit within the `[-0.3, 0.3]` range, centering at `0`, which lets diverging colormaps (like `RdBu`) display positive and negative spatial bias patterns correctly instead of saturating.

## Summary of Plotting Routines

| Routine | Type | Background / Base Tile | Styling |
| :--- | :--- | :--- | :--- |
| `plot_tract_gdf` | Static | ESRI World Imagery | Orange boundaries, transparent fill |
| `gvplot_chloropleth` | Dynamic | OpenStreetMap (OSM) | Configurable chloropleth overlay |
| `gvplot_resid` | Dynamic | OpenStreetMap (OSM) | Residual diagnostic on log scale with `RdBu` cmap |
| `plot_gdf_state` | Static | OpenStreetMap (OSM) | Overlay with state boundaries |
| `plot_gdfs_map` | Static | OpenStreetMap (OSM) | Multi-panel choropleth side-by-side |
