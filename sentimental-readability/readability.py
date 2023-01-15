
def main():
    y = 0
    string = input("Text: ")
    s = len(string.split())
    for char in string:
        if char.isalpha():
            y = y + 1
    u = string.count('.') + string.count('?') + string.count('!')
    calculation = (0.0588 * y/s * 100) - (0.296 * u/s * 100)-15.8
    n = round(calculation)
    if n < 1:
        print("Before Grade 1")
    elif n > 16:
        print("Grade 16+")
    else:
        print(f"Grade {n}")


if __name__ == "__main__":
    main()