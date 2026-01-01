import json
from app.services.ingest_service import save_sanction

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Admin Ingest API.
    Triggered by API Gateway POST /ingest
    Expected Body: JSON with sanction data.
    """
    print(f"Received ingest request")

    try:
        # 1. Parse Body
        if 'body' not in event:
            return {"statusCode": 400, "body": json.dumps({"error": "Empty body"})}
        
        # Если body приходит как строка (обычно так и есть в Proxy integration), парсим её
        body = event['body']
        if isinstance(body, str):
            body = json.loads(body)
            
        # 2. Call Service
        success = save_sanction(body)
        
        if success:
            return {
                "statusCode": 201,
                "body": json.dumps({"message": "Created", "id": body.get("normalized_name")})
            }
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Validation failed or DB error"})
            }

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}