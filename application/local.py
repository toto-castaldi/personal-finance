import common.portfolio as portfolio
import sys

if __name__ == "__main__":
    account_id = sys.argv[1]
    p = portfolio.Portfolio(account_id)
    print(p.values[-1].assets[1].amount)