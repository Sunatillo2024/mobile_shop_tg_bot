from app.database.db import SessionLocal
from app.database.models import User, Category, Product, CartItem, Address, Order, OrderItem
from sqlalchemy.exc import IntegrityError
from typing import Optional, List


def save_user_to_db(telegram_id: int, full_name: str = None) -> Optional[User]:
    db = SessionLocal()
    try:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        # User already exists, return existing user
        existing_user = db.query(User).filter_by(telegram_id=telegram_id).first()
        return existing_user
    except Exception as e:
        db.rollback()
        print(f"Ошибка при сохранении пользователя: {e}")
        return None
    finally:
        db.close()


def check_user_in_db(telegram_id: int) -> Optional[User]:
    db = SessionLocal()
    try:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        return user
    except Exception as e:
        print(f"[Error] {e}")
        return None
    finally:
        db.close()


def get_category_name_from_db() -> List[tuple]:
    db = SessionLocal()
    try:
        categories = db.query(Category.id, Category.name).filter_by(is_active=True).all()
        return categories
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()


def get_products_item_from_db(category_id: int) -> List[Product]:
    db = SessionLocal()
    try:
        products = db.query(Product).filter_by(
            category_id=category_id,
            is_active=True
        ).filter(Product.available > 0).all()
        return products
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()


def get_product_by_id(product_id: int) -> Optional[Product]:
    db = SessionLocal()
    try:
        product = db.query(Product).filter_by(id=product_id, is_active=True).first()
        return product
    except Exception as e:
        print(f"[Error] {e}")
        return None
    finally:
        db.close()


def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> bool:
    db = SessionLocal()
    try:
        # Check if item already exists in cart
        existing_item = db.query(CartItem).filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[Error adding to cart] {e}")
        return False
    finally:
        db.close()


def get_cart_items(user_id: int) -> List[CartItem]:
    db = SessionLocal()
    try:
        cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
        return cart_items
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()


def update_cart_quantity(user_id: int, product_id: int, quantity: int) -> bool:
    db = SessionLocal()
    try:
        cart_item = db.query(CartItem).filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()

        if cart_item:
            if quantity <= 0:
                db.delete(cart_item)
            else:
                cart_item.quantity = quantity
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"[Error updating cart] {e}")
        return False
    finally:
        db.close()


def clear_cart(user_id: int) -> bool:
    db = SessionLocal()
    try:
        db.query(CartItem).filter_by(user_id=user_id).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[Error clearing cart] {e}")
        return False
    finally:
        db.close()


def save_address(user_id: int, address_text: str, latitude: float = None, longitude: float = None) -> bool:
    db = SessionLocal()
    try:
        # Deactivate old addresses
        db.query(Address).filter_by(user_id=user_id).update({"is_active": False})

        # Add new address
        address = Address(
            user_id=user_id,
            address_text=address_text,
            latitude=latitude,
            longitude=longitude,
            is_active=True
        )
        db.add(address)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[Error saving address] {e}")
        return False
    finally:
        db.close()


def get_user_address(user_id: int) -> Optional[Address]:
    db = SessionLocal()
    try:
        address = db.query(Address).filter_by(user_id=user_id, is_active=True).first()
        return address
    except Exception as e:
        print(f"[Error] {e}")
        return None
    finally:
        db.close()


def create_order(user_id: int, phone_number: str = None) -> Optional[Order]:
    db = SessionLocal()
    try:
        # Get cart items
        cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
        if not cart_items:
            return None

        # Get user address
        address = db.query(Address).filter_by(user_id=user_id, is_active=True).first()
        if not address:
            return None

        # Calculate total price
        total_price = 0
        for item in cart_items:
            product = db.query(Product).filter_by(id=item.product_id).first()
            if product:
                total_price += product.price * item.quantity

        # Create order
        order = Order(
            user_id=user_id,
            total_price=total_price,
            delivery_address=address.address_text,
            phone_number=phone_number,
            status="pending"
        )
        db.add(order)
        db.flush()  # Get order ID

        # Create order items
        for item in cart_items:
            product = db.query(Product).filter_by(id=item.product_id).first()
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price_at_order=product.price
                )
                db.add(order_item)

        # Clear cart
        db.query(CartItem).filter_by(user_id=user_id).delete()

        db.commit()
        db.refresh(order)
        return order
    except Exception as e:
        db.rollback()
        print(f"[Error creating order] {e}")
        return None
    finally:
        db.close()


def get_user_orders(user_id: int) -> List[Order]:
    db = SessionLocal()
    try:
        orders = db.query(Order).filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return orders
    except Exception as e:
        print(f"[Error] {e}")
        return []
    finally:
        db.close()