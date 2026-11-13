# India's Diwali Economy (2020–2026)

### An End-to-End Data Analytics Project with Machine Learning Exploration

An analytical exploration of India's Diwali-associated economic activity through retail spending patterns, gold demand, confectionery markets, fireworks industry indicators, and vehicle registration trends.

This project brings together data from multiple sources to study different dimensions of India's festive economy. It uses Python for data preparation and analysis, SQL for structured data querying, and statistical and machine learning techniques to explore patterns in the available data.

> **Research approach:** Not every dataset directly measures Diwali-specific expenditure. The project distinguishes between direct festive retail data and broader economic indicators rather than treating them as equivalent measures of Diwali spending.

---

## Project Objectives

- Explore different sectors associated with India's Diwali economy.
- Analyze retail transaction patterns and product-category spending.
- Examine historical vehicle registration trends.
- Investigate gold and confectionery market indicators.
- Explore available fireworks industry information.
- Clean, transform, and prepare datasets using Python.
- Integrate selected datasets into a relational SQLite database.
- Use SQL to perform analytical queries and aggregations.
- Explore opportunities for predictive modelling and spending-pattern segmentation.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Manipulation | Pandas, NumPy |
| Database | SQLite |
| Query Language | SQL |
| Machine Learning | Scikit-learn |
| Predictive Modelling | Linear Regression (planned implementation) |
| Clustering | K-Means (planned implementation) |
| Feature Scaling | StandardScaler |
| Visualization | Matplotlib |
| Data Sources | CSV, XLSX, PDF |

---

## Datasets

The project uses multiple datasets covering different dimensions of India's festive economy.

| Dataset | Description | Analytical Purpose |
|---|---|---|
| VAHAN Year-wise | Annual vehicle registration data, 2020–2026 | Long-term registration trends |
| VAHAN Monthly (2020–2022) | Monthly vehicle registration data | Historical monthly patterns |
| VAHAN Monthly (2023–2025) | Monthly vehicle registration data | Recent monthly patterns |
| India Confectionery Market | Historical and forecast market data | Confectionery market trends |
| Diwali Sales | Retail transaction dataset containing customer, product and amount information | Category-wise spending and customer analysis |
| World Gold Council | Gold market statistics | Gold demand and jewellery market analysis |
| PESO Fireworks Information | Information about authorized fireworks manufacturers | Fireworks industry context |

### Data Coverage and Interpretation

The datasets differ in their reporting periods, geographical coverage, units of measurement, and levels of detail.

Important distinctions:

- The Diwali Sales dataset provides retail transaction-level information.
- VAHAN data represents vehicle registrations, not verified Diwali vehicle purchases.
- Confectionery market figures represent broader market activity, not exclusively Diwali sales.
- Gold market statistics require careful extraction of India-specific jewellery demand figures.
- Fireworks manufacturer information does not directly measure fireworks sales or consumer expenditure.

These differences are considered when interpreting results and drawing conclusions.

---

## Project Workflow

### 1. Data Collection and Preparation

- Collected datasets from different sources in CSV, Excel, and PDF formats.
- Inspected dataset structures, column types, and missing values.
- Removed duplicate records where appropriate.
- Handled missing numerical values using suitable imputation methods.
- Converted date and numerical columns into appropriate data types.
- Created additional analytical features from VAHAN monthly data.
- Exported cleaned datasets for subsequent analysis.

**Output:** Cleaned datasets stored in the `output/` directory.

### 2. Database Management and SQL Analytics

Created a relational SQLite database named `diwali_economy.db`.

The current database ingestion script integrates:

- `fact_transactions` — Diwali retail transaction records.
- `fact_vehicle_registrations` — Monthly vehicle registration records.

SQL analysis includes:

- Product-category performance.
- Unique customer counts.
- Recorded sales amounts by category.
- Customer purchase activity.
- Annual vehicle registration trends.
- October–November registration comparisons.
- Monthly registration patterns.

SQL query results are exported as CSV files for further analysis.

**Note:** Recorded sales amounts and average row amounts are not automatically equivalent to verified transaction revenue and average order value.

### 3. Exploratory Data Analysis

The project explores:

- Year-wise vehicle registration trends.
- Monthly vehicle registration patterns.
- Retail spending across product categories.
- Customer purchase activity.
- Gold and confectionery market trends.
- Selected relationships between economic indicators.

The analysis is designed to identify patterns and trends while considering differences in dataset coverage and measurement.

### 4. Predictive Modelling

