# Configure the AWS Provider and required version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Set the AWS region for all resources
provider "aws" {
  region = var.aws_region
}

# ECR Repository to store Docker images
# This is where our FastAPI application container images will be stored
resource "aws_ecr_repository" "app" {
  name = var.ecr_repository_name

  # Enable vulnerability scanning on image push
  image_scanning_configuration {
    scan_on_push = true
  }

  # Allow image tags to be overwritten
  image_tag_mutability = "MUTABLE"
}

# ECR Lifecycle Policy
# Automatically clean up untagged images to save storage costs
resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Remove untagged images"
        selection = {
          tagStatus     = "untagged"
          countType     = "sinceImagePushed"
          countUnit     = "days"
          countNumber   = 1
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# EventBridge Rule to monitor ECR image pushes
# This rule triggers when a new image is pushed to our ECR repository
resource "aws_cloudwatch_event_rule" "ecr_push" {
  name        = "${var.lambda_function_name}-ecr-push"
  description = "Capture ECR image push events"

  event_pattern = jsonencode({
    source      = ["aws.ecr"]
    detail-type = ["ECR Image Action"]
    detail = {
      action-type = ["PUSH"]
      repository-name = [aws_ecr_repository.app.name]
    }
  })
}

# EventBridge Target
# Configures the Lambda function as the target for ECR push events
resource "aws_cloudwatch_event_target" "lambda_update" {
  rule      = aws_cloudwatch_event_rule.ecr_push.name
  target_id = "UpdateLambdaFunction"
  arn       = aws_lambda_function.app.arn
  role_arn  = aws_iam_role.lambda_update_role.arn
}

# API Gateway HTTP API
# Creates a modern HTTP API that will expose our Lambda function
resource "aws_apigatewayv2_api" "lambda" {
  name          = "${var.lambda_function_name}-api"
  protocol_type = "HTTP"
}

# API Gateway Stage
# Deployment stage for the HTTP API (e.g., prod, dev)
resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id
  name   = var.environment
  auto_deploy = true

  # Configure access logs for API Gateway
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip            = "$context.identity.sourceIp"
      requestTime   = "$context.requestTime"
      httpMethod    = "$context.httpMethod"
      routeKey      = "$context.routeKey"
      status        = "$context.status"
      protocol      = "$context.protocol"
      responseTime  = "$context.responseLatency"
      integrationError = "$context.integration.error"
    })
  }
}

# CloudWatch Log Group for API Gateway
# Stores API Gateway access logs with 30-day retention
resource "aws_cloudwatch_log_group" "api_gw" {
  name              = "/aws/apigateway/${var.lambda_function_name}"
  retention_in_days = 30
}

# CloudWatch Log Group for Lambda
# Stores Lambda function logs with 30-day retention
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 30
}

# S3 Bucket for file storage
resource "aws_s3_bucket" "app" {
  bucket = var.s3_bucket_name
}

# S3 Bucket versioning
resource "aws_s3_bucket_versioning" "app" {
  bucket = aws_s3_bucket.app.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "app" {
  bucket = aws_s3_bucket.app.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket lifecycle rule
resource "aws_s3_bucket_lifecycle_configuration" "app" {
  bucket = aws_s3_bucket.app.id

  rule {
    id     = "cleanup_old_versions"
    status = "Enabled"

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

# Add S3 bucket policy to allow Lambda access
resource "aws_s3_bucket_policy" "app" {
  bucket = aws_s3_bucket.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowLambdaAccess"
        Effect    = "Allow"
        Principal = {
          AWS = aws_iam_role.lambda_role.arn
        }
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.app.arn,
          "${aws_s3_bucket.app.arn}/*"
        ]
      }
    ]
  })
}

# DynamoDB Table
resource "aws_dynamodb_table" "app" {
  name           = "${var.lambda_function_name}-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  
  attribute {
    name = "pk"
    type = "S"
  }

  tags = {
    Name = "${var.lambda_function_name}-table"
  }
}

# IAM Policy for S3 access
resource "aws_iam_role_policy" "lambda_s3" {
  name = "${var.lambda_function_name}-s3-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          aws_s3_bucket.app.arn,
          "${aws_s3_bucket.app.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.app.arn
        ]
      }
    ]
  })
}

# Lambda Function
# The main FastAPI application running in a container
resource "aws_lambda_function" "app" {
  function_name = var.lambda_function_name
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app.repository_url}:latest"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 60  # Increased from 30 to 60 seconds
  memory_size   = 512 # Increased from 256 to 512 MB

  environment {
    variables = {
      ENVIRONMENT            = var.environment
      ECR_REPOSITORY_NAME    = var.ecr_repository_name
      LAMBDA_FUNCTION_NAME   = var.lambda_function_name
      S3_BUCKET_NAME         = var.s3_bucket_name
      DYNAMODB_TABLE_NAME    = aws_dynamodb_table.app.name
    }
  }
}

# API Gateway Integration
# Connects the HTTP API to the Lambda function
resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.lambda.id
  integration_type = "AWS_PROXY"

  connection_type      = "INTERNET"
  description         = "Lambda integration"
  integration_method  = "POST"
  integration_uri     = aws_lambda_function.app.invoke_arn
}

# API Gateway Route for root path
# Handles requests to the root path (/)
resource "aws_apigatewayv2_route" "lambda_root" {
  api_id    = aws_apigatewayv2_api.lambda.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# API Gateway Route for proxy paths
# Handles all other paths (/{proxy+})
resource "aws_apigatewayv2_route" "lambda" {
  api_id    = aws_apigatewayv2_api.lambda.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# Lambda Permission for API Gateway
# Allows API Gateway to invoke the Lambda function
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}

# Lambda Permission for EventBridge
# Allows EventBridge to invoke the Lambda function
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ecr_push.arn
}

# IAM Role for Lambda
# Execution role for the Lambda function
resource "aws_iam_role" "lambda_role" {
  name = "${var.lambda_function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Role for Lambda Updates
# Role used by EventBridge to update the Lambda function
resource "aws_iam_role" "lambda_update_role" {
  name = "${var.lambda_function_name}-update-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda Updates
# Allows EventBridge to update the Lambda function code
resource "aws_iam_role_policy" "lambda_update_policy" {
  name = "${var.lambda_function_name}-update-policy"
  role = aws_iam_role.lambda_update_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:UpdateFunctionCode"
        ]
        Resource = aws_lambda_function.app.arn
      }
    ]
  })
}

# CloudWatch Logs Policy
# Allows Lambda to write logs to CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Output the API Gateway endpoint URL
output "api_endpoint" {
  value = "${aws_apigatewayv2_stage.lambda.invoke_url}/"
} 