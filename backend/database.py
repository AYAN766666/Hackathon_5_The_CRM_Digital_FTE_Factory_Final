"""
Database Configuration and Session Management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
import sys

# Add parent path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


# Create async engine with asyncpg driver
# Convert postgresql:// to postgresql+asyncpg:// for async support
database_url = settings.database_url

# Handle different URL formats for asyncpg
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

# Fix SSL parameters for asyncpg
# Replace sslmode=require with ssl=require (asyncpg format)
database_url = database_url.replace("sslmode=require", "ssl=require")
# Remove channel_binding as asyncpg doesn't support it
database_url = database_url.replace("&channel_binding=require", "")

# If using ssl=true, convert to ssl=require for proper validation
database_url = database_url.replace("ssl=true", "ssl=require")

engine = create_async_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Dependency for getting database session"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db(retries: int = 3, delay: int = 2):
    """Initialize database - create all tables with retry logic"""
    import asyncio
    
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print(f"[OK] Database tables created successfully")
            return
        except Exception as e:
            last_error = e
            error_msg = str(e)
            print(f"[WARN] Database init attempt {attempt}/{retries} failed: {error_msg}")
            
            if attempt < retries:
                print(f"   Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                # Provide helpful error messages based on error type
                if "getaddrinfo" in error_msg or "Name or service not known" in error_msg:
                    print("\n[ERROR] CONNECTION ERROR: Cannot resolve database hostname")
                    print("   Please check:")
                    print("   1. Your DATABASE_URL in .env file is correct")
                    print("   2. You have an active internet connection")
                    print("   3. The database server is accessible")
                elif "connection refused" in error_msg.lower():
                    print("\n[ERROR] CONNECTION ERROR: Database refused connection")
                    print("   Please check:")
                    print("   1. Database server is running")
                    print("   2. Database port is accessible")
                    print("   3. Firewall settings allow connections")
                elif "authentication" in error_msg.lower() or "password" in error_msg.lower():
                    print("\n[ERROR] AUTHENTICATION ERROR: Database login failed")
                    print("   Please check:")
                    print("   1. DATABASE_URL username and password are correct")
                elif "SSL" in error_msg or "ssl" in error_msg.lower():
                    print("\n[ERROR] SSL ERROR: Database SSL connection failed")
                    print("   Try adding ?sslmode=disable to your DATABASE_URL (development only)")
                else:
                    print(f"\n[ERROR] Database error: {error_msg}")
    
    # Re-raise the last error after all retries
    raise last_error
