class Category:
    def __init__(self, name):
        """
        Constructor for the Category class
        """
        self._name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """
        Adds deposits to the ledger list

        Args:
            amount (float):                 Represents the amount that was deposited.
            description (str, optional):    Represents reason for the deposit. Defaults to "".
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Adds withdraws to the ledger list (if possible)

        Args:
            amount (float):                 Represents the amount that was withdrawn.
            description (str, optional):    Represents reason for the withdrawal. Defaults to "".

        Returns:
            bool:   Returns a bool value that determines if the withdraw took place
        """
        if not self.check_funds(amount):
            return False

        self.ledger.append({"amount": 0 - amount, "description": description})
        return True

    def transfer(self, amount, category):
        """
        Transfer amounts to other categories

        Args:
            amount (float):         Represents the amount to transfer.
            category (Category):    Represents the category to transfer money to.

        Returns:
            bool:   Returns a bool value that determines if the transfer took place
        """
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, "Transfer to " + category._name)
        category.deposit(amount, "Transfer from " + self._name)
        return True

    def check_funds(self, amount):
        """
        Checks if there are enough funds to withdraw or transfer

        Args:
            amount (float): Represents the amount that the user wishes to withdraw or transfer

        Returns:
            bool:   Returns a bool value which determines if there are enough funds
        """
        return amount <= self.get_balance()

    def get_balance(self):
        """
        Gets the user's total balance

        Returns:
            float:  Returns the user's total balance
        """
        bal = 0.00

        # Adds to the balance
        for activity in self.ledger:
            bal += activity.get("amount")

        return bal

    def __str__(self):
        """
        Displays a budget while printing a Category object based on
        https://forum.freecodecamp.org/t/budget-app-python/410549/2

        Returns:
            str:    Returns the budget that should be displayed
        """
        items = ""
        total = 0.00

        for i in range(len(self.ledger)):
            items += f"{self.ledger[i]['description'][0:23]:23}" + \
                f"{self.ledger[i]['amount']:>7.2f}" + "\n"
            total += self.ledger[i]["amount"]

        return f"{self._name:*^30}\n" + items + "Total: " + str(total)


def create_spend_chart(categories):
    """
    Creates a spending chart for all categories based on
    https://github.com/fuzzyray/budget-app/blob/main/budget.py

    Args:
        categories (list):  Represents the list that contains all of the categories.

    Returns:
        str:    Returns the spending chart
    """
    chart = "Percentage spent by category\n"
    totals = []

    # Gets the totals
    for category in categories:
        total = 0
        for ledger in category.ledger:
            if ledger["amount"] < 0:
                total += abs(ledger["amount"])

        totals.append(round(total, 2))

    # Gets percentages
    total = round(sum(totals), 2)
    percents = list(map(lambda amount: int(
        (((amount / total) * 10) // 1) * 10), totals))

    # Retrieves and formats the percentages
    # and adds bars for the chart
    for num in reversed(range(0, 101, 10)):
        chart += str(num).rjust(3) + "|"
        for percent in percents:
            if percent >= num:
                chart += " o "
            else:
                chart += "   "

        chart += " \n"

    # Adds dashes
    chart += " "*4 + "-"*10 + "\n"

    # Adds category names
    names = list(map(lambda category: category._name, categories))
    maxLen = max(map(lambda name: len(name), names))
    names = list(map(lambda name: name.ljust(maxLen), names))

    for name in zip(*names):
        chart += " "*4 + \
            "".join(map(lambda char: char.center(3), name)) + " \n"

    return chart.rstrip("\n")   # Removes the last new line character
