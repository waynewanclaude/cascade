class CustomPanel:
    def __init__(self, html, css="", js="", data=None, title=None, width=None, height=None):
        self.type_name = "custom"
        self.title = title
        self.width = width
        self.height = height
        self.html = html
        self.css = css
        self.js = js
        self.data = data # Houses dynamic localized state data maps

    def serialize(self):
        return {
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "html": self.html,
            "css": self.css,
            "js": self.js,
            "data": self.data
        }
