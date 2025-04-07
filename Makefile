# Check if .env file exists
ifneq (,$(wildcard backend/.env))
    include backend/.env
    export
endif

# Variables with fallbacks
AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
AWS_REGION ?= us-east-1
ECR_REPOSITORY ?= fastapi-lambda
LAMBDA_FUNCTION ?= fastapi-lambda
IMAGE_TAG ?= latest

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

TERRAFORM_ENV_VARS := \
	TF_VAR_aws_region=$(AWS_REGION) \
	TF_VAR_s3_bucket_name=$(S3_BUCKET_NAME) \
	TF_VAR_ecr_repository_name=$(ECR_REPOSITORY) \
	TF_VAR_lambda_function_name=$(LAMBDA_NAME)


# Commands
.PHONY: ecr-login build push deploy test clean terraform-init terraform-plan terraform-apply terraform-destroy check-env create-infrastructure generate-lock

# Check environment variables
check-env:
	@echo "$(YELLOW)🔍 Checking environment variables...$(NC)"
	@if [ -z "$(AWS_REGION)" ]; then \
		echo "$(YELLOW)⚠️  AWS_REGION not set$(NC)"; \
		exit 1; \
	fi
	@if [ -z "$(S3_BUCKET_NAME)" ]; then \
		echo "$(YELLOW)⚠️  S3_BUCKET_NAME not set$(NC)"; \
		exit 1; \
	fi
	@if [ -z "$(LAMBDA_NAME)" ]; then \
		echo "$(YELLOW)⚠️  LAMBDA_NAME not set$(NC)"; \
		exit 1; \
	fi
	@if [ -z "$(ECR_REPOSITORY)" ]; then \
		echo "$(YELLOW)⚠️  ECR_REPOSITORY not set$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ All required environment variables are set$(NC)"

# Generate poetry.lock file
generate-lock:
	@echo "🔒 Generating poetry.lock file..."
	cd backend && poetry env use python3.12
	cd backend && poetry lock
	@echo "$(GREEN)✅ poetry.lock generated successfully$(NC)"

# Create infrastructure with Terraform
create-infrastructure: check-env terraform-init terraform-apply
	@echo "$(GREEN)✅ Infrastructure created successfully$(NC)"

# Login to ECR
ecr-login: check-env
	@echo "🔑 Logging in to Amazon ECR..."
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	@echo "$(GREEN)✅ Successfully logged in to ECR$(NC)"

# Build Docker image
build: generate-lock ecr-login
	@echo "🔨 Building Docker image $(ECR_REPOSITORY):$(IMAGE_TAG)..."
	cd backend && docker build -t $(ECR_REPOSITORY):$(IMAGE_TAG) .
	@echo "$(GREEN)✅ Docker image built successfully$(NC)"

# Push image to ECR
push: build
	@echo "🏷️  Tagging Docker image for ECR..."
	docker tag $(ECR_REPOSITORY):$(IMAGE_TAG) $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG)
	@echo "⬆️  Pushing image to ECR..."
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPOSITORY):$(IMAGE_TAG)
	@echo "$(GREEN)✅ Image successfully pushed to ECR$(NC)"

# Initialize Terraform
terraform-init: check-env 
	@echo "🚀 Initializing Terraform..."
	cd terraform && $(TERRAFORM_ENV_VARS) terraform init
	@echo "$(GREEN)✅ Terraform initialized successfully$(NC)"

# Plan Terraform changes
terraform-plan: check-env 
	@echo "📋 Planning Terraform changes..."
	cd terraform && $(TERRAFORM_ENV_VARS) terraform plan
	@echo "$(GREEN)✅ Terraform plan completed$(NC)"

# Apply Terraform changes for ECR repository only
terraform-apply-ecr: check-env terraform-init
	@echo "🏗️  Applying Terraform changes for ECR repository..."
	cd terraform && $(TERRAFORM_ENV_VARS) terraform apply -auto-approve -target=aws_ecr_repository.app
	@echo "$(GREEN)✅ ECR repository created successfully$(NC)"

# Apply remaining Terraform changes
terraform-apply-remaining: check-env 
	@echo "🏗️  Applying remaining Terraform changes..."
	cd terraform && $(TERRAFORM_ENV_VARS) terraform apply -auto-approve
	@echo "$(GREEN)✅ Remaining infrastructure created successfully$(NC)"

# Deploy the application
deploy: create-infrastructure push
	@echo "🚀 Deployment completed successfully"

# Test the API endpoint
test: check-env
	@echo "🧪 Testing API endpoint..."
	@curl -s https://$(shell cd terraform && terraform output -raw api_endpoint) | jq .
	@echo "$(GREEN)✅ API test completed$(NC)"

# Clean up local resources
clean:
	@echo "🧹 Cleaning up local resources..."
	docker rmi $(ECR_REPOSITORY):$(IMAGE_TAG) || true
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

# Complete deployment pipeline
all: check-env terraform-apply-ecr push terraform-apply-remaining test
	@echo "$(GREEN)✨ All tasks completed successfully$(NC)" 