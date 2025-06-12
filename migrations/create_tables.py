# migrations/create_tables.py
import sys
import os

# Add the parent directory to sys.path to be able to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app.models import Base

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def drop_tables():
    print("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully!")

def reset_tables():
    drop_tables()
    create_tables()
    print("Database reset complete!")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "create":
            create_tables()
        elif command == "drop":
            drop_tables()
        elif command == "reset":
            reset_tables()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: create, drop, reset")
    else:
        # Default action is to create tables
        create_tables()
