# Talk2SQL Agent

## Overview

The `Talk2SQL` agent is a Python-based tool designed to interact with a PostgreSQL database using natural language queries. The agent converts these queries into SQL expressions, executes them against the database, and displays the results in a web browser.

## Features

- Convert natural language queries into SQL expressions.
- Execute SQL queries against a PostgreSQL database.
- Display query results in a web browser.
- Dynamic YAML generation from Pydantic schemas for flexible schema handling.

## Prerequisites

- **Python 3.10+**: Ensure you have Python 3.10 or higher installed.
- **PostgreSQL**: A running PostgreSQL instance.
- **Docker**: (Optional) If you want to run PostgreSQL using Docker.
- **Dependencies**: Install required Python packages.

## Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/alalulu8668/talk2sql.git
cd talk2sql
```

### Step 2: Create a Python Virtual Environment

It's recommended to create a virtual environment to manage dependencies:

```bash
python3 -m venv talk2sql_env
source talk2sql_env/bin/activate
```

### Step 3: Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```


### Step 4: Set Up PostgreSQL

#### Option 1: Using Docker

If you have Docker installed, you can quickly set up a PostgreSQL instance:

```bash
docker run --name talk2sql_db -e POSTGRES_USER=talk2sql_user -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=talk2sql_db -p 5432:5432 -d postgres
```

#### Option 2: Local PostgreSQL Instance

Ensure your PostgreSQL instance is running and create a database:

```bash
# Access the PostgreSQL command line interface
psql -U postgres

# Create a new database
CREATE DATABASE talk2sql_db;

# Create a new user with a password
CREATE USER talk2sql_user WITH PASSWORD 'mysecretpassword';

# Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE talk2sql_db TO talk2sql_user;
```

### Step 5: Configure the Database URL

The database URL is configured through environment variables (`TALK2SQL_DATABASE_URL`), you will also need an OpenAI API key (`OPENAI_API_KEY`).
    
```bash
export TALK2SQL_DATABASE_URL="postgresql+asyncpg://talk2sql_user:mysecretpassword@localhost/talk2sql_db"
export OPENAI_API_KEY="sk-XXXXXXXX"
```

Ensure this URL matches your PostgreSQL setup.

### Step 6: Run the Talk2SQL Agent

With everything set up, you can now run the agent:

```bash
python talk2sql_agent.py
```

The agent will:

1. Convert a natural language query to an SQL expression.
2. Execute the SQL query against the PostgreSQL database.
3. Save the query results to a CSV file.
4. Display the results in your web browser.

### Example Query

An example query to test the agent:

```python
user_query = "Show me all patient records with age greater than 10."
```

This will display all patient records in your browser where the age is greater than 10.

## Troubleshooting

- **Connection Issues**: Ensure your PostgreSQL instance is running and accessible.
- **Python Dependencies**: Double-check that all Python dependencies are installed.
- **Database Setup**: Verify that the database, user, and privileges are correctly configured.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.