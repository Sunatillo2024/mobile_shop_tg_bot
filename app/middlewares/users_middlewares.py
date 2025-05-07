# from aiogram import BaseMiddleware
# from aiogram.types import Message
# from typing import Callable, Dict, Any
# from app.database.db import SessionLocal
# from app.database.models import User
#
#
# class UserRegistrationMiddleware(BaseMiddleware):
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Any],
#         event: Message,
#         data: Dict[str, Any]
#     ) -> Any:
#         db = SessionLocal()
#         try:
#             user_id = event.from_user.id
#             user = db.query(User).filter_by(telegram_id=user_id).first()
#
#             if not user:
#                 # User doesn't exist, create new user
#                 new_user = User(
#                     telegram_id=user_id,
#                     full_name=event.from_user.full_name,
#                 )
#                 db.add(new_user)
#                 db.commit()
#                 db.refresh(new_user)
#                 data["db_user"] = new_user  # Attach new user to data
#             else:
#                 # User already exists, attach existing user
#                 data["db_user"] = user
#         except Exception as e:
#             db.rollback()
#             print(f"[Middleware Error] {e}")
#             data["db_user"] = None  # In case of error, ensure no user is passed
#         finally:
#             db.close()
#
#         return await handler(event, data)
#
#
