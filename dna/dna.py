import csv
import sys


def main():
    try:
        flag = 0
        # TODO: Check for command-line usage
        file1 = open(sys.argv[1])
        # TODO: Read database file into a variable
        reader = csv.reader(file1)
        # TODO: Read DNA sequence file into a variable
        file = open(sys.argv[2])
        # TODO: Find longest match of each STR in DNA sequence
        string = file.read()
        x = longest_match(string, "AGATC")
        y = longest_match(string, "TTTTTTCT")
        z = longest_match(string, "AATG")
        a = longest_match(string, "TCTAG")
        b = longest_match(string, "GATA")
        c = longest_match(string, "TATC")
        d = longest_match(string, "GAAA")
        e = longest_match(string, "TCTG")

        # TODO: Check database for matching profiles
        if sys.argv[1] == "databases/large.csv":
            for row in reader:
                if row[0] == "name":
                    continue
                if (int(row[1]) == x) and (int(row[2]) == y) and (int(row[3]) == z) and (int(row[4]) == a) and (int(row[5]) == b) and (int(row[6]) == c) and (int(row[7]) == d) and (int(row[8]) == e):
                    print(row[0])
                    flag = 1
        if sys.argv[1] == "databases/small.csv":
            for row in reader:
                if row[0] == "name":
                    continue
                if (int(row[1])== x) and (int(row[2]) == z) and (int(row[3]) == c):
                    print(row[0])
                    flag = 1
        if flag == 0:
            print("no match")
        file1.close()
        file.close()
    except:
        print("Usage: python dna.py data.csv sequence.txt")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
