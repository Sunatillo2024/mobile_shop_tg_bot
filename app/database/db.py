import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from app.utils.logger import the_logger
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Create engine with proper configuration
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        the_logger.info("✅ Database connection successful!")
        return True
    except OperationalError as e:
        the_logger.error(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        the_logger.error(f"❌ Unexpected database error: {e}")
        return False


def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Extract database name from URL
        db_name = DATABASE_URL.split('/')[-1]
        base_url = DATABASE_URL.rsplit('/', 1)[0]

        # Connect to postgres database to create new database
        temp_engine = create_engine(f"{base_url}/postgres")

        with temp_engine.connect() as connection:
            # Set autocommit mode for database creation
            connection.execute(text("COMMIT"))

            # Check if database exists
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name}
            )

            if not result.fetchone():
                # Create database
                connection.execute(text(f"CREATE DATABASE {db_name}"))
                the_logger.info(f"✅ Database '{db_name}' created successfully!")
            else:
                the_logger.info(f"✅ Database '{db_name}' already exists!")

    except Exception as e:
        the_logger.error(f"❌ Failed to create database: {e}")
        raise


def init_db():
    """Initialize database with tables"""
    try:
        # Test connection first
        if not test_connection():
            the_logger.error("❌ Cannot initialize database - connection failed!")
            return False

        # Import models to register them with Base
        from app.database import models

        # Create all tables
        Base.metadata.create_all(bind=engine)
        the_logger.info("✅ Database tables created successfully!")

        # Create sample data if tables are empty
        create_sample_data()

        return True

    except Exception as e:
        the_logger.error(f"❌ Error initializing database: {e}")
        return False


def create_sample_data():
    """Create sample categories and products for testing"""
    try:
        from app.database.models import Category, Product

        db = SessionLocal()

        # Check if categories already exist
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            the_logger.info("Sample data already exists, skipping...")
            db.close()
            return

        # Create sample categories
        categories = [
            Category(name="Smartphones", is_active=True),
            Category(name="Tablets", is_active=True),
            Category(name="Accessories", is_active=True),
        ]

        for category in categories:
            db.add(category)

        db.commit()

        # Create sample products
        products = [
            Product(
                name="iPhone 15 Pro",
                description="Latest iPhone with A17 Pro chip",
                price=999.99,
                category_id=1,
                available=10,
                is_active=True
            ),
            Product(
                name="Samsung Galaxy S24",
                description="Premium Android smartphone",
                price=899.99,
                category_id=1,
                available=15,
                is_active=True
            ),
            Product(
                name="iPad Air",
                description="Powerful tablet for work and play",
                price=599.99,
                category_id=2,
                available=8,
                is_active=True
            ),
            Product(
                name="Wireless Charger",
                description="Fast wireless charging pad",
                price=49.99,
                category_id=3,
                available=25,
                is_active=True
            ),
        ]

        for product in products:
            db.add(product)

        db.commit()
        db.close()

        the_logger.info("✅ Sample data created successfully!")

    except Exception as e:
        the_logger.error(f"❌ Error creating sample data: {e}")
        if 'db' in locals():
            db.rollback()
            db.close()


def drop_all_tables():
    """Drop all tables (use with caution!)"""
    try:
        from app.database import models
        Base.metadata.drop_all(bind=engine)
        the_logger.info("✅ All tables dropped successfully!")
    except Exception as e:
        the_logger.error(f"❌ Error dropping tables: {e}")