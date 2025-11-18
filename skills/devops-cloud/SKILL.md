---
name: devops-cloud
description: Master DevOps practices, CI/CD pipelines, containerization with Docker, Kubernetes orchestration, AWS cloud services, Terraform IaC, and infrastructure monitoring for production systems.
---

# DevOps & Cloud Skill

Master DevOps, CI/CD, containerization, Kubernetes, AWS, Terraform, and infrastructure management.

## Quick Start

### Docker Containerization (50 hours)
```dockerfile
# Multi-stage Dockerfile for Node.js
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD node healthcheck.js
CMD ["node", "server.js"]
```

### Docker Compose Orchestration
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://db:5432/app
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secure
      - POSTGRES_DB=app
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
```

### Kubernetes Fundamentals (60 hours)
```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 10

---
# Service to expose deployment
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

### Terraform Infrastructure as Code (50 hours)
```hcl
# AWS provider configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# EC2 instance
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  tags = {
    Name = "${var.environment}-web-server"
  }
}

# RDS database
resource "aws_db_instance" "main" {
  identifier     = "${var.environment}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_encrypted = true

  db_name  = "maindb"
  username = "admin"
  password = random_password.db_password.result

  backup_retention_period = 30
  multi_az               = var.environment == "production"
}

# Variables
variable "aws_region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "environment" {
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# Outputs
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: Deploy Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test
      env:
        DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test_db

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .

    - name: Push to ECR
      run: |
        aws ecr get-login-password --region ${{ secrets.AWS_REGION }} | \
        docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
        docker tag myapp:${{ github.sha }} ${{ secrets.ECR_REGISTRY }}/myapp:latest
        docker push ${{ secrets.ECR_REGISTRY }}/myapp:latest

    - name: Deploy to Kubernetes
      run: |
        aws eks update-kubeconfig --name prod-cluster
        kubectl set image deployment/web-app web=${{ secrets.ECR_REGISTRY }}/myapp:latest
```

## AWS Core Services

### EC2 & VPC
```hcl
# VPC with subnets
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"
}

# Security group
resource "aws_security_group" "web" {
  name = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Monitoring & Observability

### Prometheus & Grafana
```yaml
# Prometheus configuration
global:
  scrape_interval: 15s

scrape_configs:
- job_name: 'app'
  static_configs:
  - targets: ['localhost:3000']

- job_name: 'kubernetes'
  kubernetes_sd_configs:
  - role: node
```

### Application Logging
```typescript
// Winston logging in Node.js
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

logger.info('Application started');
logger.error('Database connection failed', { error: err });
```

## Best Practices

- [ ] Use Infrastructure as Code
- [ ] Version control everything
- [ ] Automate testing
- [ ] Implement proper CI/CD
- [ ] Use container registries
- [ ] Secure secrets management
- [ ] Monitor all systems
- [ ] Plan disaster recovery
- [ ] Document architecture
- [ ] Regular backup testing

## Tools & Services

- **Containerization**: Docker, Podman
- **Orchestration**: Kubernetes, Docker Swarm
- **Cloud**: AWS, Google Cloud, Azure
- **IaC**: Terraform, CloudFormation, Pulumi
- **Monitoring**: Prometheus, Grafana, DataDog
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins

## When to Invoke This Skill

Invoke when:
- Creating CI/CD pipelines
- Containerizing applications
- Deploying to cloud
- Writing infrastructure code
- Setting up monitoring
- Database replication
- Disaster recovery
- Cost optimization
