// This program takes a binary bitmap and converts it to the hexadecimal equivalent
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bitmap.h"

char * bitmap16(char *value)
{
    if (strlen(value) != b_len)
    {
        printf("Binary bitmap must be %i chars long\n", b_len);
        exit(1);
    }

    // Initialize variables
    long ltok = 0;
    char *map = malloc(sizeof(char) * (x_len + 1));
    if (map == NULL)
    {
        printf("Not enough memory for map\n");
        exit(1);
    }
    map[0] = '\0';

    // Populate string
    for (int i = 0; i < b_len; i += 4)
    {
        // Divide bitmap in 4 bits chunks (+ null terminator). Store each chunk in a string buffer
        char *l = malloc(sizeof(char) * 5);
        if (l == NULL)
        {
            printf("Not enough memory for l\n");
            free(map);
            exit(1);
        }
        char *c = malloc(sizeof(char) * 2);
        if (c == NULL)
        {
            printf("Not enough memory for c\n");
            free(map);
            free(l);
            exit(1);
        }

        strncpy(l, value + i, 4);
        l[4] = '\0';
        // Convert buffer into a long
        ltok = strtol(l, NULL, 2);
        // Print long to string as hexadecimal value
        sprintf(c, "%lX", ltok);
        strcat(map, c);
        free(l);
        free(c);
    }

    return map;
}