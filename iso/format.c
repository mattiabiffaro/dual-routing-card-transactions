// This program takes a raw ISO message and converts it into the formatted equivalent
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>

#include "helpers.h"

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./format \'[ISO message]\'\n");
        return 1;
    }

    // Initialize variables
    char *raw = argv[1];
    int position = 0;
    define_len();

    // Get Message Type
    char *type = malloc(sizeof(char) * 5);
    strncpy(type, raw, 4);
    type[4] = '\0';
    printf("<MSG-%s>\n", type);
    position += 4;

    // Get bitmap
    char *hexbitmap = malloc(sizeof(char) * (field_n16 + 1));
    strncpy(hexbitmap, raw + position, field_n16);
    hexbitmap[field_n16] = '\0';
    printf("    001<%s>\n", hexbitmap);
    position += field_n16;

    // Convert bitmap to binary
    char *bitmap = malloc(sizeof(char) * (field_n + 1));
    for (int i = 0; i < field_n16; i++)
    {
        switch (toupper(hexbitmap[i]))
        {
            case '0':

                strcat(bitmap, "0000"); break;

            case '1':

                strcat(bitmap, "0001"); break;

            case '2':

                strcat(bitmap, "0010"); break;

            case '3':

                strcat(bitmap, "0011"); break;

            case '4':

                strcat(bitmap, "0100"); break;

            case '5':

                strcat(bitmap, "0101"); break;

            case '6':

                strcat(bitmap, "0110"); break;

            case '7':

                strcat(bitmap, "0111"); break;

            case '8':

                strcat(bitmap, "1000"); break;

            case '9':

                strcat(bitmap, "1001"); break;

            case 'A':

                strcat(bitmap, "1010"); break;

            case 'B':

                strcat(bitmap, "1011"); break;

            case 'C':

                strcat(bitmap, "1100"); break;

            case 'D':

                strcat(bitmap, "1101"); break;

            case 'E':

                strcat(bitmap, "1110"); break;

            case 'F':

                strcat(bitmap, "1111"); break;

            default:

                printf("Invalid char found in bitmap\n");
                free(type);
                free(hexbitmap);
                free(bitmap);
                return 2;
        }
    }

    // Take note of present fields
    for (int i = 0; i < field_n; i++)
    {
        switch (bitmap[i])
        {
            case '0':

                DE[i + 1].present = 0; break;

            case '1':

                DE[i + 1].present = 1; break;

            default:

                printf("Invalid char found in bitmap\n");
                free(type);
                free(hexbitmap);
                free(bitmap);
                return 2;
        }
    }

    // Iterate for each field
    for (int i = 2; i < field_n; i++)
    {
        if (DE[i].present)
        {
            if (DE[i].var_len)
            {
                char *s = malloc(sizeof(char) * DE[i].var_len + 1);
                strncpy(s, raw + position, DE[i].var_len);
                s[DE[i].var_len] = '\0';
                DE[i].len = atoi(s);
                position += DE[i].var_len;
                free(s);
            }

            DE[i].value = malloc(sizeof(char) * (DE[i].len + 1));
            strncpy(DE[i].value, raw + position, DE[i].len);
            DE[i].value[DE[i].len] = '\0';
            printf("    %03i<%s>\n", i, DE[i].value);
            free(DE[i].value);
            position += DE[i].len;
        }
    }
        // Check field length
        // Extract field from string
        // Take note of current position on string

    free(type);
    free(hexbitmap);
    free(bitmap);
    return 0;
}