from datetime import datetime

class Menu:

    def show_header(self):
        print("============================================================")
        print("                      🚀 StockAnalyser                       ")
        print("============================================================")
        print()
        print("🔍 PORTFOLIO (NAME) ANALYSE")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y [%H:%M]')}")
        print()

    def show_analysis_start(self):
        print("/================================/")

    def show_analysis_end(self):
        print("/================================/")
        print()

    def show_summary_start(self):
        print("======================== 📊 SUMMARY ========================")

    def show_summary_end(self):
        print("============================================================")
        print("✅ Analyse Done !")

    def show_no_data_error(self):
        print("❌ No data available for analysis")

    def show_summary(self, results):
        up_count = sum(1 for stock in results if stock['percentage_change'] > 0)
        down_count = sum(1 for stock in results if stock['percentage_change'] < 0)
        stable_count = sum(1 for stock in results if stock['percentage_change'] == 0)
        
        total_variation = sum(stock['percentage_change'] for stock in results)
        average_variation = total_variation / len(results)

        print(f"Number of Stocks: {len(results)}")
        print(f"Up: {up_count} 📈")
        print(f"Down: {down_count} 📉")
        print(f"Stable: {stable_count} ➡️")
        print(f"Average Variation: {average_variation:+.2f}%")

        if results:
            best_stock = max(results, key=lambda x: x['percentage_change'])
            worst_stock = min(results, key=lambda x: x['percentage_change'])
            print()
            print(f"🏆 Best: {best_stock['symbol']} ({best_stock['company_name']}) : {best_stock['percentage_change']:+.2f}%")
            print(f"📉 Worst: {worst_stock['symbol']} ({worst_stock['company_name']}) : {worst_stock['percentage_change']:+.2f}%")