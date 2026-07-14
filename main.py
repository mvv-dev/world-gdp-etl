import logging
import sqlite3

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def load(df: DataFrame):
    logging.info("Load process started")

    # save json file
    df.to_json("gdps.json")

    # Create DB
    connection = sqlite3.connect("World_Economies.db")

    # Create table
    df.to_sql(
        name="Countries_by_GDP",
        con=connection,
        if_exists="replace",
        index=False
    )

    # Example query
    query = """
    SELECT *
    FROM Countries_by_GDP
    WHERE "IMF Estimate GDP (USD Billion)" >= 100"""

    result = connection.execute(query)

    for row in result:
        print(row)

    logging.info("Load process completed")

    connection.close()



def transform(df: DataFrame) -> DataFrame:
    logging.info("Transform process started")

    # GDP -> Billions USD, rounded to 2 decimal places
    # DataFrame ordered by gdp (Descending)

    # Clean strings spaces, "", "—" and others
    df["Country/Territory"] = df["Country/Territory"].str.strip()
    df["IMF Estimate GDP (USD Million)"] = (df["IMF Estimate GDP (USD Million)"].str.strip()
                                            .str.replace(",", "").str.replace("—","0"))
    df["Year"] = df["Year"].str.replace("", "0").str.replace("—","0").str.slice(-4).astype(int)

    # Convert number and billions
    df["IMF Estimate GDP (USD Million)"] = df["IMF Estimate GDP (USD Million)"].astype(float).div(1000).round(2)

    #Rename the column
    df = df.rename(columns={"IMF Estimate GDP (USD Million)": "IMF Estimate GDP (USD Billion)"})

    logging.info(
        "Transform process completed: %s rows transformed",
        len(df)
    )

    return df



def extract(url: str) -> DataFrame:
    logging.info("Extract process started")

    # Do the request and get


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

    logging.info(
        "Extract process completed: %s rows extracted",
        len(gdp_by_country_df)
    )

    return gdp_by_country_df





def main():

    url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"

    logging.info("ETL pipeline started")

    try:
        df = extract(url)
        transformed_df = transform(df)
        load(transformed_df)

    except Exception:
        logging.exception("ETL pipeline failed")
        raise

    else:
        logging.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    main()

