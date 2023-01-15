#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char alphabet[] = "abcdefghijklmnopqrstuvwxyz";
char ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
    // TODO: Print the winner
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int s = strlen(word);
    int sum = 0;
    int x;
    int k;
    // IF char is capital
    for (int i = 0; i < s ; i++)
    {
        if (isupper(word[i]))
        {
            for (int q = 0; q < 24; q++)
            {
                if (word[i] != ALPHABET[q])
                {
                    int f = 5;
                }
                else
                {
                    sum = sum + POINTS[q];
                    break;
                }
            }
        }
        //if char is small
        for (k = 0; k < 24; k++)
        {
            if (word[i] != alphabet[k])
            {
                int r = 5;
            }
            else
            {
                sum = sum + POINTS[k];
                break;
            }
        }
    }
    //return score
    return sum;
}
