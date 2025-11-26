print("Testing imports...")

try:
    print("1. Testing config...")
    from config import app_config, llm_config, SCENARIO_TEMPLATES, DEPARTURE_CITIES, SEASONS
    print("   ✓ Config OK")
except Exception as e:
    print(f"   ✗ Config Error: {e}")

try:
    print("2. Testing agents...")
    from agents import AgentOrchestrator
    print("   ✓ Agents OK")
except Exception as e:
    print(f"   ✗ Agents Error: {e}")

try:
    print("3. Testing scenarios...")
    from scenarios import ScenarioPlanner
    print("   ✓ Scenarios OK")
except Exception as e:
    print(f"   ✗ Scenarios Error: {e}")

try:
    print("4. Testing utils...")
    from utils import format_currency, format_duration
    print("   ✓ Utils OK")
except Exception as e:
    print(f"   ✗ Utils Error: {e}")

try:
    print("5. Testing RAG...")
    from rag import RAGRetriever
    print("   ✓ RAG OK")
except Exception as e:
    print(f"   ✗ RAG Error: {e}")

print("\nAll tests complete!")