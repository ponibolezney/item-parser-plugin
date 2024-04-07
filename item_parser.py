import re
import sqlite3
import os

def parse_and_insert_item(input_str):
    # Определяем путь к директории со скриптом
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Формируем полный путь к БД относительно директории скрипта
    db_path = os.path.join(script_dir, 'game_database.db')

    # Подключаемся к БД
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Парсинг параметров
    pattern = r'!Добыча: \[(.*?), \'(.*?)\', (.*?), (\d+)\]'
    match = re.match(pattern, input_str)

    if match:
        item_type, name, description, damage = match.groups()

        # Создаем новый item_type если нужно
        c.execute("INSERT OR IGNORE INTO item_types (type) VALUES (?)", (item_type,))
        item_type_id = c.execute("SELECT id FROM item_types WHERE type = ?", (item_type,)).fetchone()[0]

        # Вставка в items
        c.execute("INSERT INTO items (name, description, item_type_id) VALUES (?, ?, ?)",
                  (name, description, item_type_id))
        item_id = c.lastrowid

        # Вставка в weapons или armors
        is_weapon = c.execute("SELECT is_weapon FROM item_types WHERE id = ?", (item_type_id,)).fetchone()[0]
        if is_weapon:
            c.execute("INSERT INTO weapons (item_id, damage) VALUES (?, ?)", (item_id, int(damage)))
        else:
            is_armor = c.execute("SELECT is_armor FROM item_types WHERE id = ?", (item_type_id,)).fetchone()[0]
            if is_armor:
                c.execute("INSERT INTO armors (item_id, defence) VALUES (?, ?)", (item_id, int(damage)))

        conn.commit()
        conn.close()
        print(f"Успешно добавлен новый предмет: {name}")
    else:
        print("Некорректный формат входной строки")

# Пример использования
input_str = "!Добыча: [Тяжелый стальной меч, 'Хребет Вершителя', Прочный и сбалансированный двуручный меч, 15]"
parse_and_insert_item(input_str)