#!/usr/bin/python3

class UIBDocument():
    def __init__(self, frame) -> None:
        super().__init__()

        self.frame = frame
        
    #################### JQuery Code
    @property
    def document(self):
        return self.frame.documentElement()

    def alert(self, text: str):
        self.document.evaluateJavaScript("alert('%s')" % text)
    