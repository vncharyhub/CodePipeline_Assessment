# Multi-Cloud AI Service Pipeline

## Overview

This project demonstrates a **CI/CD pipeline** using AWS CloudFormation and CodePipeline to deploy a serverless application that interacts with multiple AI models (Amazon Bedrock and Azure OpenAI).

### Architecture

![Architecture Diagram](architecture-diagram.png)  
*Diagram shows CodePipeline triggered by GitHub commits, building and deploying CloudFormation stack which provisions Lambda + API Gateway + Secrets Manager.*

### Components

- **CodePipeline**: Automatically triggered on commits to GitHub main branch
- **CodeBuild**: Runs linting on Lambda Python code
- **CloudFormation**: Deploys all AWS infrastructure:
  - Lambda function (Python)
  - API Gateway HTTP API (public endpoint)
  - Secrets Manager (stores dummy API keys)
  - IAM Roles with least privilege
- **Lambda Function**: 
  - Accepts POST JSON with `prompt` and `target_model`
  - Calls Amazon Bedrock API or Azure OpenAI API placeholder
  - Retrieves secrets securely from Secrets Manager

---

## Deployment Instructions

### Prerequisites

- AWS CLI configured with appropriate permissions
- GitHub personal access token with repo access
- AWS account with IAM permissions to create CodePipeline, Lambda, API Gateway, Secrets Manager

### Steps

1. Clone this repository:

```bash
git clone https://github.com/vncharyhub/CodePipeline_Assessment.git
cd CodePipeline_Assessment
