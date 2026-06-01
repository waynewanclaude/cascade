import math
from cascade import Cascade, Table, StockChartsChart

# Initialize the StockCharts visual explorer dashboard
app = Cascade(
    title="StockCharts Analytics",
    orientation="horizontal",
    persistence_path="browser"
)

def generate_mock_stockcharts_series():
    series = []
    base_price = 100.0
    for i in range(20):
        # Establish dynamic pricing swings
        change = (i * 0.9) - ((i - 10) * (i - 10) * 0.15)
        open_p = base_price + change
        close_p = open_p + (2.5 * (-1 if i % 2 == 0 else 1))
        high_p = max(open_p, close_p) + 4.5
        low_p = min(open_p, close_p) - 3.2
        
        # Calculate mock moving average (cyan line)
        mv50_val = base_price + (i * 0.4)
        
        # Calculate custom buy/sell floating indicators (triangles)
        sig = None
        if i == 4 or i == 14:
            sig = "buy"
        elif i == 8 or i == 18:
            sig = "sell"
            
        # Calculate custom precise price event markers (magenta dots)
        evt_price = None
        if i == 6 or i == 16:
            evt_price = high_p + 1.5
            
        series.append({
            "time": f"Day {i + 1}",
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": int(120000 + (i * 8500)),
            
            # Additional Indicators & Markers columns
            "mv50": round(mv50_val, 2),
            "updw_ind": sig,
            "type1": round(evt_price, 2) if evt_price is not None else None,
            
            # Zero-Loss Pipeline: Unmapped column, invisible on SVG but passed downstream!
            "unmapped_secret": f"SEC-KEY-00{i+1}-AUDIT-PASS"
        })
    return series

# --------------------------------------------------
# Level 0 (StockCharts.com Custom Candlestick Explorer)
# --------------------------------------------------
@app.root_panel()
def show_stockcharts_chart():
    stock_data = generate_mock_stockcharts_series()
    
    # Declarative visual specs configuration mapping
    visual_instructions = {
        "*OHLC": "stockcharts;logY",  # Enables StockCharts hollow theme and logarithmic Y scale
        "mv50": "cyan line",          # Renders 50MA as a solid cyan line path
        "updw_ind": {
            "buy": "green triangle-up",   # Places green buy marker below low wick
            "sell": "red triangle-down"   # Places red sell marker above high wick
        },
        "type1": "magenta dot"        # Plots precise magenta circle at event price
    }
    
    return StockChartsChart(
        data=stock_data,
        title="StockCharts Advanced Layout",
        on_click=inspect_hidden_records,
        chart_config=visual_instructions,
        width="560px",
        height=280
    )

# --------------------------------------------------
# Level 1 (Downstream Auditor Table - Verifying Data Pipeline)
# --------------------------------------------------
@app.panel("inspect_hidden_records")
def inspect_hidden_records(clicked_candle):
    # Retrieve all clicked candle coordinates, standard and unmapped alike!
    data_list = []
    for key, val in clicked_candle.items():
        data_list.append({
            "Parameter Column": str(key),
            "Extracted Value": str(val) if val is not None else "-"
        })
        
    return Table(
        data=data_list,
        title=f"Record Details: {clicked_candle.get('time', 'Day 1')}",
        width="450px"
    )
