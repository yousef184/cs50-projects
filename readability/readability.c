#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
int sum;
int count_letters(string text);
int count_words(string p);
int count_scentences(string f);

int main(void)
{

string x = get_string("Text: ");
int y = count_letters(x);
 int s = count_words(x);
int u = count_scentences(x);
float calculation = (0.0588 * y/s *100 ) - (0.296 * u/s * 100)-15.8;
int n = round(calculation);
if (n < 1)
{
    printf("Before Grade 1\n");
}
else if (n>16)
{
    printf("Grade 16+\n");
}
else
{
    printf("Grade %i\n",n);
}
}

//count letters
int count_letters(string text)
{
    int l = strlen(text);
    for (int i = 0 ; i < l; i++)
    {
        if((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
             sum = sum + 1;
        }
    }
return sum;
}

//count words
int count_words(string p)
{
    int word=1;
    int l = strlen(p);
    for (int i = 0 ; i < l; i++)
    {
        if (p[i] == ' ')
        {
            word = word + 1;
        }
    }
    return word;
}

//count scentences
int count_scentences(string f)
{
    int scentences=0;
    int l = strlen(f);
    int i;
    for (i = 0; i < l ; i++)
        {
            if(f[i] == 46 || f[i] == '?' || f[i] == '!' )
            {
                scentences = scentences + 1;
            }
        }
    return scentences;
}