from io import StringIO

import pandas as pd
import requests

def requestConstituents(url, table_id):
    response = requests.get(
        url,
        headers={"User-Agent": "AAIS student project"},
        timeout=30,
    )
    response.raise_for_status()

    tables = pd.read_html(
        StringIO(response.text),
        attrs={"id": table_id},
        flavor="lxml",
    )
    df = tables[0]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join(dict.fromkeys(str(level) for level in column if level))
            for column in df.columns
        ]
    df.columns = df.columns.str.lower().str.replace(" ", "_")
 
   

    
    return df

constituents_df = (
    requestConstituents(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        "constituents",
    )
)
history_df = (
    requestConstituents(
        "https://en.wikipedia.org/wiki/Historical_components_of_the_S&P_500",
          "changes",
          )
)
constituents_df["yahoo_symbol"] = constituents_df["symbol"].str.replace(".", "-", regex=False)



history_df['added_ticker'] = history_df['added_ticker'].str.replace(".", "-", regex=False)
history_df['removed_ticker'] = history_df['removed_ticker'].str.replace(".", "-", regex=False)

dd = (
    pd.concat(
        [
            constituents_df["yahoo_symbol"],
            history_df["added_ticker"],
            history_df["removed_ticker"],
        ],
        ignore_index=True,
    )
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

print(dd)