The project plans to explore Linear Regression for analysing historical trends and developing forecasts where sufficient comparable historical observations are available.

Potential applications include:

- Vehicle registration trend forecasting.
- Retail spending trend analysis.
- Comparison of predicted and observed values.
- Evaluation of model performance using appropriate metrics.

Forecasts will be treated as model-based estimates rather than confirmed economic outcomes.

### 5. Spending Pattern Segmentation

The project also explores K-Means Clustering as a potential technique for identifying spending patterns.

The proposed workflow includes:

- Selecting relevant numerical features.
- Handling missing values and outliers.
- Standardizing features using `StandardScaler`.
- Selecting an appropriate number of clusters.
- Applying K-Means.
- Interpreting and visualizing the resulting groups.

Any resulting clusters will be treated as exploratory statistical segments rather than verified customer classifications.

### 6. Data Visualization

Visualizations are used to communicate patterns in the datasets, including:

- Vehicle registration trends.
- Year-over-year changes.
- Product-category spending.
- Economic indicator comparisons.
- Spending-pattern segmentation.

Visualizations will be documented alongside the analytical methods and data limitations used to produce them.

---

## Repository Structure

```text
India-Diwali-Economy-Analysis/
│
├── data/
│   ├── 2020 -2026 vahan year.csv
│   ├── 2020-2022 montwise vahan.csv
│   ├── 2023-2025 montiwse vahan.csv
│   ├── dataset_4_india_confectionery.csv
│   ├── Diwali Sales Data.csv
│   ├── GDT Tables_Q326_EN.xlsx
│   └── PESO_Authorized_Fireworks_Manufacturers.pdf
│
├── output/
│   ├── diwali_sales_cleaned.csv
│   ├── vahan_monthly_cleaned.csv
│   ├── india_jewellery_demand_raw.csv
│   ├── category_performance.csv
│   ├── customer_activity.csv
│   ├── annual_vehicle_trend.csv
│   └── monthly_vehicle_trend.csv
│
├── diwali_cleaning.py
├── diwali_database.py
├── diwali_economy.db
│
└── README.md
```

*The output files are generated by the corresponding scripts. Additional datasets and visualization files may be added as the project develops.*

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sharadashenoy18/India-Diwali-Economy-Analysis.git

cd India-Diwali-Economy-Analysis
```

### 2. Install Dependencies

```bash
pip install pandas numpy matplotlib scikit-learn openpyxl
```

SQLite is available through Python's built-in `sqlite3` module.

### 3. Prepare the Datasets

Place the required input datasets in the project directory, or update the file paths in the Python scripts if using a separate `data/` directory.

### 4. Run Data Cleaning

```bash
python diwali_cleaning.py
```

This prepares the retail and VAHAN datasets and exports the cleaned outputs.

### 5. Create the Database and Run SQL Analytics

```bash
python diwali_database.py
```

This creates or updates the SQLite database, executes analytical SQL queries, and exports the query results.

*Run the scripts in the above order when using the cleaned datasets generated by the data-cleaning script.*

---

## Limitations and Considerations

- The datasets have different reporting periods, geographical coverage, and levels of granularity.
- Not all datasets directly measure Diwali-specific expenditure.
- Vehicle registrations cannot independently establish Diwali-related vehicle purchases.
- Broader confectionery and gold market figures should not be interpreted as Diwali-only sales.
- Fireworks manufacturer records do not represent actual sales or consumer spending.
- Forecast reliability depends on historical data availability, data quality, and model assumptions.
- Clustering results depend on feature selection, scaling, and the choice of cluster count.
- Correlation does not establish causation.
- 2026 data may represent a partial reporting period and should not be compared with complete years without adjustment.

---

## Key Learning Outcomes

- Developed a multi-dataset data analytics workflow.
- Practised data cleaning and feature engineering using Pandas.
- Used SQLite for relational data storage and management.
- Applied SQL aggregations and analytical queries.
- Explored retail spending and vehicle registration patterns.
- Worked with datasets from different sources and reporting formats.
- Investigated the use of statistical analysis and machine learning in economic data exploration.
- Developed an understanding of data limitations and responsible interpretation of analytical findings.

---

## Author

**Sharada Shenoy**

M.Sc. Computer Science | Aspiring Data Analyst

- LinkedIn: [Sharada Shenoy](https://linkedin.com/in/sharada-shenoy-665a79275/)
- GitHub: [sharadashenoy18](https://github.com/sharadashenoy18)

---

*An independent Data Analytics project exploring India's Diwali-associated economic activity through multiple data sources.*
