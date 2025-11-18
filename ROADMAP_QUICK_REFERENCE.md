# Developer Roadmap Plugin - Quick Reference Guide

## One-Page Roadmap Overview

### Skill Progression Summary

| Role | Foundation | Intermediate | Advanced | Expert | Entry Salary |
|------|-----------|--------------|----------|--------|--------------|
| Data Analyst | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $55-75K |
| Data Engineer | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $85-110K |
| ML Engineer | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $100-130K |
| AI Engineer | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $110-140K |
| Data Scientist | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $100-130K |
| MLOps Engineer | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $95-125K |
| Prompt Engineer | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $70-90K |
| AI Agents | 0-3 mo | 3-6 mo | 6-12 mo | 12+ mo | $110-140K |

---

## Essential Tools by Category

### Foundation Tools (All Roles)
- **Languages**: Python, SQL
- **Version Control**: Git, GitHub
- **Development**: Jupyter Notebooks, VS Code
- **Documentation**: Markdown, Confluence

### Data Stack
```
Data Collection → Processing → Storage → Analysis → Visualization

SQL ← PostgreSQL/MySQL/Snowflake
Python ← Pandas, NumPy
Visualization ← Power BI, Tableau
```

### ML/AI Stack
```
Data → Feature Engineering → Model → Evaluation → Deployment

Python + PyTorch/TensorFlow
Scikit-learn ← XGBoost, LightGBM
Experiment Tracking ← MLflow, W&B
```

### Production Stack
```
Code → Test → Build → Deploy → Monitor → Alert

GitHub/GitLab → GitHub Actions/Jenkins
Docker → Kubernetes
Prometheus/Grafana ← Monitoring
```

---

## Quick Skill Checklist by Role

### Data Analyst Essentials
- [ ] SQL: SELECT, JOIN, GROUP BY, subqueries
- [ ] Excel: Pivot tables, VLOOKUP, formulas
- [ ] Python: Pandas, NumPy basics
- [ ] Visualization: Power BI OR Tableau
- [ ] Statistics: Mean, median, standard deviation, hypothesis testing
- [ ] Database: Basic understanding of relational databases

### Data Engineer Essentials
- [ ] Python: Advanced programming, object-oriented
- [ ] SQL: Complex queries, optimization, indexing
- [ ] Apache Spark: RDDs, DataFrames, SQL
- [ ] Kafka: Message streaming basics
- [ ] Airflow: Workflow orchestration
- [ ] Docker & Kubernetes: Containerization and orchestration
- [ ] Cloud: AWS/GCP/Azure services

### ML Engineer Essentials
- [ ] Python: Advanced programming
- [ ] Statistics: Probability, distributions, hypothesis testing
- [ ] Linear Algebra: Matrices, eigenvalues
- [ ] Scikit-learn: Classification, regression, clustering
- [ ] PyTorch OR TensorFlow: Neural networks, deep learning
- [ ] Model Evaluation: Cross-validation, metrics, ROC curves
- [ ] Feature Engineering: Selection, scaling, interaction

### AI Engineer Essentials
- [ ] Python: Application development
- [ ] LLM Basics: GPT, Claude, Gemini understanding
- [ ] Prompt Engineering: Techniques and optimization
- [ ] API Integration: REST, webhook handling
- [ ] LangChain: Tool integration, chains, agents
- [ ] Vector Databases: Embeddings, semantic search
- [ ] RAG Systems: Retrieval augmented generation

### Data Scientist Essentials
- [ ] Python & R: Statistical programming
- [ ] SQL: Data retrieval and manipulation
- [ ] Statistics: Hypothesis testing, distributions, inference
- [ ] Scikit-learn: ML algorithms
- [ ] Visualization: Matplotlib, Seaborn, Plotly
- [ ] Experimentation: A/B testing, experimental design
- [ ] Communication: Storytelling with data

