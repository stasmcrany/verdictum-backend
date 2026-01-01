import os
import sys
import boto3

# PATH SETUP
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# CONFIGURATION
# То же самое имя таблицы!
REAL_TABLE_NAME = "VerdictumSanctions" 
os.environ['TABLE_NAME'] = REAL_TABLE_NAME
os.environ['AWS_REGION'] = 'us-east-1'

print(f"🔎 Запуск теста поиска. Таблица: {REAL_TABLE_NAME}")

try:
    from app.services.search_service import search_by_name
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

# AUTH SETUP (Если сессия еще активна, ключи подхватятся. Если нет - вставь их снова в Env)
try:
    session = boto3.Session()
    if not session.get_credentials():
        print("⚠️ Нет кредов! Задай AWS_ACCESS_KEY_ID и AWS_SECRET_ACCESS_KEY в терминале.")
except:
    pass

# TEST EXECUTION
# 1. Поиск существующего (разный регистр, чтобы проверить нормализацию)
query = "Pablo Escobar" 
print(f"Testing search for: '{query}'...")
results = search_by_name(query)

if results:
    print("✅ НАЙДЕНО!")
    for item in results:
        print(f" - {item.get('name')} (Source: {item.get('source')})")
else:
    print("❌ НИЧЕГО НЕ НАЙДЕНО (А должно быть).")

print("-" * 20)

# 2. Поиск несуществующего
query_fake = "Ivan Drago"
print(f"Testing search for: '{query_fake}'...")
results_fake = search_by_name(query_fake)

if not results_fake:
    print("✅ КОРРЕКТНО: Иван Драго чист перед законом.")
else:
    print("❌ ОШИБКА: Нашли кого-то лишнего.")