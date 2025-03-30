# Smart File Search (Backend)

This is the backend of the Smart File Search project, built with FastAPI and managed using Poetry.

## 📋 Requirements

### Local Development
- Python 3.11
- Poetry (Python package manager)

### AWS Deployment
- AWS CLI configured with appropriate credentials
- Terraform installed

---

## 🛠️ Local Development Setup

### 1. Install Poetry
Follow instructions: https://python-poetry.org/docs/#installation

Or use:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Setup the project
```bash
cd backend
poetry env activate
```

### 3. Run the development server
```bash
poetry run uvicorn app.main:app --reload
```

## ☁️ AWS Deployment Setup

### 1. Build the package
```bash
# Install dependencies
poetry install

# Build the package
poetry build-lambda
```

### 2. Deploy to AWS Lambda
```bash
# Navigate to Terraform directory
cd .aws/terraform

# Initialize Terraform
terraform init

# Review the changes
terraform plan

# Apply the changes
terraform apply
```

After successful deployment, Terraform will output the API Gateway URL where your service is available.

### 3. Clean up (Optional)
To remove the deployed resources:
```bash
terraform destroy
```

## 📝 Deployment Notes
- Make sure you have AWS credentials configured properly
- The deployment uses AWS Lambda with Python 3.11 runtime
- API Gateway is configured with HTTP API type
- CloudWatch logging is enabled for both Lambda and API Gateway