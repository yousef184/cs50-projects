#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    // check user inputs
    if (argc != 2)
    {
        printf("./recover IMAGE");
        return 1;
    }
    // open input file
    FILE *input = fopen(argv[1], "r");
    //check validity of file
    if (input == NULL)
    {
        return 1;
    }
    // making a buffer
    unsigned char buffer [512];
    //counting images
    int count = 0;
    FILE *output = NULL;
    char *filename = malloc(8 * sizeof(char));
    while (fread(buffer, sizeof(char), 512, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0   )
        {
            sprintf(filename, "%03i.jpg", count);
            output = fopen(filename, "w");
            count++;
        }
        if (output != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output);
        }
    }
    fclose(input);
    fclose(output);
    free(filename);
}