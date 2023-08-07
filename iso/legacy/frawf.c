// This program gets a CSV file containing formatted ISO messages
// then prints the resulting raw messages one by one in a single concatenated string, including the hexadecimal bitmap, to an output CSV file
#define _DEFAULT_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#include "helpers.h"

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: %s [input].csv [output].csv\n", argv[0]);
        return 1;
    }

    // Define fields length
    define_len();
    // Define mandatory fields
    define_mandatory();

    inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        printf("Not enough memory for %s\n", argv[1]);
        return 2;
    }

    outptr = fopen(argv[2], "w");
    if (outptr == NULL)
    {
        printf("Not enough memory for %s\n", argv[2]);
        fclose(inptr);
        return 2;
    }

    buffer = malloc(sizeof(char) * MAX);
    if (buffer == NULL)
    {
        printf("Not enough memory for buffer\n");
        fclose(inptr);
        fclose(outptr);
        return 2;
    }

    // Skip header line
    fgets(buffer, MAX, inptr);

    // Print ISO messages to outptr line by line
    writer();

    fclose(inptr);
    fclose(outptr);
    free(buffer);
    printf("%s file generated\n", argv[2]);
    return 0;
}