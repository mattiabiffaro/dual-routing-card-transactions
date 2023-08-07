// This program takes an hexadecimal bitmap and converts it to the binary equivalent
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "bitmap.h"

char * bitmap2(char *value)
{
    if (strlen(value) != x_len)
    {
        printf("Hexadecimal bitmap must be %i chars long\n", x_len);
        exit(1);
    }

    char *map = malloc(sizeof(char) * (b_len + 1));
    if (map == NULL)
    {
        printf("Not enough space for map\n");
        exit(1);
    }
    map[0] = '\0';

    for (int i = 0; i < x_len; i++)
    {
        switch (toupper(value[i]))
        {
            case '0':

                strcat(map, "0000"); break;

            case '1':

                strcat(map, "0001"); break;

            case '2':

                strcat(map, "0010"); break;

            case '3':

                strcat(map, "0011"); break;

            case '4':

                strcat(map, "0100"); break;

            case '5':

                strcat(map, "0101"); break;

            case '6':

                strcat(map, "0110"); break;

            case '7':

                strcat(map, "0111"); break;

            case '8':

                strcat(map, "1000"); break;

            case '9':

                strcat(map, "1001"); break;

            case 'A':

                strcat(map, "1010"); break;

            case 'B':

                strcat(map, "1011"); break;

            case 'C':

                strcat(map, "1100"); break;

            case 'D':

                strcat(map, "1101"); break;

            case 'E':

                strcat(map, "1110"); break;

            case 'F':

                strcat(map, "1111"); break;

            default:

                printf("Invalid char found\n");
                exit(1);
        }
    }

    return map;
}