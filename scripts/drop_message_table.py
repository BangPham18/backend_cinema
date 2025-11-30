import sys
import os
from sqlalchemy import text

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine

def drop_table():
    try:
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS message_database_2"))
            connection.commit()
            print("✅ Successfully dropped table 'message_database_2'")
    except Exception as e:
        print(f"❌ Failed to drop table: {e}")

if __name__ == "__main__":
    drop_table()
