from models import Base, Publisher, Book, Shop, Stock, Sale
from sqlalchemy import create_engine

# 1. Создаем движок для SQLite в памяти
engine = create_engine('sqlite:///:memory:')

# 2. Создаем все таблицы
Base.metadata.create_all(engine)

print("Все таблицы успешно созданы!")