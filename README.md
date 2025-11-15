# 🛢️ AWS ETL Pipeline – Sakila Data Lake Analytics (Glue + S3 + Athena)
This project implements a data analytics architecture for the Sakila movie rental database using AWS services. It features ETL processes in AWS Glue for incremental data ingestion, transformation, and loading into a data lake in S3 as Parquet files.

Data is queryable via AWS Athena, with automated schema detection using Glue Crawlers and orchestration via Glue Workflows. A modified web application allows inserting new rentals into the Sakila RDS database, triggering updates to the analytics system. The architecture supports continuous deployment with unit tests, managing resources programmatically via boto3.

---

# 📊 Introduction to Big Data and Data Engineering

This project transforms the Sakila database (a sample movie rental system) into a dimensional model for analytics.

Perception → Data is ingested from RDS sources.

Decision-making → ETL jobs apply transformations like joins and calculations.

Action → Data is stored in S3 and cataloged for querying.

This setup creates a scalable analytics system, enabling insights into sales, customers, and inventory while keeping data updated.

---

# 🚀 Features

📥 **Incremental ETL**: Daily updates for dimension tables (Film, Customer, Store) from RDS to S3.

🔗 **SQL Transformations**: Joins multiple tables (customer, film, rental, store) to build the Fact Sales table.

🗓️ **Python Date Dimension**: Generates date details including quarter, weekday/weekend, and US holidays.

🕷️ **Glue Crawlers**: Automatically detect and catalog Parquet schemas in the Glue Data Catalog.

🔄 **Glue Workflows**: Orchestrate ETL jobs and crawlers for sequential execution.

🌐 **Web Application**: Modified to insert new rentals (date, customer document, film selection via dropdown).

🚀 **Continuous Deployment**: Unit tests and boto3 for managing AWS resources like jobs in S3.

📊 **Athena Querying**: Visualize and query the data lake directly.

✅ **Dimensional Modeling**: Supports star schema with facts and dimensions for efficient analytics.

✅ Date ID Formatting: Converts dates to integer format (e.g., 20051201 for 2005-12-01).

---

# 💻 Code Workflow

scripts/glue_etl_incremental.py
Handles incremental data movement from RDS Sakila tables (Film, Customer, Store) to S3 dimension tables.

Runs daily to append new or updated records as Parquet files.

scripts/glue_etl_fact_sales.py
Combines data from customer, film, rental, and store tables.

Uses the SQL transform option in Glue to perform joins and create the Fact Sales table.

Converts rental_date to Date_sales_id as an integer.

scripts/glue_etl_date_dimension.py
Python script to populate the Date_sales dimension.

Calculates additional attributes like year quarter, weekday/weekend status, and US holiday flags.

Integrated with a workflow that runs the job followed by a crawler for catalog updates.

sql/fact_sales_transform.sql
SQL query for the Fact Sales ETL, including joins and date transformations.

web_app/
Contains the modified web application code.

Allows users to input rental date, customer document, and select a film from a dropdown.

Inserts data directly into the Sakila RDS database, triggering ETL updates.

---

# 🧩 How It Works

A user accesses the Web Application to create a new rental: enters date, customer document, and selects a film.

The app inserts the data into the Sakila RDS database (tables like rental).

Incremental ETL jobs run daily via Glue:

Pull new data from Film, Customer, Store to update dimension tables in S3.

Combine sources to build/update Fact Sales with SQL joins.

Generate or update the Date_sales dimension using Python logic.

Glue Crawlers scan the Parquet files in S3 to detect schemas and update the Data Catalog.

Glue Workflows orchestrate the process: execute jobs, then crawlers.

Analysts query the data lake via AWS Athena for insights into sales trends.

The system maintains data freshness as new rentals are added, with all resources managed via boto3 for CI/CD.

---

# 🧠 ETL Processes Summary

Incremental Dimension ETL
Connect to RDS Sakila.

Identify new/updated records in Film, Customer, Store.

Transform and write as Parquet to S3 dimension paths.

Ensure daily execution for increments.

Fact Sales ETL
Joins customer, film, rental, and store tables.

Transforms rental_date to Date_sales_id (e.g., CAST to INT in YYYYMMDD format).

Writes combined data as Parquet to S3 fact path.

Date Dimension ETL
Python script generates date records.

Calculates:

Quarter of the year.

Weekday (True/False for weekend).

US holiday status (using predefined holiday logic).

Workflow includes job execution followed by a crawler.

🧠 Data Transformation (SQL and Python)
Fact Sales (SQL)
For Fact Sales, an example SQL join:

SQL

SELECT
    c.customer_id,
    f.film_id,
    s.store_id,
    CAST(REPLACE(SUBSTRING(r.rental_date, 1, 10), '-', '') AS INT) AS date_sales_id,
    r.amount
FROM
    rental r
JOIN
    customer c ON r.customer_id = c.customer_id
JOIN
    inventory i ON r.inventory_id = i.inventory_id
JOIN
    film f ON i.film_id = f.film_id
JOIN
    store s ON i.store_id = s.store_id;
Date_sales (Python)
For the Date_sales dimension in Python:

Use datetime to iterate dates.

Determine quarter: date.month // 4 + 1.

Weekend: date.weekday() >= 5.

US holidays: Check against a list (e.g., New Year's, Independence Day).

🔧 AWS Services Requirements
AWS Glue (for ETL jobs, crawlers, workflows)

Amazon S3 (for data lake storage as Parquet)

AWS Athena (for querying the cataloged data)

Amazon RDS (with Sakila database schema)

Python (with boto3 for deployment)

📊 Future Improvements
🔄 Integrate AWS Lambda for event-driven ETL triggers on new rentals.

🧮 Add more dimensions (e.g., Actor, Category from Sakila).

🖥️ Build a dashboard with Amazon QuickSight for visualizations.

🧭 Implement monitoring with CloudWatch for ETL failures.

👨‍💻 Author
Developed by [FormalIngenieroniel]
