// Simulate genetic inheritance of blood type

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Each person has two parents and two alleles
typedef struct person
{
    struct person *parents[2];
    char alleles[2];
}
person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    // Seed random number generator
    srand(time(0));

    // Create a new family with three generations
    person *p = create_family(GENERATIONS);

    // Print family tree of blood types
    print_family(p, 0);

    // Free memory
    free_family(p);
}

// Create a new individual with `generations`
person *create_family(int generations)
{
    char al[4][2];
    char al2[2][2];
    // TODO: Allocate memory for new person
    person *p;
    p = (person *)malloc(sizeof(person));

    // If there are still generations left to create
    if (generations > 1)
    {
        // Create two new parents for current person by recursively calling create_family
        person *parent0 = create_family(generations - 1);
        person *parent1 = create_family(generations - 1);

        // TODO: Set parent pointers for current person
        p->parents[0] = parent0;
        p->parents[1] = parent1;
        // TODO: Randomly assign current person's alleles based on the alleles of their parents
        char a = parent0->alleles[0];
        char b = parent0->alleles[1];
        char c = parent1->alleles[0];
        char d = parent1->alleles[1];
        al[0][0] = a;
        al[0][1] = c;
        al[1][0] = a;
        al[1][1] = d;
        al[2][0] = b;
        al[2][1] = c;
        al[3][0] = b;
        al[3][1] = d;
        if (a ==  b)
        {
            al2[0][0] = a;
            al2[0][1] = c;
            al2[1][0] = a;
            al2[1][1] = d;
            srand(time(0));
            int upper = 1;
            int lower = 0;
            int number;
            number = (rand() % (upper - lower + 1)) + lower;
            p->alleles[0] = al2[number][0];
            p->alleles[1] = al2[number][1];
        }
        else if (c ==  d)
        {
            al2[0][0] = a;
            al2[0][1] = c;
            al2[1][0] = a;
            al2[1][1] = d;
            srand(time(0));
            int upper = 3;
            int lower = 0;
            int number;
            number = (rand() % (upper - lower + 1)) + lower;
            p->alleles[0] = al[number][0];
            p->alleles[1] = al[number][1];
        }
        else
        {
            srand(time(0));
            int upper = 3;
            int lower = 0;
            int number;
            number = (rand() % (upper - lower + 1)) + lower;
            p->alleles[0] = al[number][0];
            p->alleles[1] = al[number][1];
        }
    }

    // If there are no generations left to create
    else
    {
        p->parents[0] = NULL;
        p->parents[1] = NULL;
        // TODO: Randomly assign alleles
        p->alleles[0] = random_allele();
        p->alleles[1] = random_allele();
    }

    // TODO: Return newly created person
    return  p;
}

// Free `p` and all ancestors of `p`.
void free_family(person *p)
{
    // TODO: Handle base case
    if (p == NULL)
    {
        return ;
    }
    // TODO: Free parents recursively
    free_family(p->parents[0]);
    free_family(p->parents[1]);
    // TODO: Free child
    free(p);
}

// Print each family member and their alleles.
void print_family(person *p, int generation)
{
    // Handle base case
    if (p == NULL)
    {
        return;
    }

    // Print indentation
    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }

    // Print person
    if (generation == 0)
    {
        printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else if (generation == 1)
    {
        printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else
    {
        for (int i = 0; i < generation - 2; i++)
        {
            printf("Great-");
        }
        printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }

    // Print parents of current generation
    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

// Randomly chooses a blood type allele.
char random_allele()
{
    int r = rand() % 3;
    if (r == 0)
    {
        return 'A';
    }
    else if (r == 1)
    {
        return 'B';
    }
    else
    {
        return 'O';
    }
}
