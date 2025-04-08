variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "$default"
}

variable "google_api_key" {
  description = "Google Api Key"
  type        = string
  default     = "$default"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "fastapi-lambda"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "fastapi-lambda"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for file storage"
  type        = string
  default     = "smart-file-search-bucket"
}

variable "frontend_bucket_name" {
  description = "Name of the S3 bucket for frontend static website hosting"
  type        = string
  default     = "smart-file-search-frontend"
}

variable "cloudfront_domain_name" {
  description = "Domain name for the CloudFront distribution"
  type        = string
  default     = ""
}

variable "use_custom_domain" {
  description = "Whether to use a custom domain for the CloudFront distribution"
  type        = bool
  default     = false
}

variable "domain_name" {
  description = "Custom domain name for the CloudFront distribution"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate for the custom domain"
  type        = string
  default     = ""
} 