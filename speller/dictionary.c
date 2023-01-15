// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

int counter = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *cursor;
    int k = hash(word);
    cursor = table[k];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word))
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int total = 0;
    for(int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    int hashkey;
    node *n;
    char buff[LENGTH + 1];
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    while (fscanf(file, "%s", buff) != EOF)
    {
        n = (node*)malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word,buff);
        hashkey = hash(buff);
        n->next=table[hashkey];
        table[hashkey]=n;
        counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++) // loop thru all the arrays
    {
        // tmp1 is like a cursor that points to each node while tmp2 is the pointer that frees the prior node
        node *tmp1 = table[i]; // initially tmp1 points to 1st node
        while (tmp1 != NULL) // until end of ll
        {
            node *tmp2 = tmp1; // tmp2 points to what tmp1 points
            tmp1 = tmp1 -> next; // tmp1 points to next node
            free(tmp2); // tmp2 frees the prior node
        }
    }

    return true;
}