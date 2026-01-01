import os
import boto3
from botocore.exceptions import ClientError
from app.models.sanction_model import SanctionEntity

# CONFIGURATION
# 1. Get Table Name from env or return None (handled later)
TABLE_NAME = os.environ.get('TABLE_NAME')
# 2. Get Region with a fallback default (Crucial for Local Dev!)
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# INITIALIZATION
# Pass region_name explicitly to avoid NoRegionError on local Windows machines
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME) if TABLE_NAME else None

def save_sanction(raw_data: dict) -> bool:
    """
    Validates and saves a sanction entity to DynamoDB.
    
    Args:
        raw_data (dict): Dictionary containing raw sanction data.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    if not table:
        print("Error: TABLE_NAME environment variable is not set.")
        return False

    try:
        # 1. Validation via Pydantic
        entity = SanctionEntity(**raw_data)

        # 2. Key Formation (Single Table Design)
        pk = f"NAME#{entity.normalized_name}"
        sk = f"SOURCE#{entity.source}"

        # 3. Prepare Item
        item = entity.model_dump()
        item['PK'] = pk
        item['SK'] = sk

        # 4. Write to Database
        table.put_item(Item=item)
        print(f"Successfully saved: {entity.normalized_name}")
        return True

    except ValueError as e:
        print(f"Validation Error for data {raw_data.get('name', 'Unknown')}: {e}")
        return False
        
    except ClientError as e:
        print(f"DynamoDB ClientError: {e.response['Error']['Message']}")
        return False
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False