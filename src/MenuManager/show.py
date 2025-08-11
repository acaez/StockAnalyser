from datetime import datetime

class Menu:
    
    def start(self):
        print("============================================================")
        print("                      🚀 StockAnalyser                       ")
        print("============================================================")
        print()
        print("🔍 PORTFOLIO (NAME) ANALYSE")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y [%H:%M]')}")
        print()
    
    def analyse_start(self):
        print("/================================/")
    
    def analyse_end(self):
        print("/================================/")
        print()
    
    def resume_start(self):
        print("======================== 📊 SUMMARY =========================")

    def resume_end(self):
        print("============================================================")
        print("✅ Analyse Done !")
    
    def error_no_data(self):
        print("❌ No data available for analysis")
    
    def summary(self, results):
        up_count = sum(1 for stock in results if stock['percentage_variation'] > 0)
        down_count = sum(1 for stock in results if stock['percentage_variation'] < 0)
        stable_count = sum(1 for stock in results if stock['percentage_variation'] == 0)
        
        total_variation = sum(stock['percentage_variation'] for stock in results)
        average_variation = total_variation / len(results)

        print(f"Number of Stocks: {len(results)}")
        print(f"Up: {up_count} 📈")
        print(f"Down: {down_count} 📉")
        print(f"Stable: {stable_count} ➡️")
        print(f"Average Variation: {average_variation:+.2f}%")

        if results:
            best_stock = max(results, key=lambda x: x['percentage_variation'])
            worst_stock = min(results, key=lambda x: x['percentage_variation'])
            print()
            print(f"🏆 Best: {best_stock['symbol']} ({best_stock['name']}) : {best_stock['percentage_variation']:+.2f}%")
            print(f"📉 Worst: {worst_stock['symbol']} ({worst_stock['name']}) : {worst_stock['percentage_variation']:+.2f}%")