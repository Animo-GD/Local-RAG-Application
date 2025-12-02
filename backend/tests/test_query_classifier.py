import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
import dspy
from core import SmartQueryClassifier
from config import settings
# Setup
lm = dspy.LM(model=f"ollama/{settings.LLM_MODEL}", api_base="http://localhost:11434",max_tokens=200)
dspy.configure(lm=lm)

classifier = SmartQueryClassifier()

available_tables = [
    "customers",
    "orders", 
    "products",
    "employees",
    "sales_records"
]

available_documents = [
    "Company_Handbook_2024.pdf",
    "Q3_Financial_Report.pdf",
    "Product_Specifications.pdf",
    "Employee_Benefits_Guide.pdf"
]

# Test queries
test_queries = [
    "How many customers are from London?",
    "What does the company handbook say about vacation policy?",
    "Hello, how are you doing today?",
    "Explain the quarterly sales performance",
    "Who is the CEO mentioned in the financial report?",
    "Count all orders placed last month",
    "Summarize the product specifications",
    "What's the weather like?",
]

print("=" * 80)
print("SMART QUERY CLASSIFICATION DEMO")
print("=" * 80)
print(f"\nAvailable Tables: {', '.join(available_tables)}")
print(f"Available Documents: {', '.join(available_documents)}\n")
print("=" * 80)

# Classify each query
for i, query in enumerate(test_queries, 1):
    print(f"\n[Query {i}] {query}")
    print("-" * 80)
    
    result = classifier(
        question=query,
        tables=available_tables,
        documents=available_documents
    )
    
    # Display results
    print(f"Classification: {result['query_type'].upper()}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Reasoning: {result['reasoning']}")
    
    # Show what action would be taken
    if result['query_type'] == 'sql':
        print("→ Action: Query the database")
    elif result['query_type'] == 'document':
        print("→ Action: Search documents using RAG")
    else:
        print("→ Action: Use general LLM knowledge")
    
    print("-" * 80)

print("\n" + "=" * 80)
print("DEMO COMPLETE")
print("=" * 80)