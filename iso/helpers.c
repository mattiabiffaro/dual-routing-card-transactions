#define _DEFAULT_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <sys/time.h>

#include "helpers.h"

// Declare array of Data Elements
field DE[field_n + 1];

// Declare mandatory fields
mandatory_fields authDE[field_n + 1];
mandatory_fields advDE[field_n + 1];
mandatory_fields revDE[field_n + 1];

// Declare archive of counters already used
// A counter will not be repeated twice
// The program supports up to COUNT_MAX different counters
rand_archive used[COUNT_MAX + 1];

// Initialize or declare counters
int AuthCounter = 0;
int STANCounter = 0;
int OriginalSTAN = 0;
int resIDCounter = 0;
int AmtCounter = 1;

// Declare pointers
FILE *inptr;
FILE *outptr;
char *buffer;
char *line;
char *scenario;
char *msg;
char *datetime;

// Declare time objects and state array for random()
struct tm *sys_tm;
struct tm *Originaltm;
char state[STATE_SIZE];


// Defines length attributes of data elements
void define_len(void)
{
    // Initialize variable length to 0
    for (int i = 0; i < field_n + 1; i++)
    {
        DE[i].var_len = 0;
    }

    // Define variable length prefixing format
    DE[2].var_len = 2;
    DE[32].var_len = 2;
    DE[33].var_len = 2;
    DE[43].var_len = 2;
    DE[46].var_len = 3;
    DE[48].var_len = 3;
    DE[54].var_len = 3;
    DE[56].var_len = 2;
    DE[59].var_len = 3;
    DE[63].var_len = 3;
    DE[93].var_len = 2;
    DE[94].var_len = 2;
    DE[100].var_len = 2;
    DE[102].var_len = 2;
    DE[116].var_len = 3;

    // Define fixed lengths (or max length for variable length fields)
    DE[3].len = 6;
    DE[4].len = 12;
    DE[6].len = 12;
    DE[11].len = 6;
    DE[12].len = 12;
    DE[14].len = 4;
    DE[22].len = 12;
    DE[23].len = 3;
    DE[24].len = 3;
    DE[25].len = 4;
    DE[26].len = 4;
    DE[37].len = 12;
    DE[38].len = 6;
    DE[39].len = 3;
    DE[41].len = 8;
    DE[42].len = 15;
    DE[49].len = 3;
    DE[51].len = 3;
    DE[102].len = 23;
}

