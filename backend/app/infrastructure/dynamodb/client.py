"""
DynamoDB client configuration.
"""
import os
import boto3
from botocore.config import Config
from typing import Optional


class DynamoDBClient:
    """
    DynamoDB client class for interacting with DynamoDB tables.
    """
    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize the DynamoDB client.
        
        Args:
            table_name: Optional table name. If not provided, will use the environment variable.
        """
        self.table_name = table_name or os.environ.get('DYNAMODB_TABLE_NAME')
        if not self.table_name:
            raise ValueError("DynamoDB table name must be provided or set in DYNAMODB_TABLE_NAME environment variable")
            
        self.config = self._create_config()
        self.dynamodb = self._create_resource()
        self.table = self._get_table()
    
    def _create_config(self) -> Config:
        """
        Create the boto3 configuration with retries and timeouts.
        
        Returns:
            boto3 Config object
        """
        return Config(
            retries=dict(
                max_attempts=3,
                mode='standard'
            ),
            connect_timeout=5,
            read_timeout=5
        )
    
    def _create_resource(self):
        """
        Create the DynamoDB resource.
        
        Returns:
            boto3 DynamoDB resource
        """
        return boto3.resource('dynamodb', config=self.config)
    
    def _get_table(self):
        """
        Get the DynamoDB table resource.
        
        Returns:
            boto3 DynamoDB Table resource
        """
        return self.dynamodb.Table(self.table_name)
    
    def get_table(self):
        """
        Get the DynamoDB table resource.
        
        Returns:
            boto3 DynamoDB Table resource
        """
        return self.table


# Create a singleton instance
dynamodb_client = DynamoDBClient()
table = dynamodb_client.get_table() 