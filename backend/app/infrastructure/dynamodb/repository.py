"""
DynamoDB repository with generic CRUD operations.
"""
from typing import Any, Dict, List, Optional, Union, Type, TypeVar
from pydantic import BaseModel
from .client import table, dynamodb_client
from datetime import datetime

T = TypeVar('T', bound=BaseModel)

class DynamoDBRepository:
    @staticmethod
    def _convert_datetime_to_iso(item_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert datetime objects to ISO 8601 strings for DynamoDB compatibility.
        
        Args:
            item_dict: Dictionary containing item data
            
        Returns:
            Dictionary with datetime objects converted to ISO 8601 strings
        """
        result = {}
        for key, value in item_dict.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = DynamoDBRepository._convert_datetime_to_iso(value)
            elif isinstance(value, list):
                result[key] = [
                    DynamoDBRepository._convert_datetime_to_iso(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    @staticmethod
    async def put_item(item: BaseModel) -> Dict[str, Any]:
        """
        Put an item in the DynamoDB table.
        
        Args:
            item: Pydantic model instance to save
            
        Returns:
            The response from DynamoDB
        """
        item_dict = item.model_dump()
        # Convert datetime objects to ISO 8601 strings
        item_dict = DynamoDBRepository._convert_datetime_to_iso(item_dict)
        response = table.put_item(Item=item_dict)
        return response

    @staticmethod
    async def get_item(key: Dict[str, Any], model_class: Type[T]) -> Optional[T]:
        """
        Get an item from the DynamoDB table and convert it to a Pydantic model.
        
        Args:
            key: Dictionary containing the primary key
            model_class: The Pydantic model class to convert the item to
            
        Returns:
            The item as a Pydantic model if found, None otherwise
        """
        response = table.get_item(Key=key)
        item = response.get('Item')
        if item:
            return model_class.model_validate(item)
        return None

    @staticmethod
    async def update_item(
        key: Dict[str, Any],
        update_expression: str,
        expression_attribute_values: Dict[str, Any],
        expression_attribute_names: Optional[Dict[str, str]] = None,
        model_class: Optional[Type[T]] = None
    ) -> Optional[T]:
        """
        Update an item in the DynamoDB table.
        
        Args:
            key: Dictionary containing the primary key
            update_expression: The update expression
            expression_attribute_values: Values for the update expression
            expression_attribute_names: Names for the update expression
            model_class: Optional Pydantic model class to convert the response to
            
        Returns:
            The updated item as a Pydantic model if model_class is provided, otherwise the raw response
        """
        params = {
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'ALL_NEW'
        }
        
        if expression_attribute_names:
            params['ExpressionAttributeNames'] = expression_attribute_names
            
        response = table.update_item(**params)
        item = response.get('Attributes')
        
        if item and model_class:
            return model_class.model_validate(item)
        return item

    @staticmethod
    async def delete_item(key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete an item from the DynamoDB table.
        
        Args:
            key: Dictionary containing the primary key
            
        Returns:
            The response from DynamoDB
        """
        response = table.delete_item(Key=key)
        return response

    @staticmethod
    async def query(
        key_condition_expression: str,
        expression_attribute_values: Dict[str, Any],
        expression_attribute_names: Optional[Dict[str, str]] = None,
        filter_expression: Optional[str] = None,
        limit: Optional[int] = None,
        model_class: Optional[Type[T]] = None
    ) -> List[Union[Dict[str, Any], T]]:
        """
        Query items from the DynamoDB table.
        
        Args:
            key_condition_expression: The key condition expression
            expression_attribute_values: Values for the query expression
            expression_attribute_names: Names for the query expression
            filter_expression: Optional filter expression
            limit: Optional limit for the number of items
            model_class: Optional Pydantic model class to convert items to
            
        Returns:
            List of items matching the query, as Pydantic models if model_class is provided
        """
        params = {
            'KeyConditionExpression': key_condition_expression,
            'ExpressionAttributeValues': expression_attribute_values
        }
        
        if expression_attribute_names:
            params['ExpressionAttributeNames'] = expression_attribute_names
            
        if filter_expression:
            params['FilterExpression'] = filter_expression
            
        if limit:
            params['Limit'] = limit
            
        response = table.query(**params)
        items = response.get('Items', [])
        
        if model_class:
            return [model_class.model_validate(item) for item in items]
        return items

    @staticmethod
    async def scan(
        filter_expression: Optional[str] = None,
        expression_attribute_values: Optional[Dict[str, Any]] = None,
        expression_attribute_names: Optional[Dict[str, str]] = None,
        limit: Optional[int] = None,
        model_class: Optional[Type[T]] = None
    ) -> List[Union[Dict[str, Any], T]]:
        """
        Scan items from the DynamoDB table.
        
        Args:
            filter_expression: Optional filter expression
            expression_attribute_values: Values for the scan expression
            expression_attribute_names: Names for the scan expression
            limit: Optional limit for the number of items
            model_class: Optional Pydantic model class to convert items to
            
        Returns:
            List of items matching the scan, as Pydantic models if model_class is provided
        """
        params = {}
        
        if filter_expression:
            params['FilterExpression'] = filter_expression
            
        if expression_attribute_values:
            params['ExpressionAttributeValues'] = expression_attribute_values
            
        if expression_attribute_names:
            params['ExpressionAttributeNames'] = expression_attribute_names
            
        if limit:
            params['Limit'] = limit
            
        response = table.scan(**params)
        items = response.get('Items', [])
        
        if model_class:
            return [model_class.model_validate(item) for item in items]
        return items
        
    @staticmethod
    async def batch_write(items: List[BaseModel]) -> Dict[str, Any]:
        """
        Write multiple items to the DynamoDB table in a batch operation.
        
        Args:
            items: List of Pydantic model instances to write
            
        Returns:
            The response from DynamoDB
        """
        # DynamoDB batch_write_item has a limit of 25 items per batch
        batch_size = 25
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]
            request_items = [{'PutRequest': {'Item': item.model_dump()}} for item in batch]
            
            response = dynamodb_client.dynamodb.meta.client.batch_write_item(
                RequestItems={
                    table.name: request_items
                }
            )
            results.append(response)
            
        return results
        
    @staticmethod
    async def batch_get(
        keys: List[Dict[str, Any]], 
        model_class: Optional[Type[T]] = None
    ) -> List[Union[Dict[str, Any], T]]:
        """
        Get multiple items from the DynamoDB table in a batch operation.
        
        Args:
            keys: List of primary keys to retrieve
            model_class: Optional Pydantic model class to convert items to
            
        Returns:
            List of items retrieved, as Pydantic models if model_class is provided
        """
        # DynamoDB batch_get_item has a limit of 100 items per batch
        batch_size = 100
        all_items = []
        
        for i in range(0, len(keys), batch_size):
            batch = keys[i:i+batch_size]
            
            response = dynamodb_client.dynamodb.meta.client.batch_get_item(
                RequestItems={
                    table.name: {
                        'Keys': batch
                    }
                }
            )
            
            items = response.get('Responses', {}).get(table.name, [])
            all_items.extend(items)
            
        if model_class:
            return [model_class.model_validate(item) for item in all_items]
        return all_items 