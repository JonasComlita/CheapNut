try:
    from backend.main import app
    from backend.smart_pantry import update_benchmarks
    from backend.analysis_engine import AnalysisEngine
    from backend.models import BenchmarkItem
    print("Imports successful")
except Exception as e:
    print(f"Import failed: {e}")
