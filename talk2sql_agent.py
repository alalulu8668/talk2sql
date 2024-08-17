import asyncio
import yaml
import pandas as pd
import webbrowser
from schema_agents import Role, schema_tool
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
import os

# Define the SQL schema models
class PatientRecordSchema(BaseModel):
    """A schema representing a patient record."""
    id: int = Field(description="The ID of the patient record.")
    name: str = Field(description="The name of the patient.")
    age: int = Field(description="The age of the patient.")
    patient_id: str = Field(description="The unique patient ID.")
    symptoms: str = Field(description="The symptoms of the patient.")
    ct_image_file: str = Field(description="The filename of the CT image.")
    image_path: str = Field(description="The file path of the CT image.")

class SQLQuery(BaseModel):
    """A schema representing a SQL query."""
    query: str = Field(description="The SQL query to be executed.")

DATABASE_URL = os.environ.get('TALK2SQL_DATABASE_URL','postgresql+asyncpg://talk2sql_user:mysecretpassword@localhost/talk2sql_db')

# Generate the YAML content directly from the schema
constraints_yaml = yaml.dump({
    'name': 'patient_records',
    'description': 'Table containing patient records with detailed medical data.',
    'columns': {k: v['description'] for k, v in PatientRecordSchema.model_json_schema()['properties'].items()}
}, sort_keys=False)

@schema_tool
async def execute_sql_query(sql_query: SQLQuery) -> str:
    """Execute the SQL query and save the results to a file."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(text(sql_query.query))
            records = result.fetchall()

            # Convert to DataFrame
            data = [dict(id=record[0], name=record[1], age=record[2], patient_id=record[3],
                         symptoms=record[4], ct_image_file=record[5], image_path=record[6]) 
                    for record in records]
            df = pd.DataFrame(data)

            # Save to CSV
            file_path = 'patient_records.csv'
            df.to_csv(file_path, index=False)
            return file_path

@schema_tool
def display_in_browser(file_path: str) -> str:
    """Display the CSV file data in a web browser."""
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Convert DataFrame to HTML
    html_content = df.to_html(index=False)

    # Write HTML to file
    html_file = 'patient_records.html'
    with open(html_file, 'w') as f:
        f.write(html_content)

    # Open the HTML page in the default browser
    full_path = os.path.abspath(html_file)
    webbrowser.open(f'file://{full_path}')

    return f"Table displayed in the browser from the file: {file_path}"

async def main():
    agent = Role(
        name="HealthQueryAgent",
        profile="Medical Data Query Agent",
        goal="Your goal is to help convert user queries to SQL expressions. You have access to patient records.",
        constraints=constraints_yaml,
        register_default_events=True,
    )
    
    # Simulate a user query in natural language
    user_query = "Show me all patient records with age greater than 10."

    display_message = await agent.acall([user_query], [execute_sql_query, display_in_browser])

    print(display_message)

if __name__ == "__main__":
    asyncio.run(main())
