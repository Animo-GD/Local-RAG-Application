import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import from backend
from services import SQLService

try:
    service = SQLService()
    service.initialize()

    # Generate SQL
    sql = service.generate_sql("show me all customers from London")
    print(f"Generated SQL: {sql}")

    # Execute and get results as dict
    results = service.execute_sql_as_dict(sql)
    for row in results:
        print(row)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()