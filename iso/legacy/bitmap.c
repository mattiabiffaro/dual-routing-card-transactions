#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "bitmap.h"

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./bitmap [value]\n");
        return 1;
    }

    char* map;

    // Handle options
    if (strlen(argv[1]) == b_len)
    {
        map = bitmap16(argv[1]);
    }
    else
    {
        map = bitmap2(argv[1]);
    }

    printf("%s\n", map);
    free(map);
    return 0;
}