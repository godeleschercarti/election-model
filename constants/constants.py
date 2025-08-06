RAW_DATA_PATH = "data/raw"
DATA_PATH = "data/clean"

ELECTION_YEARS = [2023, 2020, 2017, 2014, 2011, 2008, 2005, 2002, 1999]
BOUNDARY_YEARS = [2020, 2014, 2008, 2002, 1996]
CYCLES = [(2023, 2020), (2017, 2014), (2011, 2008), (2005, 2002)]

ELECTORATES_NUM = {
    2023: 72,
    2020: 72,
    2017: 71,
    2014: 71,
    2011: 70,
    2008: 70,
    2005: 69,
    2002: 69,
    1999: 67,
    1996: 67,
}

MAJOR_PARTIES:dict[str, list[int]] = {
    "NAT": list(range(1996, 2023+1, 3)),
    "LAB": list(range(1996, 2023+1, 3)),
    "GRN": list(range(1996, 2023+1, 3)),
    "ACT": list(range(1996, 2023+1, 3)),
    "NZF": list(range(1996, 2023+1, 3)),
    "TPM": list(range(2002, 2023+1, 3)),
    "TOP": list(range(2017, 2023+1, 3)),
    "CON": list(range(2011, 2023+1, 3)),
    "UNF": list(range(1996, 2017+1, 3)),
    "ALL": list(range(1996, 2011+1, 3)),
    "JPP": list(range(2002, 2008+1, 3)),
    "CHR": list(range(2002, 2005+1, 3)), #TODO: Fix for 1999
    "MNA": list(range(2011, 2017+1, 3))
} 

PARTY_ABBREVIATIONS = {
    "ACT New Zealand": "ACT",
    "ACT": "ACT",
    "Green Party": "GRN",
    "Labour Party": "LAB",
    "National Party": "NAT",
    "New Conservatives": "CON",
    "New Conservative": "CON",
    "Conservative": "CON",
    "Conservative Party": "CON",
    "New Zealand First Party": "NZF",
    "NZ First": "NZF",
    "Te Pti Mori": "TPM",
    "Maori Party": "TPM",
    "Mori Party": "TPM",
    "Mana Maori Movement": "MNA",
    "The Opportunities Party TOP": "TOP",
    "United Future": "UNF",
    "United Future New Zealand": "UNF",
    "United NZ": "UNF",
    "Mana": "MNA",
    "Mana Maori": "MNA",
    "Internet Mana": "MNA",
    "Alliance": "ALL",
    "Jim Andertons Progressive": "JPP",
    "Progressive Coalition": "JPP",
    "Christian Heritage NZ": "CHR",
    "Christian Heritage": "CHR",
    "Christian Heritage Party": "CHR"
}

PARTY_ABBREVIATIONS_LOWER = {k.lower(): v for k, v in PARTY_ABBREVIATIONS.items()}