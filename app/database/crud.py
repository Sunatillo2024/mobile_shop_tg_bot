from app.database.db import SessionLocal
from app.database.models import User, Category, Product


def save_user_to_db(telegram_id, full_name=None,):
    db = SessionLocal()
    try:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user  # Returning the user after committing to the DB
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении пользователя: {e}")
        return None
    finally:
        db.close()


def check_user_in_db(telegram_id):
    db = SessionLocal()
    try:
        query = db.query(User).filter_by(telegram_id=telegram_id)
        user = query.first()  # Fetch the first match (or None if no match)

        return user  # Return user object if found, otherwise None
    except Exception as e:
        print(f"[Error] {e}")
        return None
    finally:
        db.close()





def get_category_name_from_db():
    db = SessionLocal()
    try:
        categories = db.query(Category.id, Category.name).all()  # Получаем id и name
        print(categories)  # Для отладки
        return categories
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()


def get_products_item_from_db(category_id):
    db = SessionLocal()
    try:
        products = db.query(Product).filter_by(category_id=category_id).all()
        return products
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()

async def user_create_or_get(data):
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=data.telegram_id).first()
        if user:
            return user
        else:
            user = User(**data.dict())
            db.add(user)        # yangi userni qo‘shish
            db.commit()         # transactionni saqlash
            db.refresh(user)    # qayta yuklash (id va boshqa fieldlar uchun)
            return user
    except Exception as e:
        db.rollback()  # xatolik bo‘lsa orqaga qaytar
        raise e
    finally:
        db.close()