### MLOps Engineer Essentials
- [ ] Python: ML systems programming
- [ ] Docker: Containerization and image building
- [ ] Kubernetes: Orchestration and deployment
- [ ] CI/CD: GitHub Actions, Jenkins, GitLab CI
- [ ] Model Serving: FastAPI, model registry
- [ ] Monitoring: Prometheus, Grafana, model drift detection
- [ ] Infrastructure as Code: Terraform, CloudFormation

### Prompt Engineer Essentials
- [ ] Prompt Techniques: Zero-shot, few-shot, chain-of-thought
- [ ] LLM APIs: OpenAI, Anthropic, Google usage
- [ ] Prompt Optimization: Testing and iteration
- [ ] Context Management: Token usage and relevance
- [ ] Output Parsing: Structured extraction
- [ ] RAG Basics: Retrieval integration
- [ ] Evaluation: Quality assessment and metrics

### AI Agents Essentials
- [ ] Python: Application development
- [ ] Agent Concepts: ReAct, AutoGPT patterns
- [ ] LangChain/LangGraph: Agent frameworks
- [ ] Tool Design: API specification and integration
- [ ] Multi-step Reasoning: Planning and execution
- [ ] Memory Management: Context and conversation history
- [ ] Error Handling: Graceful failures and recovery

---

## Technology Stack by Experience Level

### Junior Level (0-6 months)
**Data Analyst**
- SQL, Excel, Python basics
- One BI tool (Power BI OR Tableau)
- PostgreSQL

**Data Engineer**
- Python, SQL, Git
- Docker basics
- One cloud platform

**ML Engineer**
- Python, statistics, linear algebra
- Scikit-learn, Pandas
- Basic ML algorithms

**AI Engineer**
- Python fundamentals
- One LLM API (OpenAI/Anthropic)
- Basic prompting

### Intermediate Level (6-12 months)
**Data Analyst**
- SQL optimization, Python proficiency
- Advanced Excel
- BI tool mastery, Google Sheets
- Statistics and A/B testing

**Data Engineer**
- Python advanced, SQL expert
- Docker, basic Kubernetes
- Spark basics, Airflow
- Cloud platform mastery

**ML Engineer**
- Python expert, strong statistics
- PyTorch OR TensorFlow
- Feature engineering, experimentation
- Model evaluation and validation

**AI Engineer**
- Python application development
- Multiple LLM APIs
- LangChain basics, RAG systems
- Vector databases

### Senior Level (12+ months)
**Data Analyst**
- Complex SQL optimization
- Python expert
- Multiple BI tools
- Advanced statistics
- SQL stored procedures

**Data Engineer**
- Spark expert, Kafka streaming
- Kubernetes, infrastructure design
- Data lake/warehouse architecture
- Cost optimization
- Multiple cloud platforms

**ML Engineer**
- Advanced neural networks
- NLP/Computer Vision
- Model deployment
- Distributed training
- Advanced deep learning

**AI Engineer**
- Multi-agent systems
- Advanced RAG architectures
- Production AI systems
- Cost optimization
- Domain-specific models

---

## Common Implementation Patterns

### ETL Pattern (Data Engineering)
```
Source System
    ↓
Extract (API/SQL/Files)
    ↓
Transform (Clean, Validate, Aggregate)
    ↓
Load (Database/Data Lake)
    ↓
Analytics/Reporting
```

### ML Model Lifecycle (ML Engineering)
```
Problem Definition
    ↓
Data Collection & Exploration
    ↓
Feature Engineering
    ↓
Model Selection
    ↓
Training & Tuning
    ↓
Evaluation
    ↓
Deployment
    ↓
Monitoring & Retraining
```

### AI Agent Pattern (AI Engineers)
```
User Request
    ↓
Task Understanding
    ↓
Tool Selection
    ↓
Execution
    ↓
Observation & Feedback
    ↓
Loop Until Complete
    ↓
Response Delivery
```

### CI/CD Pipeline (MLOps)
```
Code Commit
    ↓
Automated Testing
    ↓
Model Training
    ↓
Model Evaluation
    ↓
Registry Update
    ↓
Staging Deployment
    ↓
Production Deployment
    ↓
Monitoring & Alerts
```

