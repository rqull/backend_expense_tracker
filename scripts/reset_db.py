from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/expense_tracker")

# Create engine
engine = create_engine(DATABASE_URL)

def reset_database():
    try:
        # Create a connection
        with engine.connect() as connection:
            # Start a transaction
            with connection.begin():
                # Disable foreign key checks temporarily
                connection.execute(text("SET session_replication_role = 'replica';"))
                
                # Get all table names
                result = connection.execute(text("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row[0] for row in result]
                
                # Delete all data from each table
                for table in tables:
                    connection.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                
                # Re-enable foreign key checks
                connection.execute(text("SET session_replication_role = 'origin';"))
                
                print("Database berhasil direset!")
                print("Semua data telah dihapus.")
                
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    # Ask for confirmation
    confirm = input("PERHATIAN: Ini akan menghapus SEMUA data dari database. Lanjutkan? (y/N): ")
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Operasi dibatalkan.") 