import pytest
import logging
from main import count_vowels_and_consonants
from main import init_db, add_user, get_user

# Настройка логирования

fh = logging.FileHandler('Pytest.log')
fh.setLevel(logging.INFO)

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(request.node.name)s - %(levelname)s - %(message)s',
#                     handlers=[
#                         logging.FileHandler("pytest.log"),
#                         logging.StreamHandler()
#                     ]
#                     )
logger = logging.getLogger(__name__)
logger.addHandler(fh)


@pytest.fixture(autouse=True)
def db_conn(request):
    conn = init_db()
    # Логирование начала теста
    logger.info("Starting test: %s", request.node.name)
    yield conn
    # Логирование окончания теста
    logger.info("Finished test: %s", request.node.name)
    conn.close()

def test_add_or_get_user(db_conn):
    add_user(db_conn, "Sasha", 30)
    user = get_user(db_conn, "Sasha")
    assert user == (1, "Sasha", 30)

@pytest.mark.parametrize("name, age", [
    ("Alex", 25),
    ("Maria", 22),
    ("John", 28),
])
def test_add_multiple_users(db_conn, name, age):
    add_user(db_conn, name, age)
    user = get_user(db_conn, name)
    assert user[1] == name
    assert user[2] == age


# - Проверьте, что функция правильно считает гласные в строке, содержащей только гласные.
# - Проверьте, что функция возвращает 0 для строки, не содержащей гласных.
def test_all_vowels():
    input_str = 'aeiouyAEIOUYаеёиоуыэюяйАЕЁИОУЫЭЮЯЙ'
    num_vowels, num_consonants = count_vowels_and_consonants(input_str)
    assert num_vowels == len(input_str)
    assert num_consonants == 0
# - Проверьте, что функция правильно считает согласные в строке, содержащей только согласные.
# - Проверьте, что функция возвращает 0 для строки, не содержащей согласных.
def test_no_vowels():
    input_str = 'bcdfghjklmnpqrstvwxzБВГДЖЗКЛМНПРСТФХЦЧШЩ'
    num_vowels, num_consonants = count_vowels_and_consonants(input_str)
    assert num_vowels == 0
    assert num_consonants == len(input_str)

# - Проверьте, что функция правильно считает гласные в смешанных строках (включая прописные и строчные буквы).
def test_mixed_string():
    input_str = 'Hello Привет'
    num_vowels, num_consonants = count_vowels_and_consonants(input_str)
    assert num_vowels == 4
    assert num_consonants == 7

# - Проверьте, что функция правильно считает гласные в смешанных строках (включая прописные и строчные буквы)
# .
def test_mixed_string_mistake():
    input_str = 'Hello Привет'
    num_vowels, num_consonants = count_vowels_and_consonants(input_str)
    assert num_vowels == 4
    assert num_consonants == 8      # намеренная ошибка -  '7' исправил на '8'

# Тестовая функция с использованием библиотеки pytest, которая позволяет параметризовать тесты
@pytest.mark.parametrize("input_str, expected_vowels, expected_consonants", [
    ('', 0, 0),
    ('Python', 2, 4),
    ('Пайтон', 3, 3),
    ('1234567890', 0, 0),
    ('AaEeIiOoUuYyАаЕеЁёИиОоУуЫыЭэЮюЯя', 32, 0),
    ('The quick brown fox jumps over the lazy dog', 12, 23),
    ('Съешь ещё этих мягких французских булок, да выпей же чаю', 19, 25),  # исправлено на 25
])
def test_count_vowels_and_consonants_parametrized(input_str, expected_vowels, expected_consonants):
    num_vowels, num_consonants = count_vowels_and_consonants(input_str)
    assert num_vowels == expected_vowels
    assert num_consonants == expected_consonants