# 🛢️ AWS ETL Pipeline – Sakila Data Lake Analytics (Glue + S3 + Athena)

This project implements a data analytics architecture for the Sakila movie rental database using AWS services. It features ETL processes in AWS Glue for incremental data ingestion, transformation, and loading into a data lake in S3 as Parquet files.

Data is queryable via AWS Athena, with automated schema detection using Glue Crawlers and orchestration via Glue Workflows. A modified web application allows inserting new rentals into the Sakila RDS database, triggering updates to the analytics system. The architecture supports continuous deployment with unit tests, managing resources programmatically.

---

# 📊 Introduction to Big Data and Data Engineering

This project transforms the Sakila database (a sample movie rental system) into a dimensional model for analytics.

- Perception → Data is ingested from RDS sources.

- Decision-making → ETL jobs apply transformations like joins and calculations.

- Action → Data is stored in S3 and cataloged for querying.

This setup creates a scalable analytics system, enabling insights into sales, customers, and inventory while keeping data updated.

---

# 🚀 Features

- 📥 **Incremental ETL**: Allows updates for dimension tables (Film, Customer, Store) from RDS to S3.

- 🔗 **SQL Transformations**: Joins multiple tables (customer, film, rental, store) to build the Fact Sales table.

- 🗓️ **Python Date Dimension**: Generates date details including quarter, weekday/weekend, and US holidays.

- 🕷️ **Glue Crawlers**: Automatically detect and catalog Parquet schemas in the Glue Data Catalog.

- 🔄 **Glue Workflows**: Orchestrate ETL jobs and crawlers for sequential execution.

- 🌐 **Web Application**: Created to insert new rentals (date, customer document, film selection via dropdown).

- 🚀 **Continuous Deployment**: Unit tests for managing AWS resources like jobs in S3.

- 📊 **Athena Querying**: Visualize and query the data lake directly.

- ✅ **Dimensional Modeling**: Supports star schema with facts and dimensions for efficient analytics.

- 🚧 **Date ID Formatting**: Converts dates to integer format (e.g., 20051201 for 2005-12-01).

---

# 💻 Code Workflow

## base_datos.py

- Manages connections to the Sakila RDS database.
- Defines and creates a 'usuarios' table for user management, with columns for ID, names, surnames, birth date, and password.
- Uses Python to generate date records and integrate with Glue workflows.

## app.py

- Flask backend application with CORS enabled for cross-origin requests.
- Connects to the AWS MySQL RDS database using Flask-SQLAlchemy.
- Includes API endpoints: /register (POST), /users (GET) and  /check_db.

## Back/test/Servidor.py

- Defines the Usuario model.
- Provides a function create_test_app() to set up a test Flask application with an in-memory SQLite database for unit testing.
- Includes test routes: /register (POST) for creating a user (parses birth date to datetime.date); /users (GET) for retrieving users.

## .github/workflows/app.yaml

- CI/CD workflow named "DeployBackend" triggered on pushes to the "Back" branch.
- Executes unit tests using pytest on Back/test/test_usuario.py (with PYTHONPATH set).
- If tests succeed, deploys to an EC2 instance via SSH: pulls the "Back" branch, activates a virtual environment, installs dependencies, kills any process on port 5000, and runs app.py in a detached tmux session, logging to registro.log.

## .github/workflows/app-front.yaml

- CI/CD workflow named "DeployFrontend" triggered on pushes to the "Front" branch.
- Deploys to an EC2 instance via SSH: updates packages, installs npm, pulls the "Front" branch, runs npm install and npm run build in Front/user-registration, installs Apache2, clears and sets permissions on /var/www/html/, copies the build output to the web root, and restarts Apache2.

## Front/user-registration/

- Frontend component or page for user interactions.
- Created to include the rental form with date input, customer document, and film dropdown.

---

# 🧩 How It Works

- A user accesses the Web Application to create a new rental: enters date, customer document, and selects a film.

- The app inserts the data into the Sakila RDS database (tables like rental).

- Incremental ETL jobs run via Glue.

  - Pull new data from Film, Customer, Store to update dimension tables in S3.

  - Combine sources to build/update Fact Sales with SQL joins.

  - Generate or update the Date_sales dimension using Python logic.

- Glue Crawlers scan the Parquet files in S3 to detect schemas and update the Data Catalog.

- Glue Workflows orchestrate the process: execute jobs, then crawlers.

- Analysts query the data lake via AWS Athena for insights into sales trends.

- The system maintains data freshness as new rentals are added, with all resources managed via boto3 for CI/CD.

---

# 🧠 ETL Processes Summary

## Incremental Dimension ETL

- Connect to RDS Sakila.
- Identify new/updated records in Film, Customer, Store.
- Transform and write as Parquet to S3 dimension paths.

## Fact Sales ETL

- Joins customer, film, rental, and store tables.
- Transforms rental_date to Date_sales_id (e.g., CAST to INT in YYYYMMDD format).
- Writes combined data as Parquet to S3 fact path.

---

# 🔧 AWS Services Requirements

- AWS Glue (for ETL jobs, crawlers, workflows)
- Amazon S3 (for data lake storage as Parquet)
- AWS Athena (for querying the cataloged data)
- Amazon RDS (with Sakila database schema)
- Python (with React for develoment and deployment)

---

# 📊 Future Improvements

- 🔄 Integrate AWS Lambda for event-driven ETL triggers on new rentals.
- 🧮 Add more dimensions (e.g., Actor, Category from Sakila).
- 🖥️ Build a dashboard with Amazon QuickSight for visualizations.
- 🧭 Implement monitoring with CloudWatch for ETL failures.

---

# 👨‍💻 Author

Developed by **Daniel Bernal**
