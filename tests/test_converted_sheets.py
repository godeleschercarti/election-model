import pandas as pd

from constants.constants import *

def test_electorate_sheets():
     for year in ELECTION_YEARS:
        df = pd.read_csv(f"{DATA_PATH}/{year}/electorates.csv", index_col=0)
        assert df.columns.tolist() == ["year", "electorate_id", "electorate_name", "party_votes", "candidate_votes", "registered_voters", "total_voters"]

def test_electorate_cycle_consistency():
    for cycle in CYCLES:
        ldf = pd.read_csv(f"{DATA_PATH}/{cycle[0]}/electorates.csv", index_col=0)
        rdf = pd.read_csv(f"{DATA_PATH}/{cycle[1]}/electorates.csv", index_col=0)
        ldf = ldf.merge(rdf, on="electorate_id", how="inner")
        assert (ldf["electorate_name_y"] == rdf["electorate_name"]).all()
