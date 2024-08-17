import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from generate_data import PatientRecord

async def query_data(engine):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Perform a simple query to retrieve all patient records
            result = await session.execute(select(PatientRecord))
            patients = result.scalars().all()  # Load all results into memory
            
            # Print the results within the session context
            for patient in patients:
                print(f"ID: {patient.id}, Name: {patient.name}, Age: {patient.age}, Patient ID: {patient.patient_id}, Symptoms: {patient.symptoms}, CT Image File: {patient.ct_image_file}, Image Path: {patient.image_path}")

async def main():
    # Setup database connection
    engine = create_async_engine('postgresql+asyncpg://talk2sql_user:mysecretpassword@localhost/talk2sql_db', echo=True)
    
    # Query and print the data
    await query_data(engine)
    
    # Close the engine
    await engine.dispose()

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
