import json
import os
import boto3
from boto3.dynamodb.conditions import Key

# Инициализация DynamoDB
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # Стандартные заголовки для CORS (чтобы браузер не ругался)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    }

    try:
        # Получаем параметры запроса (?name=...)
        query_params = event.get('queryStringParameters')
        if not query_params or 'name' not in query_params:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Missing 'name' parameter"})
            }

        name_query = query_params['name'].strip().upper()
        
        # Поиск в DynamoDB (PK = NAME#<QUERY>)
        # В реальном проекте тут нужна нормализация, но пока ищем точное совпадение
        pk = f"NAME#{name_query}"
        
        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk)
        )
        
        items = response.get('Items', [])
        
        # Преобразуем данные для фронтенда
        results = []
        for item in items:
            # Разбираем SK, чтобы достать источник (SOURCE#OFAC -> OFAC)
            source = item.get('SK', '').replace('SOURCE#', '')
            results.append({
                "name": item.get('normalized_name', 'Unknown'),
                "source": source,
                "raw_data": item # Можно убрать, если не нужно
            })

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"results": results})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }