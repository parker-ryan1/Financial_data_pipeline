
class FinancialAssessment:
    def __init__(self, current_assets, non_current_assets, current_liabilities, long_term_liabilities, equity, receivables, receivables_overdue, cogs, average_inventory, ebit, interest_expense, revenue, total_assets, net_income, dividends):
        self.current_assets = current_assets
        self.non_current_assets = non_current_assets
        self.current_liabilities = current_liabilities
        self.long_term_liabilities = long_term_liabilities
        self.equity = equity
        self.receivables = receivables
        self.receivables_overdue = receivables_overdue
        self.cogs = cogs
        self.average_inventory = average_inventory
        self.ebit = ebit
        self.interest_expense = interest_expense
        self.revenue = revenue
        self.total_assets = total_assets
        self.net_income = net_income
        self.dividends = dividends

    def current_ratio(self):
        return self.current_assets / self.current_liabilities

    def quick_ratio(self):
        return (self.current_assets - self.average_inventory) / self.current_liabilities

    def receivables_overdue_percentage(self):
        return (self.receivables_overdue / self.receivables) * 100

    def inventory_turnover(self):
        return self.cogs / self.average_inventory

    def debt_to_equity_ratio(self):
        total_liabilities = self.current_liabilities + self.long_term_liabilities
        return total_liabilities / self.equity

    def interest_coverage_ratio(self):
        return self.ebit / self.interest_expense

    def return_on_assets(self):
        return (self.net_income / self.total_assets) * 100

    def return_on_equity(self):
        return (self.net_income / self.equity) * 100

    def gross_margin(self):
        return ((self.revenue - self.cogs) / self.revenue) * 100
  def net_profit_margin(self):
        return (self.net_income / self.revenue) * 100

    def dividend_payout_ratio(self):
        return (self.dividends / self.net_income) * 100

    def run_assessment(self):
        print("Financial Risk Assessment")
        print("==========================")
        print(f"Current Ratio: {self.current_ratio():.2f} (Benchmark: 2.0)")
        print(f"Quick Ratio: {self.quick_ratio():.2f} (Benchmark: 1.5)")
        print(f"Receivables Overdue Percentage: {self.receivables_overdue_percentage():.2f}% (Benchmark: 20%)")
        print(f"Inventory Turnover: {self.inventory_turnover():.2f} times (Benchmark: 6 times)")
        print(f"Debt-to-Equity Ratio: {self.debt_to_equity_ratio():.2f} (Benchmark: 0.5)")
        print(f"Interest Coverage Ratio: {self.interest_coverage_ratio():.2f} (Benchmark: 5.0)")
        print(f"Return on Assets (ROA): {self.return_on_assets():.2f}% (Benchmark: 5%)")
        print(f"Return on Equity (ROE): {self.return_on_equity():.2f}% (Benchmark: 15%)")
        print(f"Gross Margin: {self.gross_margin():.2f}% (Benchmark: 40%)")
        print(f"Net Profit Margin: {self.net_profit_margin():.2f}% (Benchmark: 10%)")
        print(f"Dividend Payout Ratio: {self.dividend_payout_ratio():.2f}% (Benchmark: 30%)")

def get_input(prompt, cast_func):
    while True:
        try:
            return cast_func(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    current_assets = get_input("Enter current assets: ", float)
    non_current_assets = get_input("Enter non-current assets: ", float)
    current_liabilities = get_input("Enter current liabilities: ", float)
    long_term_liabilities = get_input("Enter long-term liabilities: ", float)
    equity = get_input("Enter equity: ", float)
    receivables = get_input("Enter total receivables: ", float)
    receivables_overdue = get_input("Enter receivables overdue: ", float)
    cogs = get_input("Enter cost of goods sold (COGS): ", float)
    average_inventory = get_input("Enter average inventory: ", float)
    ebit = get_input("Enter earnings before interest and taxes (EBIT): ", float)
    interest_expense = get_input("Enter interest expense: ", float)
    revenue = get_input("Enter total revenue: ", float)
    total_assets = get_input("Enter total assets: ", float)
    net_income = get_input("Enter net income: ", float)
    dividends = get_input("Enter dividends paid: ", float)

    assessment = FinancialAssessment(
        current_assets, non_current_assets, current_liabilities, long_term_liabilities,
        equity, receivables, receivables_overdue, cogs, average_inventory, ebit, interest_expense,
        revenue, total_assets, net_income, dividends
    )

    assessment.run_assessment()
