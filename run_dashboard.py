import streamlit.cli as stcli
import sys
from pathlib import Path

if __name__ == "__main__":
    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "app.py"
    sys.argv = ["streamlit", "run", str(dashboard_path)]
    sys.exit(stcli.main()) 