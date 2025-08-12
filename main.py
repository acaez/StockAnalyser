#!/usr/bin/env python3
"""
StockAnalyser - A Python-based stock portfolio analyzer.

This is the main entry point for the StockAnalyser application that provides
real-time stock analysis for a predefined portfolio of stocks.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from portfolio_manager.analyser import analyze_portfolio
from menu_manager.display import Menu

def main() -> None:

    menu = Menu()
    menu.show_header()
    menu.show_analysis_start()
    results = analyze_portfolio()
    menu.show_analysis_end()
    if results:
        menu.show_summary_start()
        menu.show_summary(results)
        menu.show_summary_end()
    else:
        menu.show_no_data_error()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user")
        sys.exit(0)
    except Exception as error:
        print(f"\n❌ Unexpected error: {error}")
        print("💡 Tip: Check that yfinance is installed with 'pip install yfinance'")
        sys.exit(1)
