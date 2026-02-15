"""
Quick test script to verify TrendOps setup.
Run this after installing dependencies to ensure everything works.
"""
import sys
import os
import warnings

# Suppress the noisy google-generativeai FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

def test_imports():
    """Test that all required packages can be imported."""
    print("\nTesting imports...")
    
    try:
        import fastapi
        print("[OK] FastAPI")
    except ImportError:
        print("[FAIL] FastAPI - run: pip install fastapi")
        return False
    
    try:
        import uvicorn
        print("[OK] Uvicorn")
    except ImportError:
        print("[FAIL] Uvicorn - run: pip install uvicorn")
        return False
    
    try:
        import httpx
        print("[OK] HTTPX")
    except ImportError:
        print("[FAIL] HTTPX - run: pip install httpx")
        return False
    
    try:
        import google.generativeai
        print("[OK] Google Generative AI")
    except ImportError:
        print("[FAIL] Google Generative AI - run: pip install google-generativeai")
        return False
    
    try:
        import numpy
        print("[OK] NumPy")
    except ImportError:
        print("[FAIL] NumPy - run: pip install numpy")
        return False
    
    return True

def test_env_vars():
    """Test that required environment variables are set."""
    print("\nTesting environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not youtube_key:
        print("[FAIL] YOUTUBE_API_KEY not set")
        print("  Set it in .env file or export YOUTUBE_API_KEY=your_key")
        return False
    else:
        print(f"[OK] YOUTUBE_API_KEY set ({youtube_key[:10]}...)")
    
    if not google_key:
        print("[FAIL] GOOGLE_API_KEY not set")
        print("  Set it in .env file or export GOOGLE_API_KEY=your_key")
        return False
    else:
        print(f"[OK] GOOGLE_API_KEY set ({google_key[:10]}...)")
    
    return True

def test_structure():
    """Test that project structure is correct."""
    print("\nTesting project structure...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/agents/data_agent.py",
        "app/agents/analytics_agent.py",
        "app/agents/intelligence_agent.py",
        "app/agents/governance_agent.py",
        "app/tools/youtube_tool.py",
        "app/tools/clustering_tool.py",
        "app/tools/scoring_tool.py",
        "app/utils/config.py",
        "app/utils/logging.py",
        "app/utils/cost_tracker.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[FAIL] {file_path} - MISSING")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("=" * 60)
    print("TrendOps Setup Verification")
    print("=" * 60)
    
    imports_ok = test_imports()
    structure_ok = test_structure()
    env_ok = test_env_vars()
    
    print("\n" + "=" * 60)
    if imports_ok and structure_ok and env_ok:
        print("[SUCCESS] ALL CHECKS PASSED")
        print("\nYou can now run:")
        print("  python -m app.main")
        print("\nOr with Docker:")
        print("  docker build -t trendops .")
        print("  docker run -p 8000:8000 --env-file .env trendops")
        sys.exit(0)
    else:
        print("[FAILED] SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running TrendOps.")
        sys.exit(1)
