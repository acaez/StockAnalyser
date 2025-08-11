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

🔍 PORTFOLIO (NAME) ANALYSE 
⏰ 11/08/2025 [05:06]

/==================================/
  📡 Récupération de GOOGL...
    ✅ GOOGL: $201.42 (+2.5%)
  📡 Récupération de AAPL...
    ✅ AAPL: $229.35 (+4.2%)
  📡 Récupération de META...
    ✅ META: $769.3 (+1.0%)
  📡 Récupération de AMZN...
    ✅ AMZN: $222.69 (-0.2%)
  📡 Récupération de MSFT...
    ✅ MSFT: $522.04 (+0.2%)
  📡 Récupération de NVDA...
    ✅ NVDA: $182.7 (+1.1%)
  📡 Récupération de TSLA...
    ✅ TSLA: $329.65 (+2.3%)
/==================================/

========================= 📊 RÉSUMÉ =========================
Number of Stocks: 7
Up: 6 📈
Down: 1 📉
Stable: 0 ➡️
Average Variation: +1.59%

🏆 Best: AAPL (Apple) : +4.24%
📉 Worst: AMZN (Amazon) : -0.20%
============================================================
✅ Analyse Done !

```



