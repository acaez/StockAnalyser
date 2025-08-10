#!/usr/bin/env python3
"""
StockAnalyser - Main Application

This program does 3 things:
1. Fetches DIAMOND stock prices
2. Calculates variations
3. Displays a summary
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from PortfolioManager.analyse import portfolio_analyzer
from MenuManager.basic import show_summary

def main():
    print("============================================================")
    print("                      🚀 StockAnalyser                       ")
    print("============================================================")
    print(f"⏰ Analyse du {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    print()
    print("🔍 ANALYSE PORTFOLIO")
    print()
    print("/==================================/")
    results = portfolio_analyzer()
    print("/==================================/")
    print()
    if results:
        print("========================= 📊 RÉSUMÉ =========================")
        show_summary(results)
        print("=" * 61)
        print("✅ Analyse Done !")
    else:
        print("❌ No data available for analysis")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu par l'utilisateur")
    except Exception as error:
        print(f"\n❌ Erreur inattendue: {error}")
        print("💡 Conseil: Vérifiez que yfinance est installé avec 'pip install yfinance'")