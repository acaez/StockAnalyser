# 📊 StockAnalyser
A Python-based stock portfolio analyzer that tracks and analyzes major tech stocks in real-time.

## 🎯 Overview
StockAnalyser is a command-line tool that fetches current stock prices for a predefined portfolio, calculates daily variations, and provides comprehensive analysis with statistics and insights.

## 📚 how it's work

Real-time Data: Fetches live stock prices using Yahoo Finance API
Daily Analysis: Calculates price changes and percentage variations
Statistical Summary: Provides comprehensive portfolio statistics

### Installation
```bash
# 1. clone the repository
git clone https://github.com/yourusername/StockAnalyser.git
cd StockAnalyser

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Usage
```bash
python main.py
```

### Sample Output
```
============================================================
                      🚀 StockAnalyser                       
============================================================

🔍 PORTFOLIO ANALYSIS 
⏰ 11/08/2025 [05:06]

/================================/
  📡 Fetching data for GOOGL...
    ✅ GOOGL: $201.42 (+2.5%)
  📡 Fetching data for AAPL...
    ✅ AAPL: $229.35 (+4.2%)
  📡 Fetching data for META...
    ✅ META: $769.3 (+1.0%)
  📡 Fetching data for AMZN...
    ✅ AMZN: $222.69 (-0.2%)
  📡 Fetching data for MSFT...
    ✅ MSFT: $522.04 (+0.2%)
  📡 Fetching data for NVDA...
    ✅ NVDA: $182.7 (+1.1%)
  📡 Fetching data for TSLA...
    ✅ TSLA: $329.65 (+2.3%)
/================================/

======================== 📊 SUMMARY =========================
Number of Stocks: 7
Up: 6 📈
Down: 1 📉
Stable: 0 ➡️
Average Change: +1.59%

🏆 Best: AAPL (Apple) : +4.24%
📉 Worst: AMZN (Amazon) : -0.20%
============================================================
✅ Analysis Complete!
```

📊 Disclaimer
This tool is for educational and informational purposes only. 
It should not be considered as financial advice.

