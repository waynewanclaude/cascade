class CandlestickChart:
    def __init__(self, data, on_click=None, title=None, width=None, height=None):
        self.type_name = "candlestick"
        self.title = title
        self.width = width
        self.height = height
        self.on_click_callback = on_click
        
        self.series = []
        self._normalize(data)

    def _normalize(self, data):
        normalized = []
        
        # Handle Pandas DataFrame inputs
        if type(data).__name__ == "DataFrame":
            try:
                normalized = data.to_dict(orient="records")
            except Exception:
                pass
        elif isinstance(data, list):
            normalized = data

        for record in normalized:
            if isinstance(record, dict):
                # Clean and parse price data coordinates
                candle = {
                    "time": str(record.get("time", "")),
                    "open": float(record.get("open", 0.0)),
                    "high": float(record.get("high", 0.0)),
                    "low": float(record.get("low", 0.0)),
                    "close": float(record.get("close", 0.0)),
                    "volume": float(record.get("volume", 0.0)),
                    "entry_target": float(record["entry_target"]) if "entry_target" in record and record["entry_target"] is not None else None,
                    "exit_target": float(record["exit_target"]) if "exit_target" in record and record["exit_target"] is not None else None
                }
                self.series.append(candle)

    def serialize(self):
        return {
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "series": self.series,
            "on_click": self.on_click_callback.__name__ if self.on_click_callback is not None else None
        }
