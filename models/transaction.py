from datetime import date

class Transaction:
    def __init__(self, date: date, category: str, description: str, amount: float, type: str):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.type = type

    def __str__(self):
        return f"Transaction(date={self.date}, category={self.category}, description={self.description}, amount={self.amount}, type={self.type})"