def format_currency(val, sign=False):
    """Formats numeric values as USD currency. (e.g. $1,234.56, +$245.00, -$12.50)"""
    try:
        num = float(val)
        prefix = ""
        if sign and num > 0:
            prefix = "+"
            
        if num < 0:
            return f"-${abs(num):,.2f}"
        else:
            return f"{prefix}${num:,.2f}"
    except (ValueError, TypeError):
        return str(val)

def format_percent(val, sign=False):
    """Formats decimal values as percentages. (e.g. 12.4%, +5.8%, -23.1%)"""
    try:
        num = float(val)
        prefix = ""
        if sign and num > 0:
            prefix = "+"
        return f"{prefix}{num:.1%}"
    except (ValueError, TypeError):
        return str(val)

class Table:
    def __init__(self, data, columns=None, on_click=None, title=None, width=None, height=None):
        self.type_name = "table"
        self.title = title
        self.width = width
        self.height = height
        self.on_click_callback = on_click
        
        self.columns = []
        self.rows = []
        self._normalize(data, columns)

    def _normalize(self, data, columns):
        # 1. Handle Pandas DataFrame input (detect dynamically without introducing package dependency)
        if type(data).__name__ == "DataFrame":
            try:
                self.rows = data.to_dict(orient="records")
                self.columns = list(data.columns)
                return
            except Exception:
                pass

        # 2. Handle List of Dictionaries
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            self.rows = data
            if columns is not None:
                self.columns = columns
            else:
                self.columns = list(data[0].keys())

        # 3. Handle List of Lists / Tuples
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], (list, tuple)):
            if columns is None:
                # Generate fallback column labels
                col_count = len(data[0])
                self.columns = [f"Col {i + 1}" for i in range(col_count)]
            else:
                self.columns = columns

            # Convert row lists into dictionary records mapping to headers
            for row_list in data:
                row_dict = {}
                for idx, val in enumerate(row_list):
                    if idx < len(self.columns):
                        row_dict[self.columns[idx]] = val
                self.rows.append(row_dict)
        else:
            self.rows = []
            self.columns = columns if columns is not None else []

    def serialize(self):
        return {
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "columns": self.columns,
            "rows": self.rows,
            "on_click": self.on_click_callback.__name__ if self.on_click_callback is not None else None
        }
