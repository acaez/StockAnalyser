#!/usr/bin/env python3

import sys
from pathlib import Path

project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from datetime import datetime
from PortfolioManager.analyser import analyzer
from MenuManager.show import Menu

def main():
    menu = Menu()
    menu.start()
    menu.analyse_start()
    results = analyzer()
    menu.analyse_end()
    if results:
        menu.resume_start()
        menu.summary(results)
        menu.resume_end()
    else:
        menu.error_no_data()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programme interrompu par l'utilisateur")
    except Exception as error:
        print(f"\n❌ Erreur inattendue: {error}")
        print("💡 Conseil: Vérifiez que yfinance est installé avec 'pip install yfinance'")
