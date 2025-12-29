# GDP Data Pipeline

A Python-based data pipeline that collects global GDP data from Wikipedia, stores it in a PostgreSQL database, and generates visualization charts.

## Features

- **Data Collection**: Scrapes GDP estimates for 2024-2025 (Live) and 2021-2023 (Archived) from Wikipedia.
- **Data Processing**: Cleans and merges data into a unified CSV dataset (`gdp_history_2021_2025.csv`).
- **Database Integration**: Loads processed data into a PostgreSQL database table (`gdp_data`).
- **Visualization**: Generates trend lines and growth rate charts for top economies.

## Prerequisites

- Python 3.x
- PostgreSQL Database
- Required Python packages (install via `pip install -r requirements.txt` if available, or manually):
  ```bash
  pip install pandas requests sqlalchemy psycopg2-binary python-dotenv matplotlib seaborn lxml
  ```

## Setup

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/mhd-hashir/gdp-pipeline.git
    cd gdp-pipeline
    ```

2.  **Database Configuration**:
    - Create a `.env` file in the root directory.
    - Add your PostgreSQL credentials:
      ```env
      DB_HOST=localhost
      DB_NAME=your_db_name
      DB_USER=your_username
      DB_PASS=your_password
      DB_PORT=5432
      ```

## Usage

1.  **Run the Pipeline**:
    Scrape data and generate CSV.

    ```bash
    python gdp_pipeline.py
    ```

2.  **Load to Database**:
    Import the CSV data into PostgreSQL.

    ```bash
    python load_db.py
    ```

3.  **Visualize Data**:
    Generate charts for GDP trends and growth.
    ```bash
    python visualize_growth.py
    ```

## Project Structure

- `gdp_pipeline.py`: Main scraping and processing script.
- `load_db.py`: Script to load data into the database.
- `db_utils.py`: Reusable database connection module.
- `visualize_growth.py`: Generates PNG charts.
- `analysis.sql`: Sample SQL queries for analysis.
- `gdp_history_2021_2025.csv`: Generated dataset.
