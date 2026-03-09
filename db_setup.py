import pandas as pd
from sqlalchemy import create_engine, text
import os
import glob
import chardet

# Configuration -> Replace with your actual local PostgreSQL credentials
# Format: postgresql://username:password@host:port/database_name
DB_USER = "postgres"
DB_PASS = "postgres" # Change this if needed
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "ubc_housing_db" # We will connect to default 'postgres' db first to create this

# First, connect to default postgres DB to create our new database
try:
    default_engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres')
    with default_engine.connect() as conn:
        conn.execute(text("COMMIT")) # Need to commit before CREATE DATABASE
        try:
            conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
            print(f"Database '{DB_NAME}' created successfully.")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Database '{DB_NAME}' already exists.")
            else:
                raise e
except Exception as e:
    print(f"Error connecting to PostgreSQL or creating database. Make sure PostgreSQL is running locally.\nError: {e}")
    print("If you don't have PostgreSQL running, you can start one via Docker:")
    print("docker run --name my-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres")
    exit(1)

# Now connect to the newly created database
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

print("Connected to PostgreSQL successfully.")

# 1. Ingest Housing Data (Multiple CSVs)
data_dir = "data/Cleaned_Housing_Rental_Data"
if not os.path.exists(data_dir):
    print(f"Error: Directory '{data_dir}' not found.")
    exit(1)

csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
housing_df_list = []

for file in csv_files:
    try:
        # Detect encoding
        with open(file, 'rb') as f:
            result = chardet.detect(f.read())
        
        df = pd.read_csv(file, encoding=result['encoding'])
        
        # Validation / Cleaning: Ensure standard column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Standardize columns if they differ slightly (e.g., 'rent' vs 'average_rent')
        if 'rent' in df.columns and 'average_rent' not in df.columns:
            df.rename(columns={'rent': 'average_rent'}, inplace=True)
            
        housing_df_list.append(df)
        print(f"Successfully loaded: {os.path.basename(file)}")
    except Exception as e:
        print(f"Error loading {file}: {e}")

if housing_df_list:
    combined_housing_df = pd.concat(housing_df_list, ignore_index=True)
    
    # Save to PostgreSQL table 'housing_rates'
    combined_housing_df.to_sql('housing_rates', engine, if_exists='replace', index=False)
    print(f"Inserted {len(combined_housing_df)} rows into 'housing_rates' table.")
else:
    print("No housing data found to insert.")

# 2. Ingest Enrolment Data
enrolment_file = "data/Enrolment_Vs_Housing_Data/housing-students-ubc-2007-2023.csv"
if os.path.exists(enrolment_file):
    try:
        enrolment_df = pd.read_csv(enrolment_file)
        # Clean column names
        enrolment_df.columns = enrolment_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('%', 'pct')
        
        enrolment_df.to_sql('ubc_enrolment', engine, if_exists='replace', index=False)
        print(f"Inserted {len(enrolment_df)} rows into 'ubc_enrolment' table.")
    except Exception as e:
        print(f"Error loading enrolment data: {e}")
else:
    print(f"Error: File '{enrolment_file}' not found.")

# 3. Analytics / Verification Queries
with engine.connect() as conn:
    print("\n--- Analytics Query Results ---")
    
    # Simple count verification
    count_res = conn.execute(text("SELECT COUNT(*) FROM housing_rates")).scalar()
    print(f"Total Housing Records in DB: {count_res}")
    
    count_res_enr = conn.execute(text("SELECT COUNT(*) FROM ubc_enrolment")).scalar()
    print(f"Total Enrolment Records in DB: {count_res_enr}\n")
    
    # Complex Query: Average Rent by Year joined with UBCV Student Beds (if years overlap)
    # Note: Housing data is usually 2020-2024, Enrolment data is 2007-2023. 
    # The overlap is 2020, 2021, 2022, 2023.
    query = """
    SELECT 
        h.year,
        ROUND(AVG(h.average_rent)::numeric, 2) as avg_rent,
        e.student_beds_ubcv
    FROM 
        housing_rates h
    JOIN 
        ubc_enrolment e ON h.year = e.chart_year
    GROUP BY 
        h.year, e.student_beds_ubcv
    ORDER BY 
        h.year;
    """
    
    try:
        print("Query: Average Rent vs Available UBCV Student Beds (Overlapping Years)")
        result = conn.execute(text(query))
        
        # Fetch all rows and column names
        rows = result.fetchall()
        columns = list(result.keys())
        
        # Display as a formatted table
        if rows:
            print(f"{columns[0]:<10} | {columns[1]:<15} | {columns[2]:<20}")
            print("-" * 50)
            for row in rows:
                print(f"{str(row[0]):<10} | ${str(row[1]):<14} | {str(row[2]):<20}")
        else:
            print("No overlapping data found for the query.")
    except Exception as e:
        print(f"Error executing analytics query: {e}")

print("\nDatabase setup and ingestion complete.")
