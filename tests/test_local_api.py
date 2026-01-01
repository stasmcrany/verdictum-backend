import os
import sys
import json

# PATH SETUP
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# CONFIG
REAL_TABLE_NAME = "VerdictumSanctions" # Твоя таблица
os.environ['TABLE_NAME'] = REAL_TABLE_NAME
os.environ['AWS_REGION'] = 'us-east-1'

try:
    from app.api.search_handler import lambda_handler
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

# AUTH (Если нужно обновить сессию)
import boto3
try:
    if not boto3.Session().get_credentials():
        print("⚠️ Нет кредов! Задай их в терминале, если тест упадет.")
except:
    pass

# 1. Имитация запроса от API Gateway
fake_event = {
    "queryStringParameters": {
        "name": "pablo escobar"
    }
}

print("🌐 Simulating API Gateway Request...")
response = lambda_handler(fake_event, None)

# 2. Анализ ответа
print(f"Status Code: {response['statusCode']}")
print("Body:")
# Красивый вывод JSON
parsed_body = json.loads(response['body'])
print(json.dumps(parsed_body, indent=2, ensure_ascii=False))

if response['statusCode'] == 200 and parsed_body['count'] > 0:
    print("\n✅ API HANDLER РАБОТАЕТ!")
else:
    print("\n❌ ЧТО-ТО ПОШЛО НЕ ТАК.")