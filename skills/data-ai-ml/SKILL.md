---
name: data-ai-ml
description: Master data science, machine learning, and AI engineering. Learn data analysis, ML model development, deep learning, LLMs, RAG systems, and production ML deployment with MLOps.
---

# Data, AI & Machine Learning Skill

Master data science, machine learning, and AI engineering across all specialization tracks.

## Quick Start

### Python Data Science Stack (60 hours)
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Data loading and exploration
df = pd.read_csv('data.csv')
print(df.describe())
print(df.isnull().sum())

# Data preprocessing
df['age'] = df['age'].fillna(df['age'].median())
df['category'] = pd.Categorical(df['category']).codes

# Train-test split
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))
```

### Deep Learning with PyTorch (100 hours)
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Neural network architecture
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Training loop
model = SimpleNN(input_size=784, hidden_size=128, output_size=10)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    total_loss = 0
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch}, Loss: {total_loss/len(train_loader)}")
```

### LLM Integration with LangChain (60 hours)
```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Simple LLM chain
llm = OpenAI(temperature=0.7, api_key="your-key")
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short poem about {topic}"
)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(topic="machine learning")

# RAG implementation
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# RAG chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
answer = qa.run("What is machine learning?")
```

### AI Agents with LangGraph (60 hours)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing_extensions import TypedDict

# Define agent state
class AgentState(TypedDict):
    messages: list
    thought: str
    action: str
    result: str

# Define tools
tools = {
    "search": lambda query: f"Search results for {query}",
    "calculate": lambda expr: eval(expr)
}

# Define agent nodes
def thought_node(state):
    """Think about the task"""
    return {"thought": "Processing..."}

def action_node(state):
    """Choose and execute action"""
    action = "search"
    result = tools[action]("query")
    return {"action": action, "result": result}

def reflection_node(state):
    """Reflect on results"""
    return {"messages": state["messages"] + [state["result"]]}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("thought", thought_node)
graph.add_node("action", action_node)
graph.add_node("reflection", reflection_node)

graph.add_edge(START, "thought")
graph.add_edge("thought", "action")
graph.add_edge("action", "reflection")
graph.add_edge("reflection", END)

agent = graph.compile()
result = agent.invoke({"messages": ["Hello"], "thought": "", "action": "", "result": ""})
```

## ML Workflows

### ETL Pipeline
```python
# Extract
raw_data = pd.read_csv('raw_data.csv')

# Transform
df = raw_data.copy()
df = df.dropna()
df['age'] = df['age'].astype(int)
df['income'] = df['income'].str.replace('$', '').astype(float)

# Load
df.to_csv('processed_data.csv', index=False)
db.insert_data(df)
```

### Model Training Pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100))
])

# Train
pipeline.fit(X_train, y_train)

# Save
import joblib
joblib.dump(pipeline, 'model.pkl')

# Load and predict
loaded_pipeline = joblib.load('model.pkl')
predictions = loaded_pipeline.predict(X_test)
```

## Model Evaluation

### Classification Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_auc_score
)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
auc = roc_auc_score(y_test, y_pred_proba)

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-Score: {f1:.3f}")
```

## Prompt Engineering

### Prompt Patterns
```python
# System prompt for role definition
system_prompt = """You are an expert Python developer.
Provide clear, well-documented code examples."""

# Few-shot learning
few_shot_prompt = """
Example 1:
Input: Calculate 2 + 2
Output: 4

Example 2:
Input: Calculate 10 * 5
Output: 50

Now solve:
Input: Calculate 7 + 3
"""

# Chain-of-thought prompting
cot_prompt = """
Solve step by step:
1. First, understand the problem
2. Break it into smaller parts
3. Solve each part
4. Combine the results

Problem: If a train travels 60mph for 2 hours, how far did it go?
"""
```

## MLOps & Deployment

### Model Versioning with MLflow
```python
import mlflow
import mlflow.sklearn

# Log model
mlflow.start_run()
mlflow.log_param("n_estimators", 100)
mlflow.log_metric("accuracy", accuracy)
mlflow.sklearn.log_model(model, "model")
mlflow.end_run()

# Load and predict
loaded_model = mlflow.sklearn.load_model("runs:/model")
predictions = loaded_model.predict(X_test)
```

### Model Serving
```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [data['age'], data['income']]
    prediction = model.predict([features])[0]
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run()
```

## Best Practices

- [ ] Versioning for data and models
- [ ] Reproducible experiments
- [ ] Proper train/test splits
- [ ] Cross-validation
- [ ] Feature importance analysis
- [ ] Monitor model drift
- [ ] A/B testing in production
- [ ] Ethical AI considerations
- [ ] Model documentation
- [ ] Regular retraining

## Tools & Frameworks

- **Data**: Pandas, NumPy, Polars
- **ML**: scikit-learn, XGBoost, LightGBM
- **Deep Learning**: PyTorch, TensorFlow
- **LLMs**: OpenAI, Anthropic, Hugging Face
- **MLOps**: MLflow, Weights & Biases, DVC

## When to Invoke This Skill

Invoke when:
- Analyzing datasets
- Building ML models
- Deep learning projects
- Working with LLMs
- Building RAG systems
- AI agent development
- Model evaluation
- Production deployment
