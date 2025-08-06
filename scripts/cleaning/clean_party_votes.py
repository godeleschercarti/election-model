from typing import Callable
import pandas as pd

from constants.constants import *

def clean_modern(year:int) -> pd.DataFrame:
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals', 'Māori Electorate Totals', 'Combined Totals']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/votes-for-registered-parties-by-electorate.csv", skiprows=1)
    df = df[~df["Electorate"].isin(TOTALS_COLS)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop(columns=["Informal Party Votes", "Total Party Votes Counted", "Total Valid Party Votes"])

    return df

def clean_key(year:int) -> pd.DataFrame:
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals', 'Māori Electorate Totals', 'Combined Totals']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/votes-for-registered-parties-by-electorate.csv", skiprows=1)
    df = df.rename(columns={df.columns[0]: "Electorate"})
    df = df.drop(0)
    df = df[~df["Electorate"].isin(TOTALS_COLS)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop(columns=["Informal Party Votes", "Total Valid Party Votes"])

    return df

def clean_clark(year:int) -> pd.DataFrame:
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals', 'Māori Electorate Totals', 'Combined Totals']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/votes-for-registered-parties-by-electorate.csv", skiprows=1, encoding="latin1")
    df = df.rename(columns={df.columns[0]: "Electorate"})
    df = df.drop(0)
    df = df[~df["Electorate"].isin(TOTALS_COLS)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop(columns=["Informal Party Votes", "Total Valid Party Votes"])

    return df

def clean_bolger(year:int) -> pd.DataFrame:
    TOTALS_COLS = ['General Electorate Totals', 'Maori Electorate Totals Including Tangata Whenua Votes', 'Combined Totals']

    df = pd.read_csv(f"{RAW_DATA_PATH}/{year}/votes-for-registered-parties-by-electorate.csv", skiprows=1, encoding="latin1")
    df = df.rename(columns={df.columns[0]: "Electorate"})
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    df = df.drop(columns=unnamed_cols)
    df = df.drop(0)
    df = df[~df["Electorate"].isin(TOTALS_COLS)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop(columns=["Total Valid Votes"])

    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", "")
        df[col] = pd.to_numeric(df[col])
    return df

def process_df(year:int, df:pd.DataFrame) -> pd.DataFrame:
    df = pd.melt(df, id_vars=["Electorate"], var_name="party", value_name="votes")
    df['party'] = df['party'].str.replace(r'[^A-Za-z0-9 ]', '', regex=True)
    df['party'] = df['party'].str.lower().map(PARTY_ABBREVIATIONS_LOWER)
    df['party'] = df['party'].fillna('MIN')

    df = df.groupby(['Electorate', 'party'], as_index=False).agg({'votes': 'sum'})
    edf = pd.read_csv(f"{DATA_PATH}/{year}/electorates.csv", index_col=0)
    edf = edf[['electorate_id', 'electorate_name', 'party_votes']]
    
    df = df.merge(edf, left_on='Electorate', right_on='electorate_name', how="left")
    df["percentage"] = df['votes']/df['party_votes']
    df["year"] = year
    df = df.drop(columns=['electorate_name', 'party_votes'])
    df.columns = pd.Index(['electorate_name', 'party', 'votes', 'electorate_id', 'percentage', 'year'])
    df = df[['year', 'electorate_id', 'electorate_name', 'party', 'votes', 'percentage']]
    df = df.reset_index(drop=True)
    return df


CLEAN_FUNCTIONS: dict[int, Callable[[int], pd.DataFrame]] = {
    2023: clean_modern,
    2020: clean_modern,
    2017: clean_modern,
    2014: clean_key,
    2011: clean_key,
    2008: clean_key, 
    2005: clean_clark, 
    2002: clean_clark,
    1999: clean_bolger,
}

def do_cleaning() -> None:
    for year in ELECTION_YEARS:
        clean_function = CLEAN_FUNCTIONS[year]
        df = clean_function(year)
        processed_df = process_df(year, df)
        processed_df.to_csv(f"{DATA_PATH}/{year}/party-votes.csv")

do_cleaning()
