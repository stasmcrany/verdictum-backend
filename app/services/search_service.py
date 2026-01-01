import os
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from typing import List, Dict, Any

# CONFIGURATION
TABLE_NAME = os.environ.get('TABLE_NAME')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# INITIALIZATION
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None

def search_by_name(name_query: str) -> List[Dict[str, Any]]:
    """
    Performs an exact match search by normalized name.
    
    Args:
        name_query (str): The name to search for (case-insensitive).
        
    Returns:
        List[Dict]: A list of found records or an empty list.
    """
    if not table:
        print("Error: TABLE_NAME environment variable is not set.")
        return []

    # 1. Normalize Input
    # Must match the logic used in Ingest Service!
    normalized_name = name_query.strip().upper()
    pk_value = f"NAME#{normalized_name}"

    try:
        # 2. Query DynamoDB
        # We use 'Query' instead of 'GetItem' because one name (PK) 
        # might have multiple records (SKs) - e.g., in OFAC and EU lists.
        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk_value)
        )
        
        items = response.get('Items', [])
        
        # 3. Log results
        print(f"Search for '{normalized_name}': Found {len(items)} records.")
        return items

    except ClientError as e:
        print(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return []
    except Exception as e:
        print(f"Unexpected error in search: {e}")
        return []