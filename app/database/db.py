from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.logger import the_logger

# Подключение к базе данных
DATABASE_URL = "postgresql://postgres:1299@localhost/Tg_bot_db_shop"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс
Base = declarative_base()

# Обязательно импортировать модели после Base!
from app.database import models


# Функция для создания таблиц
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        the_logger.info("Tables created successfully.")
    except Exception as e:
        the_logger.error(f"Error creating tables: {str(e)}")
