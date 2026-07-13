import pandas as pd
from bs4 import BeautifulSoup
import requests
from pandas import DataFrame


def load():
    pass

def transform(df: DataFrame) -> DataFrame:

    # GDP -> Billions USD, rounded to 2 decimal places
    # DataFrame ordered by gdp (Descending)

    # Clean strings spaces, "", "—" and others
    df["Country/Territory"] = df["Country/Territory"].str.strip()
    df["IMF Estimate GDP (USD Million)"] = (df["IMF Estimate GDP (USD Million)"].str.strip()
                                            .str.replace(",", "").str.replace("—","0"))
    df["Year"] = df["Year"].str.slice(-4)

    # Convert number and billions
    df["IMF Estimate GDP (USD Million)"] = round(df["IMF Estimate GDP (USD Million)"].astype(int) / 1000, 2)

    #Rename the column
    df = df.rename(columns={"IMF Estimate GDP (USD Million)": "IMF Estimate GDP (USD Billion)"})

    return df



def extract(url: str) -> DataFrame:

    # Do the request and get HTML

    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    soup_object = BeautifulSoup(html, "html.parser")
    countries_table = soup_object.find(name="table", class_="wikitable")
    countries_table_rows = countries_table.select(selector="tbody tr")
    countries = []

    for r in countries_table_rows:
        cells = r.select(selector="td")

        if cells and cells[0].select(selector="a"): # not null and All countries have "<a>" tag on first column

            country_data = {
                "Country/Territory": cells[0].text,
                "IMF Estimate GDP (USD Million)": cells[2].text,
                "Year": cells[3].text
            }

            countries.append(country_data)

    gdp_by_country_df = pd.DataFrame(countries)

    return gdp_by_country_df





def main():

    url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    df = extract(url)
    transformed_df = transform(df)

    pass


if __name__ == "__main__":
    main()

