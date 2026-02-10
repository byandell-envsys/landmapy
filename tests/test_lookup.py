import dataretrieval.nwis as nwis
import pandas as pd

def test_lookup(name, state=None):
    print(f"Searching for: {name} in state {state}")
    try:
        # Try with siteName and siteNameMatchOperator
        df, meta = nwis.what_sites(siteName=name, stateCd=state, siteNameMatchOperator='contains')
        if not df.empty:
            print("Found:")
            print(df[['site_no', 'station_nm', 'dec_lat_va', 'dec_long_va']].head())
        else:
            print("No sites found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_lookup("WHITE RIVER%", state="SD")
