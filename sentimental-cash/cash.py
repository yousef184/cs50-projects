
def get_cents():
    try:
        while True:
            cents = float(input("change owed: "))
            if (cents >= 0):
                break
        return cents
    except:
       cents = get_cents()
       return cents

def calculate_quarters(cents):
    quarters = cents//0.25
    return quarters

def calculate_dimes(cents):
    dimes = cents//0.10
    return dimes

def calculate_nickels(cents):
    nickels = cents//0.05
    return nickels

def calculate_pennies(cents):
    Pennies = cents//0.01
    return Pennies

def main():
    cents = get_cents()
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 0.25
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 0.1
    cents = round(cents,2)
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 0.05
    cents = round(cents,3)
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 0.01
    coins = quarters + dimes + nickels + pennies
    print(coins)

if __name__ == "__main__":
    main()