---

## Best Practices Summary

### Code Quality
1. Version control everything (Git)
2. Write tests (unit, integration, e2e)
3. Document your code (docstrings, README)
4. Code review before merge
5. Automate repetitive tasks

### Data Quality
1. Validate at every stage
2. Version data and models
3. Track data lineage
4. Monitor for drift
5. Implement audit trails

### Production Standards
1. Comprehensive monitoring
2. Detailed logging
3. Disaster recovery plans
4. Security best practices
5. Cost optimization

### Team Practices
1. Clear documentation
2. Regular knowledge sharing
3. Mentorship programs
4. Feedback loops
5. Incident retrospectives

---

## Learning Path Decision Tree

```
Choose Your Path:

1. Like Data & Insights?
   ├─ Visual Focus → Data Analyst
   ├─ Infrastructure Focus → Data Engineer
   └─ Statistics Focus → Data Scientist

2. Like ML & Models?
   ├─ Traditional ML → ML Engineer
   ├─ LLMs & APIs → AI Engineer
   ├─ Production Systems → MLOps
   └─ Agent Systems → AI Agents

3. Like Prompts & Optimization?
   └─ Prompt Engineer

```

---

## Transition Paths

### From Data Analyst
- → Data Engineer (add infrastructure knowledge)
- → Data Scientist (add ML knowledge)
- → Analytics Manager (add management skills)
- → AI Engineer (add LLM knowledge)

### From Data Engineer
- → MLOps Engineer (add ML knowledge)
- → Platform Engineer (specialize in infrastructure)
- → Data Architect (design systems)

### From ML Engineer
- → AI Engineer (add LLM knowledge)
- → ML Architect (design systems)
- → MLOps (focus on production)

### From AI Engineer
- → ML Engineer (add traditional ML)
- → AI Architect (design systems)
- → AI Products (add product sense)

---

## Interview Preparation Checklist

### Data Analyst
- [ ] SQL optimization techniques
- [ ] Statistical hypothesis testing
- [ ] Dashboard design principles
- [ ] Real-world business problems
- [ ] Tool expertise (Power BI/Tableau)

### Data Engineer
- [ ] System design (data pipelines)
- [ ] Spark/Hadoop concepts
- [ ] Database design
- [ ] Scalability and performance
- [ ] Cloud platform knowledge

### ML Engineer
- [ ] Model selection criteria
- [ ] Feature engineering techniques
- [ ] Evaluation metrics
- [ ] Overfitting prevention
- [ ] Production deployment

### AI Engineer
- [ ] Prompt engineering techniques
- [ ] LLM capabilities and limitations
- [ ] RAG system design
- [ ] Cost optimization
- [ ] Integration patterns

---

## Resource Links

### Primary Sources
- GitHub Repository: https://github.com/kamranahmedse/developer-roadmap
- Roadmap Site: https://roadmap.sh/

### Learning Platforms
- DataCamp: https://www.datacamp.com/
- Coursera: https://www.coursera.org/
- Fast.ai: https://www.fast.ai/
- Hugging Face: https://huggingface.co/

### Documentation
- Python: https://python.org/
- SQL: https://www.w3schools.com/sql/
- Apache Spark: https://spark.apache.org/
- PyTorch: https://pytorch.org/
- TensorFlow: https://tensorflow.org/
- LangChain: https://python.langchain.com/

---

## Key Metrics & KPIs

### Data Analyst
- Analysis accuracy
- Report delivery time
- Insight impact
- Dashboard usage

### Data Engineer
- Pipeline uptime
- Data processing latency
- Data quality score
- Cost per GB processed

### ML Engineer
- Model accuracy
- Training time
- Inference latency
- Model drift rate

### AI Engineer
- API response time
- Cost per request
- User satisfaction
- Output quality

### MLOps Engineer
- Deployment frequency
- Model drift detection
- Monitoring coverage
- Incident resolution time

---

**Version**: 1.0
**Last Updated**: November 2025
**Source**: Developer Roadmap Analysis Plugin

