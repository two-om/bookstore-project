"""
main.py - Поиск продаж книг по издателю
"""

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale

def get_db_session():
    """Создаёт и возвращает сессию для работы с БД"""
    DSN = "postgresql://postgres:postgres@localhost:5432/netology_db"
    engine = sq.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    return Session()

def get_publisher_filter(user_input):
    """Создаёт фильтр для поиска издателя"""
    if user_input.isdigit():
        return Publisher.id == int(user_input)
    else:
        return Publisher.name.ilike(f"%{user_input}%")  # Поиск по части имени

def query_sales_by_publisher(session, search_filter):
    """Выполняет запрос продаж по издателю"""
    query = session.query(
        Book.title.label("book_title"),
        Shop.name.label("shop_name"),
        Sale.price,
        Sale.date_sale
    ).join(Stock, Sale.id_stock == Stock.id) \
        .join(Book, Stock.id_book == Book.id) \
        .join(Shop, Stock.id_shop == Shop.id) \
        .join(Publisher, Book.id_publisher == Publisher.id) \
        .filter(search_filter) \
        .order_by(Sale.date_sale.desc())  # Сортируем по дате (новые сверху)

    return query.all()

def format_results(results):
    """Форматирует результаты для вывода"""
    if not results:
        return "Продажи книг этого издателя не найдены."

    output_lines = []
    for book_title, shop_name, price, date_sale in results:
        date_str = date_sale.strftime("%d-%m-%Y")
        output_lines.append(f"{book_title} | {shop_name} | {price} | {date_str}")

    return "\n".join(output_lines)

def main():
    """Основная функция скрипта"""
    print("=" * 50)
    print("ПОИСК ПРОДАЖ КНИГ ПО ИЗДАТЕЛЮ")
    print("=" * 50)

    # Получаем ввод от пользователя
    user_input = input("Введите имя или ID издателя: ").strip()

    if not user_input:
        print("Ошибка: введите имя или ID издателя")
        return

    # Создаём сессию
    session = get_db_session()

    try:
        # Создаём фильтр
        search_filter = get_publisher_filter(user_input)

        # Выполняем запрос
        results = query_sales_by_publisher(session, search_filter)

        # Выводим результаты
        print("\n" + "=" * 50)
        print(f"РЕЗУЛЬТАТЫ ПОИСКА:")
        print("=" * 50)
        print(format_results(results))
        print(f"\nНайдено записей: {len(results)}")

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        session.close()
        print("\nСессия закрыта")

if __name__ == "__main__":
    main()