# Smart File Search

[![Try Smart File Search](https://img.shields.io/badge/👉👉%20Try%20Smart%20File%20Search%20-008000?style=for-the-badge&logo=amazonaws&logoColor=white)](https://d3k0iqvqbr31j.cloudfront.net/)


Hello, Community!

In this project, we're going to build an application that provides the best possible experience for uploading and searching for file content. To achieve this goal, we need to think about what it really means to provide an optimized upload experience.

### 🚀 Simplified Upload with Drag-and-Drop

The best upload experience is the one that requires the least effort from the user. That's why we chose to implement a drag-and-drop scheme, where you simply drag the file to the application for the upload to be successful.

However, it is essential to consider some important variables:

**File size:** The system must be able to handle small and large files without compromising performance.

**Number of files:** It must be possible to upload multiple files at once, in a practical and intuitive way.

### 📄 Accepted File Types

To provide a comprehensive experience, we would ideally accept any file type: documents, images, videos, and music. However, to keep our scope realistic and achievable within the timeframe available, we will focus solely on documents.

The formats we will accept include:

- [x] DOC, DOCX (Word)
- [x] XLS, XLSX (Excel)
- [x] TXT (Text)
- [x] PDF (General)

### 🔍 Optimized Search Experience

Imagine uploading your favorite book - say, "The Little Prince" - and being able to ask it questions naturally. For example:

 - **You ask:** "What did the fox teach about friendship?"
 - **The system** instantly finds and highlights the exact passage where the fox explains: "It's the time you spent on your rose that makes your rose so important... You become responsible forever for what you've tamed."

This magic happens through semantic search. Instead of just matching keywords, our system understands meaning. When you:

1. Upload files, we convert text into AI-powered "meaning vectors"
2. Ask a question, it finds conceptually related passages
3. Get precise answers with highlighted context

Search through your documents like you're asking a friend. Just type what you're looking for in plain language and get the exact answers you need - no more scrolling or skimming through pages.

### 🎥 Demo
[![Try Smart File Search](https://img.shields.io/badge/👉👉%20Try%20Smart%20File%20Search%20-008000?style=for-the-badge&logo=amazonaws&logoColor=white)](https://d3k0iqvqbr31j.cloudfront.net/)

[Smart-File-Search.webm](https://github.com/user-attachments/assets/6120fd4f-9d75-4368-92c5-bf42e9ac0095)

### 🏗️ Archtecture

```mermaid
graph TD
    %% User
    User[User] -->|Accesses website| CloudFront[CloudFront Distribution]
    
    %% Frontend
    CloudFront -->|Serves static assets| S3Frontend[S3 Bucket - Frontend]
    
    %% Backend
    User -->|Calls API| APIGateway[API Gateway HTTP API]
    APIGateway -->|Invokes function| Lambda[Lambda Function]
    
    %% Storage
    Lambda -->|Stores files| S3Backend[S3 Bucket - Backend]
    Lambda -->|Reads/Writes file data| DynamoDB[DynamoDB Table]
    
    %% Containerization
    ECR[ECR Repository] -->|Push container image| ECRPush[ECR Image Push]
    
    %% Monitoring
    Lambda -->|Sends logs| CloudWatch[CloudWatch Logs]
    APIGateway -->|Sends logs| CloudWatch
    
    %% Events / Deployment
    ECRPush -->|Triggers rule| EventBridge[EventBridge Rule]
    EventBridge -->|Deploys updated Lambda image| Lambda
    
    %% Styles
    classDef aws fill:#FF9900,stroke:#232F3E,color:white;
    classDef user fill:#4285F4,stroke:#0F9D58,color:white;
    
    class CloudFront,S3Frontend,APIGateway,Lambda,S3Backend,DynamoDB,ECR,CloudWatch,EventBridge aws;
    class User,ECRPush user;
    
    %% Titles
    subgraph "Frontend"
        CloudFront
        S3Frontend
    end
    
    subgraph "Backend"
        APIGateway
        Lambda
    end
    
    subgraph "Storage"
        S3Backend
        DynamoDB
    end
    
    subgraph "Containerization"
        ECR
        ECRPush
    end
    
    subgraph "Monitoring"
        CloudWatch
    end
    
    subgraph "Events & Deployment"
        EventBridge
    end
```


### 💡 Future Ideas

While our initial focus is on documents, we may expand this system in the future to process other file types. For example:

Videos: Identify and indicate in which specific passage a certain dialogue or word is spoken.

Music: Find the exact minute a word or phrase appears in the lyrics.

For now, we will keep the scope well defined to ensure efficient and high-quality development. We can't wait to see what we build together! 🚀

## 🚧 Backlog

[Access Open Issues (backlog)](https://github.com/feliperooke/smart-file-search/issues)

![GitHub issues](https://img.shields.io/github/issues/feliperooke/smart-file-search?label=Backlog)

## 🛠️ Setup Instructions

### Environment Configuration

Before running the application, you need to configure your AWS credentials in the terminal:

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

Replace `your_access_key_id` and `your_secret_access_key` with your actual AWS credentials.

### Deployment Commands

To deploy the backend infrastructure and application:

```bash
make backend-deploy-all
```

To deploy only the frontend:

```bash
make frontend-deploy-all
```

These commands will handle the infrastructure deployment, build the application, and deploy it to AWS.


