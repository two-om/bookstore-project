import json
from datetime import datetime
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Stock, Book, Sale

def load_json_data(filename):
    """Загружает данные из JSON-файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_tables(engine):
    """Создаёт таблицы в базе данных"""
    from models import Base
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('Таблицы созданы')

def fill_database(session, data):
    """Заполняет базу данных из загруженных данных"""
    model_classes = {
        'publisher': Publisher,
        'shop': Shop,
        'stock': Stock,
        'book': Book,
        'sale': Sale
    }

    for record in data:
        model_name = record['model']
        model_class = model_classes.get(model_name)

        if not model_class:
            continue

        fields = record['fields']

        # Обработка специальных полей
        if model_name == 'sale':
            fields['date_sale'] = datetime.fromisoformat(
                fields['date_sale'].replace('Z', '+00:00')
            )
            fields['price'] = float(fields['price'])

        obj = model_class(id=record['pk'], **fields)
        session.add(obj)

    session.commit()
    print(f"Загружено {len(data)} записей")

def main():
    """Основная функция"""
    # Подключение к БД
    DSN = "postgresql://postgres:postgres@localhost:5432/netology_db"
    engine = sq.create_engine(DSN)

    # Создаём таблицы
    create_tables(engine)

    # Создаём сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Загружаем данные из JSON
        data = load_json_data('fixtures/tests_data.json')

        # Заполняем БД
        fill_database(session, data)

        print("База данных успешно заполнена!")

    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()