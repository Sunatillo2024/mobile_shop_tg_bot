# 🛍️ mobile_shop_tg_bot

Welcome to the **Mobile Shop Telegram Bot** — a fast, interactive, and simple solution for online shopping using Telegram!  
Built with `aiogram`, `PostgreSQL`, and Python 💡

---

## 📦 Features

✅ Browse and search mobile products  
✅ Add items to basket  
✅ Share your 📍 location for delivery  
✅ Place and track orders  
✅ Admin panel for managing products and orders  
✅ Multi-step user input using FSM (Finite State Machine)

---

## 🧠 Technologies Used

| Tool          | Purpose                             |
|---------------|-------------------------------------|
| Python        | Backend logic                       |
| Aiogram       | Telegram bot framework              |
| PostgreSQL    | Relational database                 |
| SQLAlchemy    | ORM for database models             |
| FSM (aiogram) | Handling multi-step user flows      |

---

## 🚀 How to Run

### 1. Clone the Repository bash 

git clone https://github.com/Sunatillo2024/mobile_shop_tg_bot.git
cd mobile_shop_tg_bot

## 2. Create and Activate a Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt


4. Configure Environment Variables
Create a .env file:

5.env

BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql://user:password@localhost:5432/your_db

 Run the Bot
bash

python app/main.py






