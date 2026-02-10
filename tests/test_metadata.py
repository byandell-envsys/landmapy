import dataretrieval.nwis as nwis
import pandas as pd

def test_metadata(site_id):
    print(f"Fetching metadata for site: {site_id}")
    try:
        # seriesCatalogOutput=True should provide parameters and date ranges
        df, meta = nwis.get_info(sites=site_id, seriesCatalogOutput=True)
        if not df.empty:
            print("Found series catalog:")
            # Filter for relevant columns: parm_cd, begin_date, end_date
            # Note: columns might vary based on siteOutput
            cols = ['parm_cd', 'begin_date', 'end_date', 'data_type_cd', 'count_nu']
            available_cols = [c for c in cols if c in df.columns]
            print(df[available_cols].head(20))
        else:
            print("No metadata found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_metadata("06446000")
