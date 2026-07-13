# 🌍 World GDP ETL Pipeline

A complete ETL (Extract, Transform, Load) pipeline developed in Python to automatically collect the latest Gross Domestic Product (GDP) data of countries from the International Monetary Fund (IMF), transform the data into the required format, and load it into both JSON and SQLite.

This project was developed as part of the **IBM Data Engineering Professional Certificate**.

---

## 📖 Overview

The objective of this project is to automate the process of retrieving worldwide GDP information from the IMF website.

The pipeline performs the complete ETL workflow:

1. **Extract** data from the source website.
2. **Transform** the GDP values into billions of USD (rounded to two decimal places).
3. **Load** the processed data into:
   - A JSON file
   - A SQLite database
4. Execute SQL queries for validation.
5. Log every execution step.

---
## 🚀 Features

- Extract data from an HTML webpage
- Parse and clean the extracted information
- Transform GDP values into billions of USD
- Save data as JSON
- Store data in SQLite
- Execute SQL queries
- Generate execution logs
- Modular ETL implementation

## ⚙️ Technologies

- Python 3
- Pandas
- Requests
- BeautifulSoup4
- SQLite3
- JSON
- Logging
