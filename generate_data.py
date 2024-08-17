import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text
from faker import Faker

# SQLAlchemy base
Base = declarative_base()

# Define the table schema
class PatientRecord(Base):
    __tablename__ = 'patient_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    patient_id = Column(String(50), unique=True, nullable=False)  # Increased length
    symptoms = Column(Text, nullable=True)
    ct_image_file = Column(String(100), nullable=True)
    image_path = Column(String(255), nullable=True)

# Generate synthetic data
def generate_synthetic_data(fake, num_records=100):
    data = []
    for _ in range(num_records):
        record = {
            'name': fake.name(),
            'age': fake.random_int(min=0, max=100),
            'patient_id': fake.uuid4(),
            'symptoms': fake.sentence(),
            'ct_image_file': f"{fake.uuid4()}.dcm",
            'image_path': f"/data/images/{fake.uuid4()}.dcm"
        }
        data.append(record)
    return data

# Insert data into the database
async def insert_data(engine, data):
    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all([PatientRecord(**record) for record in data])
        await session.commit()

async def main():
    # Setup database connection
    engine = create_async_engine('postgresql+asyncpg://talk2sql_user:mysecretpassword@localhost/talk2sql_db', echo=True)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Generate data
    fake = Faker()
    data = generate_synthetic_data(fake, num_records=100)

    # Insert data into the database
    await insert_data(engine, data)

    # Close the engine
    await engine.dispose()

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