// Define which fields have mandatory values and sets those values when they are fixed
// Default values that are not fixed are calculated via the set_default function
void define_mandatory(void)
{
    // Initialize mandatory fields to false
    for (int i = 0; i < field_n + 1; i++)
    {
        authDE[i].mandatory = false;
        advDE[i].mandatory = false;
        revDE[i].mandatory = false;
        DE[i].default_used = false;
        DE[i].mallocd = false;
    }

    // Define mandatory fields
    authDE[2].mandatory = advDE[2].mandatory = revDE[2].mandatory = true;
    authDE[2].def_val = advDE[2].def_val = revDE[2].def_val = "557383******9999";
    authDE[3].mandatory = advDE[3].mandatory = revDE[3].mandatory = true;
    authDE[3].def_val = advDE[3].def_val = revDE[3].def_val = "000000";
    authDE[4].mandatory = advDE[4].mandatory = revDE[4].mandatory = true;
    // authDE[4].def_val, advDE[4].def_val, revDE[4].def_val are set later with the set_default function
    authDE[6].mandatory = advDE[6].mandatory = revDE[6].mandatory = true;
    // authDE[6].def_val, advDE[6].def_val, revDE[6].def_val are set later with the set_default function
    authDE[11].mandatory = advDE[11].mandatory = revDE[11].mandatory = true;
    // authDE[11].def_val, advDE[11].def_val, revDE[11].def_val are set later with the set_default function
    authDE[12].mandatory = advDE[12].mandatory = revDE[12].mandatory = true;
    // authDE[12].def_val = advDE[12].def_val = revDE[12].def_val are set later with the set_default function
    authDE[14].mandatory = advDE[14].mandatory = true;
    authDE[14].def_val = advDE[14].def_val = "****";
    authDE[22].mandatory = advDE[22].mandatory = true;
    authDE[22].def_val = advDE[22].def_val = "100050J00011";
    authDE[23].mandatory = advDE[23].mandatory = revDE[23].mandatory = true;
    authDE[23].def_val = advDE[23].def_val = revDE[23].def_val = "000";
    authDE[24].mandatory = advDE[24].mandatory = revDE[24].mandatory = true;
    authDE[24].def_val = advDE[24].def_val = "100";
    revDE[24].def_val = "400";
    advDE[25].mandatory = revDE[25].mandatory = true;
    advDE[25].def_val = revDE[25].def_val = "1403";
    authDE[26].mandatory = advDE[26].mandatory = true;
    authDE[26].def_val = advDE[26].def_val = "5999";
    authDE[32].mandatory = advDE[32].mandatory = revDE[32].mandatory = true;
    authDE[32].def_val = advDE[32].def_val = revDE[32].def_val = "999701";
    authDE[33].mandatory = advDE[33].mandatory = revDE[33].mandatory = true;
    authDE[33].def_val = advDE[33].def_val = revDE[33].def_val = "12928";
    authDE[37].mandatory = advDE[37].mandatory = revDE[37].mandatory = true;
    authDE[37].def_val = advDE[37].def_val = revDE[37].def_val = "080000100000";
    authDE[38].mandatory = advDE[38].mandatory = revDE[38].mandatory = true;
    // authDE[38].def_val, advDE[38].def_val, revDE[38].def_val are set later with the set_default function
    advDE[39].mandatory = true;
    advDE[39].def_val = "000";
    authDE[41].mandatory = advDE[41].mandatory = revDE[41].mandatory = true;
    authDE[41].def_val = advDE[41].def_val = revDE[41].def_val = "MTF TEST";
    authDE[42].mandatory = advDE[42].mandatory = revDE[42].mandatory = true;
    authDE[42].def_val = advDE[42].def_val = revDE[42].def_val = "ABC123TESTMTF19";
    authDE[43].mandatory = advDE[43].mandatory = true;
    // authDE[43].def_val, advDE[43].def_val are set later with the set_default function
    // authDE[43].def_val = advDE[43].def_val = "DEFAULT\\Vegas\\             ITA";
    authDE[49].mandatory = advDE[49].mandatory = revDE[49].mandatory = true;
    authDE[49].def_val = advDE[49].def_val = revDE[49].def_val = "978";
    authDE[51].mandatory = advDE[51].mandatory = revDE[51].mandatory = true;
    authDE[51].def_val = advDE[51].def_val = revDE[51].def_val = "978";
    revDE[56].mandatory = true;
    // revDE[56].def_val is set later with the set_default function
    authDE[63].mandatory = advDE[63].mandatory = revDE[63].mandatory = true;
    // authDE[63].def_val, advDE[63].def_val, revDE[63].def_val are set later with the set_default function
    authDE[93].mandatory = advDE[93].mandatory = revDE[93].mandatory = true;
    authDE[93].def_val = advDE[93].def_val = revDE[93].def_val = "12928";
    authDE[94].mandatory = advDE[94].mandatory = revDE[94].mandatory = true;
    authDE[94].def_val = advDE[94].def_val = revDE[94].def_val = "999701";
    authDE[100].mandatory = advDE[100].mandatory = revDE[100].mandatory = true;
    authDE[100].def_val = advDE[100].def_val = revDE[100].def_val = "00000000000";
    authDE[102].mandatory = advDE[102].mandatory = revDE[102].mandatory = true;
    authDE[102].def_val = advDE[102].def_val = revDE[102].def_val = "600501992609           ";
    authDE[116].mandatory = advDE[116].mandatory = revDE[116].mandatory = true;
    authDE[116].def_val = advDE[116].def_val = revDE[116].def_val = "102510000660038063301-1234";
}