import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pytest
import matplotlib.pyplot as plt
from landmapyr.gbif import count_by_ecoregions, join_occurrence
from landmapyr.plots import plot_occurrence
from landmapyr.hv_plots import hvplot_occurrence


def test_decade_occurrence():
    # 1. Create mock GBIF-like GeoDataFrame
    data = {
        "year": [1982, 1985, 1991, 1999, 2002, 2005, 2012, 2018],
        "month": [5, 6, 7, 8, 9, 10, 11, 12],
        "name": ["A", "B", "C", "D", "E", "F", "G", "H"],
        "ecoregion": [0, 0, 1, 1, 0, 0, 1, 1],
        "geometry": [
            Point(0, 0),
            Point(0, 0),
            Point(1, 1),
            Point(1, 1),
            Point(0, 0),
            Point(0, 0),
            Point(1, 1),
            Point(1, 1),
        ],
    }
    df = pd.DataFrame(data)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    # Count by ecoregions using period='decade'
    occurrence_gdf = count_by_ecoregions(gdf, "ecoregion", "name", "decade")

    # Verify 'decade' is in index names
    assert "decade" in occurrence_gdf.index.names

    # The unique decade values should be 1980, 1990, 2000, 2010
    decades = occurrence_gdf.index.get_level_values("decade").unique()
    assert set(decades) == {1980, 1990, 2000, 2010}

    # 2. Join ecoregions with occurrence to test plotting
    ecoregions_data = {
        "name": ["reg1", "reg2"],
        "area": [100.0, 200.0],
        "geometry": [Point(0, 0).buffer(0.1), Point(1, 1).buffer(0.1)],
    }
    ecoregions_gdf = gpd.GeoDataFrame(
        ecoregions_data, geometry="geometry", crs="EPSG:4326"
    )
    ecoregions_gdf.index.name = "ecoregion"

    joined_gdf = join_occurrence(ecoregions_gdf, occurrence_gdf)

    # 3. Test plot_occurrence won't fail (mock show to prevent blocking)
    plt.show = lambda: None

    try:
        plot_occurrence(joined_gdf, "decade")
        plot_occurrence(joined_gdf, "decade", ncols=1)
    except Exception as e:
        pytest.fail(f"plot_occurrence failed: {e}")

    # 4. Test hvplot_occurrence won't fail
    try:
        hvplot_occurrence(joined_gdf, "decade")
    except Exception as e:
        pytest.fail(f"hvplot_occurrence failed: {e}")
