# StockAnalyser

## 🎯 Objectif


## 📚 how it's work

1. **Récupère les prix** Diamonds (Google, Apple, Meta, Amazon, Microsoft, Nvidia, Tesla)
2. **Calcule les variations** par rapport à la veille
3. **Affiche un résumé** avec statistiques

### Installation
```bash
# 1. Installer yfinance
source venv/bin/activate

# 2. Lancer le programme
python main.py
```

### Exemple de sortie
```
============================================================
                      🚀 StockAnalyser                       
============================================================

⏰ Analyse du 10/08/2025 à 14:30

🔍 ANALYSE DU PORTEFEUILLE
/==================================/
  📡 Récupération de AAPL...
    ✅ AAPL: $150.25 (+2.1%)
  📡 Récupération de GOOGL...
    ✅ GOOGL: $125.80 (-1.3%)
  📡 Récupération de MSFT...
    ✅ MSFT: $335.40 (+0.8%)
  📡 Récupération de NVDA...
    ✅ NVDA: $425.10 (+3.2%)
/==================================/

========================= 📊 RÉSUMÉ =========================
Actions analysées: 4
En hausse: 3 📈
En baisse: 1 📉
Stables: 0 ➡️
Variation moyenne: +1.20%

🏆 Meilleure: NVDA (Nvidia) : +3.20%
📉 Pire: GOOGL (Google) : -1.30%
=============================================================
✅ Analyse Done !



