import json
import redis
from app.config import config


class CartService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

    def _get_cart_key(self, user_id: int) -> str:
        return f"cart:{user_id}"

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        cart_key = self._get_cart_key(user_id)
        current_quantity = self.redis_client.hget(cart_key, str(product_id))

        if current_quantity:
            quantity = int(current_quantity) + quantity

        self.redis_client.hset(cart_key, str(product_id), quantity)

    async def remove_from_cart(self, user_id: int, product_id: int):
        cart_key = self._get_cart_key(user_id)
        self.redis_client.hdel(cart_key, str(product_id))

    async def get_cart(self, user_id: int) -> dict:
        cart_key = self._get_cart_key(user_id)
        cart_data = self.redis_client.hgetall(cart_key)
        return {int(k): int(v) for k, v in cart_data.items()}

    async def clear_cart(self, user_id: int):
        cart_key = self._get_cart_key(user_id)
        self.redis_client.delete(cart_key)

    async def update_cart_item(self, user_id: int, product_id: int, quantity: int):
        cart_key = self._get_cart_key(user_id)
        if quantity <= 0:
            await self.remove_from_cart(user_id, product_id)
        else:
            self.redis_client.hset(cart_key, str(product_id), quantity)


cart_service = CartService()