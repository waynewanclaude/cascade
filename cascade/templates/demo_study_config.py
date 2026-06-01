from cascade import Cascade, Table, CandlestickChart, CustomPanel, format_currency, format_percent

# Initialize the audit dashboard
app = Cascade(
    title="Trading Audit Study",
    orientation="horizontal",
    persistence_path="browser"
)

# Mock backtest trades ledger data
MOCK_TRADES = [
    {"ID": "T-1001", "Time": "2026-05-15", "Ticker": "NVDA", "Side": "BUY", "Qty": 100, "Price": 920.50, "P&L": 4550.00, "Return": 0.049},
    {"ID": "T-1002", "Time": "2026-05-16", "Ticker": "AAPL", "Side": "SELL", "Qty": 150, "Price": 185.20, "P&L": -1250.00, "Return": -0.045},
    {"ID": "T-1003", "Time": "2026-05-17", "Ticker": "MSFT", "Side": "BUY", "Qty": 80, "Price": 420.10, "P&L": 3840.00, "Return": 0.114},
    {"ID": "T-1004", "Time": "2026-05-18", "Ticker": "TSLA", "Side": "BUY", "Qty": 200, "Price": 175.40, "P&L": -8200.00, "Return": -0.234},
    {"ID": "T-1005", "Time": "2026-05-19", "Ticker": "AMZN", "Side": "SELL", "Qty": 120, "Price": 180.90, "P&L": 1950.00, "Return": 0.090}
]

def generate_mock_candles(ticker, base_price):
    series = []
    seed = hash(ticker) % 100
    for i in range(20):
        offset = (i - 10) * (seed * 0.1)
        open_p = base_price + offset
        close_p = open_p + (seed * 0.05 * (-1 if i % 2 == 0 else 1))
        high_p = max(open_p, close_p) + (seed * 0.03)
        low_p = min(open_p, close_p) - (seed * 0.02)
        vol = 100000 + (i * 12345)
        
        series.append({
            "time": f"Day {i + 1}",
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": int(vol),
            "entry_target": round(base_price, 2) if i == 5 else None,
            "exit_target": round(close_p, 2) if i == 15 else None
        })
    return series

# --------------------------------------------------
# Level 0 (Trades Root Table)
# --------------------------------------------------
@app.root_panel()
def show_trades_list():
    formatted_data = []
    for t in MOCK_TRADES:
        row = {
            "Trade ID": t["ID"],
            "Execution Date": t["Time"],
            "Ticker": t["Ticker"],
            "Direction": t["Side"],
            "Volume Qty": t["Qty"],
            "Price USD": format_currency(t["Price"]),
            "P&L USD": format_currency(t["P&L"], sign=True),
            "Return %": format_percent(t["Return"], sign=True)
        }
        formatted_data.append(row)
        
    return Table(
        data=formatted_data,
        title="Active Backtest Trade Ledger",
        on_click=show_market_chart,
        width="450px"
    )

# --------------------------------------------------
# Level 1 (SVG Candle Chart)
# --------------------------------------------------
@app.panel("show_market_chart")
def show_market_chart(clicked_row):
    ticker = clicked_row.get("Ticker", "NVDA")
    
    # Strip currency formatting to parse base float
    price_str = clicked_row.get("Price USD", "$100.00").replace("$", "").replace(",", "")
    base_price = float(price_str)
    
    candle_data = generate_mock_candles(ticker, base_price)
    
    return CandlestickChart(
        data=candle_data,
        title=f"{ticker} Market Distribution Timeline",
        on_click=inspect_microstructure,
        width="560px",
        height=280
    )

# --------------------------------------------------
# Level 2 (Custom Live Spread Explorer)
# --------------------------------------------------
@app.panel("inspect_microstructure")
def inspect_microstructure(clicked_candle):
    time_stamp = clicked_candle.get("time", "Day 1")
    close_p = clicked_candle.get("close", 100.0)
    
    html_content = f"""
        <div class="custom-microstructure">
            <h4>Order Book Microstructure - {time_stamp}</h4>
            <div class="spread-metrics">
                <p>Last Closed: <strong class="value-close">${close_p}</strong></p>
                <p>Bid/Ask Spread: <strong id="live-spread">$0.02</strong></p>
            </div>
            
            <div class="order-book-halves">
                <div class="book-half bid-half">
                    <h5>Bids (Buy Orders)</h5>
                    <ul id="bids-list"></ul>
                </div>
                <div class="book-half ask-half">
                    <h5>Asks (Sell Orders)</h5>
                    <ul id="asks-list"></ul>
                </div>
            </div>
        </div>
    """
    
    css_style = """
        .custom-microstructure h4 {
            font-size: 13px;
            font-weight: 700;
            color: var(--accent-cyan);
            border-bottom: 1px solid var(--border-card);
            padding-bottom: 6px;
            margin-bottom: 10px;
        }
        .spread-metrics {
            display: flex;
            justify-content: space-between;
            background: rgba(0,0,0,0.2);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-family: var(--font-mono);
            margin-bottom: 12px;
        }
        .order-book-halves {
            display: flex;
            gap: 12px;
        }
        .book-half {
            flex: 1;
            background: rgba(255,255,255,0.01);
            border: 1px solid var(--border-card);
            border-radius: 6px;
            padding: 8px;
        }
        .book-half h5 {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-dim);
            margin-bottom: 6px;
        }
        .book-half ul {
            list-style: none;
            font-family: var(--font-mono);
            font-size: 10px;
        }
        .book-half li {
            display: flex;
            justify-content: space-between;
            padding: 3px 0;
            border-bottom: 1px solid rgba(255,255,255,0.02);
        }
        .bid-half li { color: var(--accent-green); }
        .ask-half li { color: var(--accent-red); }
    """
    
    js_script = """
        const bidsList = container.querySelector('#bids-list');
        const asksList = container.querySelector('#asks-list');
        const liveSpread = container.querySelector('#live-spread');
        
        function populateBook() {
            bidsList.innerHTML = '';
            asksList.innerHTML = '';
            
            const base = parseFloat(data.closePrice);
            const spread = 0.01 + (Math.random() * 0.05);
            liveSpread.textContent = '$' + spread.toFixed(3);
            
            // Build bids
            for(let i = 0; i < 5; i++) {
                const price = base - (spread / 2) - (i * 0.02);
                const size = Math.floor(100 + Math.random() * 900);
                const li = document.createElement('li');
                li.innerHTML = `<span>$${price.toFixed(3)}</span><strong>${size}</strong>`;
                bidsList.appendChild(li);
            }
            
            // Build asks
            for(let i = 0; i < 5; i++) {
                const price = base + (spread / 2) + (i * 0.02);
                const size = Math.floor(100 + Math.random() * 900);
                const li = document.createElement('li');
                li.innerHTML = `<span>$${price.toFixed(3)}</span><strong>${size}</strong>`;
                asksList.appendChild(li);
            }
        }
        
        populateBook();
        container.closest('.panel-body').dataset.intervalId = setInterval(populateBook, 1500);
    """
    
    return CustomPanel(
        html=html_content,
        css=css_style,
        js=js_script,
        data={"closePrice": close_p},
        title="L2 Custom Order Book Microstructure",
        width="480px"
    )
