import json
from app.services.search_service import search_by_name

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Search API.
    Triggered by API Gateway GET /search?name=...
    """
    print(f"Received event: {json.dumps(event)}") # Логируем входящий запрос

    # 1. Extract Query Parameters
    # API Gateway передает параметры в queryStringParameters
    query_params = event.get('queryStringParameters') or {}
    name_query = query_params.get('name')

    # 2. Validation
    if not name_query or len(name_query) < 2:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" # Открываем CORS для всех
            },
            "body": json.dumps({
                "error": "Missing or invalid 'name' parameter. Min length is 2."
            })
        }

    # 3. Call Service Layer (Business Logic)
    try:
        results = search_by_name(name_query)
        
        # 4. Return Success Response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "query": name_query,
                "count": len(results),
                "data": results
            }, default=str) # default=str нужен для сериализации Decimal типов DynamoDB
        }

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Internal Server Error"
            })
        }