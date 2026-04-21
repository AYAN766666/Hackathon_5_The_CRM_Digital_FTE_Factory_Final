"""
Migration Script - Add priority, urgency_keywords, and processed_latency_ms columns
Run this to update existing database schema
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from database import engine, async_session_maker


async def migrate():
    """Add missing columns to messages table"""
    
    print("=" * 60)
    print("Database Migration - Add New Columns to Messages Table")
    print("=" * 60)
    
    async with async_session_maker() as session:
        try:
            # Check if columns already exist
            result = await session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'messages' 
                AND column_name IN ('priority', 'urgency_keywords', 'processed_latency_ms')
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            
            print(f"\n📊 Existing columns found: {existing_columns}")
            
            # Add priority column
            if 'priority' not in existing_columns:
                print("\n➕ Adding 'priority' column...")
                await session.execute(text("""
                    ALTER TABLE messages 
                    ADD COLUMN priority VARCHAR
                """))
                print("✅ Added 'priority' column")
            else:
                print("\n✅ 'priority' column already exists")
            
            # Add urgency_keywords column
            if 'urgency_keywords' not in existing_columns:
                print("\n➕ Adding 'urgency_keywords' column...")
                await session.execute(text("""
                    ALTER TABLE messages 
                    ADD COLUMN urgency_keywords VARCHAR
                """))
                print("✅ Added 'urgency_keywords' column")
            else:
                print("\n✅ 'urgency_keywords' column already exists")
            
            # Add processed_latency_ms column
            if 'processed_latency_ms' not in existing_columns:
                print("\n➕ Adding 'processed_latency_ms' column...")
                await session.execute(text("""
                    ALTER TABLE messages 
                    ADD COLUMN processed_latency_ms INTEGER
                """))
                print("✅ Added 'processed_latency_ms' column")
            else:
                print("\n✅ 'processed_latency_ms' column already exists")
            
            # Commit changes
            await session.commit()
            
            print("\n" + "=" * 60)
            print("✅ Migration completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Migration failed: {str(e)}")
            print("\n⚠️  Error details:")
            print(f"   {type(e).__name__}: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(migrate())
