import json
import boto3
import os
import logging

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Инициализация DynamoDB
dynamodb = boto3.resource('dynamodb')
# Если переменная окружения не задана (локально), имя стола может быть None, это ок для тестов
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None

def lambda_handler(event, context):
    # Заголовки для CORS
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Если это пре-запрос (OPTIONS) от браузера - сразу возвращаем ОК
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    try:
        logger.info(f"Received event: {event}")

        if not table:
            raise Exception("TABLE_NAME environment variable is not set")

        # 1. Разбираем тело запроса
        if 'body' not in event or event['body'] is None:
            raise ValueError("No body provided")
        
        body_str = event['body']
        if isinstance(body_str, str):
            body = json.loads(body_str)
        else:
            body = body_str

        # 2. Валидация
        name = body.get('name')
        source = body.get('source')
        
        if not name or not source:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Fields 'name' and 'source' are required"})
            }

        # 3. Нормализация и создание записи
        normalized_name = name.strip().upper()

        item = {
            'PK': f"NAME#{normalized_name}",
            'SK': f"SOURCE#{source}",
            'normalized_name': normalized_name,
            'original_name': name,
            'source': source,
            'reason': body.get('reason', 'N/A'),
            'type': 'INDIVIDUAL' # Добавляем тип на будущее
        }

        # 4. Сохранение
        table.put_item(Item=item)
        logger.info(f"Successfully ingested: {name}")

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({"message": "Created", "item": item})
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }