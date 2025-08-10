def show_summary(results):
    
    up_count = 0
    down_count = 0
    stable_count = 0
    
    for stock in results:
        if stock['percentage_variation'] > 0:
            up_count += 1
        elif stock['percentage_variation'] < 0:
            down_count += 1
        else:
            stable_count += 1
    
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