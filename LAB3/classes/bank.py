class Account():
    def __init__(self, owner, balance = 0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount} tg. New balance:{self.balance} tg")
        else:
            print("Must be positive")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Not enough funds! Available balance: {self.balance} tg")
        elif amount <= 0:
            print("Must be positive")
        else:
            self.balance -= amount
            print(f"Withdrew {amount} tg. New balance: {self.balance} tg")        

    def show_balance(self):
        print(f"Account balance: {self.balance} tg")

account = Account("Adilzhan", 100000)      
account.show_balance()
account.deposit(50000)
account.withdraw(12000)
account.show_balance
