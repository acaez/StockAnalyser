"""
Gestion des menu pour StockAnalyseApp
"""

class MenuManager:

    def start_menu():


    def select_portfolio(modules):

        portfolios =
        {
            '1': ('PERSO', modules['PERSO']),
            '2': ('BIGPHARMA', modules['BIGPHARMA']),
            '3': ('SMALLPHARMA', modules['SMALLPHARMA'])
        }
        print("\n" + "=" * 80)
        print("📊 SÉLECTION DU PORTEFEUILLE")
        print("=" * 80)
        print("1. 🏠 PERSO (Portfolio personnel)")
        print("2. 💊 BIGPHARMA (Grandes pharmas)")
        print("3. 🧪 SMALLPHARMA (Petites pharmas)")
        print("=" * 80)
        
        while True:
            try:
                choice = input("\n👉 Choisissez votre portefeuille (1-3): ").strip()
                if choice in portfolios:
                    name, portfolio = portfolios[choice]
                    print(f"✅ Portefeuille sélectionné: {name} ({len(portfolio)} actions)")
                    return name, portfolio
                else:
                    print("❌ Choix invalide")
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir !")
                return None, None
            except Exception as e:
                print(f"❌ Erreur: {e}")
