import random

class Admin:
    def __init__(self, bank_details=None, customer_details=None, amount=None):
        self.bank_details = bank_details if bank_details else {}
        self.customer_details = customer_details if customer_details else {}
        self.amount = amount if amount else {}

    def update_bank_details(self, bank, customer):
        if bank not in self.bank_details:
            self.bank_details[bank] = [customer]
        else:
            self.bank_details[bank].append(customer)

    def get_bank_details(self):
        return self.bank_details

    def get_customer_details(self, username):
        return self.customer_details.get(username, "User not found")

    def get_total_amount(self):
        total_amount = 0
        for customers in self.bank_details.values():
            for customer in customers:
                total_amount += customer.balance
        return total_amount


class Customer:
    def __init__(self, username, password, name, account_number, bank):
        self.username = username
        self.password = password
        self.name = name
        self.account_number = account_number
        self.bank = bank
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(("Deposit", amount))
        if len(self.transactions) > 5:
            self.transactions.pop(0)
        return f"Amount {amount} deposited successfully. New balance: {self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.transactions.append(("Withdraw", amount))
        if len(self.transactions) > 5:
            self.transactions.pop(0)
        return f"Amount {amount} withdrawn successfully. New balance: {self.balance}"

    def transfer(self, recipient_account, amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        self.transactions.append(("Transfer to " + recipient_account.name, amount))
        if len(self.transactions) > 5:
            self.transactions.pop(0)
        recipient_account.balance += amount
        recipient_account.transactions.append(("Transfer from " + self.name, amount))
        if len(recipient_account.transactions) > 5:
            recipient_account.transactions.pop(0)
        return f"Amount {amount} transferred successfully to {recipient_account.name}. New balance: {self.balance}"

    def mini_statement(self):
        statement = "Mini statement:\n"
        for transaction in self.transactions:
            statement += f"{transaction[0]}: {transaction[1]}\n"
        return statement


class Bank:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        self.customers.append(customer)
        return "Customer added successfully"

    def authenticate(self, username, password):
        for customer in self.customers:
            if customer.username == username and customer.password == password:
                return customer
        return None

# Example Usage:
if __name__ == "__main__":
    bank1 = Bank()
    bank2 = Bank()
    bank3 = Bank()

    admin = Admin()

    while True:
        print("\n1. Login")
        print("2. Add User")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")

            # Assuming admin login check
            if username == "admin" and password == "admin":
                while True:
                    print("\nAdmin Options:")
                    print("1. Bank Details")
                    print("2. Customer Details")
                    print("3. Amount")
                    print("4. Logout")

                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        print(admin.get_bank_details())
                    elif admin_choice == "2":
                        username = input("Enter customer username: ")
                        print(admin.get_customer_details(username))
                    elif admin_choice == "3":
                        print(admin.get_total_amount())
                    elif admin_choice == "4":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                # Customer login
                bank_choice = input("Select Bank (1. KVB, 2. HDFC, 3. ICICI): ")

                if bank_choice == "1":
                    bank = bank1
                elif bank_choice == "2":
                    bank = bank2
                elif bank_choice == "3":
                    bank = bank3
                else:
                    print("Invalid bank choice. User not added.")
                    continue

                username = input("Enter username: ")
                password = input("Enter password: ")

                customer = bank.authenticate(username, password)

                if customer:
                    while True:
                        print("\nCustomer Options:")
                        print("1. Deposit")
                        print("2. Withdraw")
                        print("3. Transfer")
                        print("4. Mini Statement")
                        print("5. Logout")

                        customer_choice = input("Enter your choice: ")

                        if customer_choice == "1":
                            amount = float(input("Enter amount to deposit: "))
                            print(customer.deposit(amount))
                        elif customer_choice == "2":
                            amount = float(input("Enter amount to withdraw: "))
                            print(customer.withdraw(amount))
                        elif customer_choice == "3":
                            recipient_account = input("Enter recipient's account number: ")
                            amount = float(input("Enter amount to transfer: "))
                            # Assuming recipient_account is found using recipient's username
                            recipient_customer = bank.authenticate(recipient_account, "")
                            if recipient_customer:
                                print(customer.transfer(recipient_customer, amount))
                            else:
                                print("Recipient account not found.")
                        elif customer_choice == "4":
                            print(customer.mini_statement())
                        elif customer_choice == "5":
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("Invalid username or password. Please try again.")

        elif choice == "2":
            role = int(input("Are you an \n 1. admin \n 2. customer: "))
            if role == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                admin.customer_details[username] = {"Username": username, "Password": password}
            elif role == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")
                name = input("Enter name: ")
                account_number = input("Enter account number: ")
                bank_choice = input("Select Bank (1. KVB, 2. HDFC, 3. ICICI): ")

                if bank_choice == "1":
                    bank = bank1
                elif bank_choice == "2":
                    bank = bank2
                elif bank_choice == "3":
                    bank = bank3
                else:
                    print("Invalid bank choice. User not added.")
                    continue

                new_customer = Customer(username, password, name, account_number, bank)
                bank.add_customer(new_customer)
                admin.update_bank_details(bank, new_customer)
                admin.customer_details[username] = {"Username": username, "Password": password}
                print("User added successfully.")
            else:
                print("Invalid role. Please try again.")
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
