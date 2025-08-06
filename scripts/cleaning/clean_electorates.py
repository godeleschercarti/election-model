from typing import Callable
import pandas as pd

from constants.constants import *

def clean_modern(year:int) -> pd.DataFrame:
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals', 'Māori Electorate Totals', 'Combined Totals']
    COLS_TO_KEEP = ['Electoral District', 'Valid Total (a)+(b)', 'Electors on Master Roll' , 'Electoral Population']
    ELEC_COLS_TO_KEEP = ['Valid Total (a)+(b)']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/party-votes-and-turnout-by-electorate.csv", skiprows=3)
    df = df.drop(0)
    df = df[~df['Electoral District'].isin(TOTALS_COLS)]
    df.reset_index(drop=True, inplace=True)
    df = df[COLS_TO_KEEP]

    edf = pd.read_csv(f"{RAW_DATA_PATH}/{year}/candidate-votes-and-turnout-by-electorate.csv", skiprows=3)
    edf = edf.drop(0)
    edf = edf[~edf['Electoral District'].isin(TOTALS_COLS)]
    edf.reset_index(drop=True, inplace=True)
    df.insert(2, "electorate", pd.Series(edf[ELEC_COLS_TO_KEEP[0]].array, index=df.index))

    return df

def clean_old(year:int):
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals  Inclusive of Tangata Whenua Votes', 'Combined Totals']
    COLS_TO_KEEP = ['Electoral District', 'Valid Total (a)+(b)', 'Electors on Master Roll' , 'Electoral Population']
    ELEC_COLS_TO_KEEP = ['Valid Total (a)+(b)']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/party-votes-and-turnout-by-electorate.csv", skiprows=3, header=1)
    df = df.drop(0)
    df = df[~df['Electoral District'].isin(TOTALS_COLS)]
    df = df[~df['Electoral District'].isna()]
    df.reset_index(drop=True, inplace=True)
    df = df[COLS_TO_KEEP]

    edf = pd.read_csv(f"{RAW_DATA_PATH}/{year}/candidate-votes-and-turnout-by-electorate.csv", skiprows=3, header=1)
    edf = edf.drop(0)
    edf = edf[~edf['Electoral District'].isin(TOTALS_COLS)]
    edf = edf[~edf['Electoral District'].isna()]
    edf.reset_index(drop=True, inplace=True)
    df.insert(2, "electorate", pd.Series(edf[ELEC_COLS_TO_KEEP[0]].array, index=df.index))

    return df

def process_df(year:int, df:pd.DataFrame) -> pd.DataFrame:
    if len(df.columns) != 5: raise Exception("Wrong number of columns in df!")
    boundary_year = max([x for x in BOUNDARY_YEARS if x <= year])

    df.insert(0, "electorate_id", f"{boundary_year}_" + df.index.astype(str).str.zfill(2))
    df.insert(0, "year", year)
    df.columns = pd.Index(["year", "electorate_id", "electorate_name", "party_votes", "candidate_votes", "registered_voters", "total_voters"])

    NUMERIC_COLS = ["party_votes", "candidate_votes", "registered_voters", "total_voters"]

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col].str.replace(",", ""))

    return df

CLEAN_FUNCTIONS: dict[int, Callable[[int], pd.DataFrame]] = {
    2023: clean_modern,
    2020: clean_modern,
    2017: clean_modern,
    2014: clean_modern,
    2011: clean_modern,
    2008: clean_modern, 
    2005: clean_modern, 
    2002: clean_modern,
    1999: clean_old
}

def do_cleaning() -> None:
    for year in ELECTION_YEARS:
        clean_function = CLEAN_FUNCTIONS[year]
        df = clean_function(year)
        processed_df = process_df(year, df)
        processed_df.to_csv(f"{DATA_PATH}/{year}/electorates.csv")

do_cleaning()