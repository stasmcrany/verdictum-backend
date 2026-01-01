import os
import sys
import boto3

# ХАК: Добавляем корневую папку проекта в sys.path
# Это нужно, чтобы Python увидел папку 'app', которая лежит на уровень выше
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# 1. НАСТРОЙКА
# Имя твоей реальной таблицы, которое мы нашли в консоли
REAL_TABLE_NAME = "VerdictumSanctions" 

os.environ['TABLE_NAME'] = REAL_TABLE_NAME
# Обычно us-east-1, если не менял
os.environ['AWS_REGION'] = 'us-east-1' 

print(f"🚀 Запуск теста. Цель: таблица {REAL_TABLE_NAME}")

try:
    # Пытаемся импортировать наш новый сервис
    from app.services.ingest_service import save_sanction
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедись, что папка 'app' существует и в ней есть файл '__init__.py' (опционально для Python 3.3+, но желательно).")
    sys.exit(1)

# 2. ТЕСТОВЫЕ ДАННЫЕ
test_data = {
    "name": "Pablo Emilio Escobar Gaviria",
    "normalized_name": "PABLO ESCOBAR",
    "source": "OFAC",
    "entity_type": "INDIVIDUAL",
    "country": "Colombia",
    "remarks": "Test from Local v0.2 script"
}

# 3. ЗАПУСК
print(f"💾 Пытаюсь сохранить: {test_data['name']}...")

# Инициализируем сессию явно, чтобы подхватить профиль из .aws/credentials
# Если скрипт падает на правах доступа, это поможет понять причину
try:
    session = boto3.Session()
    credentials = session.get_credentials()
    if not credentials:
        print("⚠️ ВНИМАНИЕ: AWS Credentials не найдены! Убедись, что настроил aws configure.")
except Exception:
    pass

result = save_sanction(test_data)

if result:
    print("✅ УСПЕХ! Данные записаны в DynamoDB.")
    print("Теперь можешь зайти в AWS Console -> DynamoDB -> Explore Items и увидеть там Пабло.")
else:
    print("❌ ПРОВАЛ. Смотри ошибку выше.")