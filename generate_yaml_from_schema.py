import yaml
from pydantic import BaseModel, Field
from typing import List

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

class TableSchema(BaseModel):
    """A schema representing the table structure."""
    name: str
    description: str
    columns: List[PatientRecordSchema]

# Function to generate YAML from Pydantic model
def generate_yaml_from_schema():
    table_schema = TableSchema(
        name="patient_records",
        description="Table containing patient records with detailed medical data.",
        columns=[
            PatientRecordSchema(
                id=1,
                name="John Doe",
                age=30,
                patient_id="12345",
                symptoms="Cough, Fever",
                ct_image_file="ct_scan_001.dcm",
                image_path="/data/images/ct_scan_001.dcm"
            )
        ]
    )
    
    # Convert the schema to a dictionary and remove example values
    table_dict = table_schema.dict()
    table_dict['columns'] = {k: v["description"] for k, v in PatientRecordSchema.schema()["properties"].items()}
    
    # Generate YAML
    yaml_content = yaml.dump(table_dict, sort_keys=False)
    
    # Write YAML to file
    with open("patient_record_schema.yaml", "w") as yaml_file:
        yaml_file.write(yaml_content)
    
    print("YAML file generated successfully.")

if __name__ == "__main__":
    generate_yaml_from_schema()
