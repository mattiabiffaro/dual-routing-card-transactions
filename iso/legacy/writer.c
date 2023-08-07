#define _DEFAULT_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <sys/time.h>

#include "helpers.h"

// Main frawf function
// Reads formatted messages from the infile, writes them to the outfile
void writer(void)
{
    int row = 1;

    init_counters();
    print_headers();

    while (fgets(buffer, MAX, inptr))
    {
        row++;
        clear_defaults();

        // Line is a pointer that will be used by strsep
        // Buffer, instead, will keep pointing to the beginning of the row
        line = buffer;

        // Initialize bitmap
        DE[1].value = malloc(sizeof(char) * field_n + 1);
        if (DE[1].value == NULL)
        {
            printf("Not enough memory for bitmap\n");
            fclose(inptr);
            fclose(outptr);
            free(buffer);
            exit(2);
        }
        strcpy(DE[1].value, "1");

        // Get scenario name
        scenario = strsep(&line, ",");
        if (!strcmp(scenario, ""))
            scenario = "Untitled";

        // Get Message type
        DE[0].value = strsep(&line, ",");
        if (!strcmp(DE[0].value, ""))
        {
            DE[0].value = authReq;
            DE[0].default_used = true;
        }
        if (
                strcmp(DE[0].value, authReq) &&
                strcmp(DE[0].value, advice) && strcmp(DE[0].value, adviceRepeat) &&
                strcmp(DE[0].value, reversal) && strcmp(DE[0].value, reversalRepeat)
            )
        {
            printf("Message type must be %s, %s, %s, %s, %s or empty on row %i\n", authReq, advice, adviceRepeat, reversal, reversalRepeat, row);
            fclose(inptr);
            fclose(outptr);
            free(buffer);
            free(datetime);
            free(DE[1].value);
            exit(3);
        }
        DE[0].present = '1';

        set_DEs();
        update_counters();
        add_padding();
        print_msg();
        free_DEs();
    }
}

// Initializes date and time
// Initialize counters based on random number generation
void init_counters(void)
{
     sys_tm = get_time();
     Originaltm = sys_tm;

     srand((unsigned int) time(NULL));
     initstate((unsigned int) time(NULL), state, STATE_SIZE);

    // No counter is used at first
    // 0 will be reserved, hence it won't be used
    used[0].STAN = used[0].AuthCode = used[0].resID = true;

    for (int i = 1; i < COUNT_MAX + 1; i++)
    {
        used[i].STAN = used[i].AuthCode = used[i].resID = false;
    }

    while (used[STANCounter].STAN)
    {
        STANCounter = OriginalSTAN = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
    }
    used[STANCounter].STAN = true;

    while (used[AuthCounter].AuthCode)
    {
        AuthCounter = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
    }
    used[AuthCounter].AuthCode = true;

    while (used[resIDCounter].resID)
    {
        resIDCounter = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
    }
    used[resIDCounter].resID = true;
}

struct tm * get_time(void)
{
    struct timeval t;
    gettimeofday(&t, NULL);
    struct tm *l = localtime(&t.tv_sec);
    return l;
}

// Whenever a new line is read from the infile, default values are freed
// Default boolean variables are used to signal the program to later free dynamically allocated memory with free_DEs()
void clear_defaults(void)
{
    for (int i = 0; i < field_n + 1; i++)
    {
        DE[i].default_used = DE[i].mallocd = false;
    }
}

// Sets a value for each DE
// Checks which data element is present and constructs the bitmap accordingly
// If a field is empty in the infile, but it's defined as mandatory by the ismandatory function,
// it will be considered present and its value will be set by set_default
void set_DEs(void)
{
    for (int i = 2; i < field_n + 1; i++) // Iterate for every DE
    {
        DE[i].value = strsep(&line, ",");
        if (!strcmp(DE[i].value, ""))
        {
            if (ismandatory(DE[0].value, i))
            {
                DE[i].present = '1';
                DE[i].value = set_default(i, DE[0].value);
                if (DE[i].value == NULL)
                {
                    fclose(inptr);
                    fclose(outptr);
                    free(buffer);
                    free(DE[1].value);
                    free(datetime);
                    exit(2);
                }
            }
            else
            {
                DE[i].present = '0'; // Set presence to false if string is null and no default is set
            }
        }
        else
        {
            DE[i].present = '1'; // Set presence to true if value is assigned
        }
        strcat(DE[1].value, &DE[i].present); // Update the bitmap
    }
    DE[1].present = '1'; // Set bitmap to present
}

// Check if field is mandatory for the given message type
bool ismandatory(char *MTI, int i)
{
    if (!strcmp(MTI, authReq) && authDE[i].mandatory)
    {
        return true;
    }
    else if ((!strcmp(MTI, advice) || !strcmp(MTI, adviceRepeat)) && advDE[i].mandatory)
    {
        return true;
    }
    else if ((!strcmp(MTI, reversal) || !strcmp(MTI, reversalRepeat)) && revDE[i].mandatory)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Sets default values
// When a default value needs to be set dynamically, the sprintf function is called
char * set_default(int i, char *MTI)
{
    DE[i].default_used = true;

    if (!strcmp(MTI, authReq))
    {
        if (i == 4 || i == 6)
        {
            authDE[i].def_val = sprintf_counter(i, MTI);
        }
        else if (i == 11)
            authDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 12)
            authDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 38)
            authDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 43)
            authDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 63)
            authDE[i].def_val = sprintf_counter(i, MTI);
        return authDE[i].def_val;
    }
    else if (!strcmp(MTI, advice) || !strcmp(MTI, adviceRepeat))
    {
        if (i == 4 || i == 6)
        {
            advDE[i].def_val = sprintf_counter(i, MTI);
        }
        else if (i == 11)
            advDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 12)
            advDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 38)
            advDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 43)
            advDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 63)
            advDE[i].def_val = sprintf_counter(i, MTI);
        return advDE[i].def_val;
    }
    else if (!strcmp(MTI, reversal) || !strcmp(MTI, reversalRepeat))
    {
        if (i == 4 || i == 6)
        {
            revDE[i].def_val = sprintf_counter(i, MTI);
        }
        else if (i == 11)
            revDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 12)
            revDE[i].def_val = sprintf_counter(i, MTI);
        else if (i == 38)
            revDE[i].def_val = sprintf_counter(i, MTI);
        // DE56 is a special field composed of MTI, DE11, DE12, and DE32 of the original authorization
        else if (i == 56)
        {
            revDE[i].def_val = sprintf_counter(i, MTI);
        }
        else if (i == 63)
            revDE[i].def_val = sprintf_counter(i, MTI);
        return revDE[i].def_val;
    }

    return NULL;
}

// Used when a default value needs to be set and to do so sprintf must be used to convert an int into a str
char * sprintf_counter(int data_element, char *MTI)
{
    char *result = NULL;

    if (data_element == 4 || data_element == 6)
    {
        result = malloc(sizeof(char) * 13);
        int n = AmtCounter * 100;
        sprintf(result, "%012i", n);
    }
    else if (data_element == 11)
    {
        result = malloc(sizeof(char) * 7);
        sprintf(result, "%06i", STANCounter);
    }
    else if (data_element == 12)
    {
        result = malloc(sizeof(char) * 13);
        sprintf(result, "%02i%02i%02i%02i%02i%02i", (sys_tm->tm_year - 100), (sys_tm->tm_mon + 1), sys_tm->tm_mday, sys_tm->tm_hour, sys_tm->tm_min, sys_tm->tm_sec);
    }
    else if (data_element == 38)
    {
        result = malloc(sizeof(char) * 7);
        sprintf(result, "%06i", AuthCounter);
    }
    else if (data_element == 43)
    {
        result = malloc(sizeof(char) * 43);
        sprintf(result, "%s", scenario);
        strcat(result, "\\Vegas\\             ITA");
    }
    else if (data_element == 56)
    {
        char *tmp_DE56 = malloc(sizeof(char) * 36);
        if (tmp_DE56 == NULL)
        {
            printf("Not enough memory for DE56 buffer\n");
            return NULL;
        }
        tmp_DE56[0] = '\0';
        strcat(tmp_DE56, authReq); // We assume the original authorizaion was an ISO1100 request
        char *strOriginalSTAN = malloc(sizeof(char) * 7);
        sprintf(strOriginalSTAN, "%06i", OriginalSTAN);
        strcat(tmp_DE56, strOriginalSTAN);
        free(strOriginalSTAN);
        char *strOriginaltm = malloc(sizeof(char) * 13);
        sprintf(strOriginaltm, "%02i%02i%02i%02i%02i%02i", (Originaltm->tm_year - 100), (Originaltm->tm_mon + 1), Originaltm->tm_mday, Originaltm->tm_hour, Originaltm->tm_min, Originaltm->tm_sec);
        strcat(tmp_DE56, strOriginaltm);
        free(strOriginaltm);
        char *DE32len = set_len(DE[32].var_len, DE[32].value);
        if (DE32len == NULL)
        {
            return NULL;
        }
        strcat(tmp_DE56, DE32len);
        free(DE32len);
        strcat(tmp_DE56, DE[32].value);
        result = tmp_DE56;
    }
    else if (data_element == 63)
    {
        result = malloc(sizeof(char) * 14);
        result[0] = '\0';
        char *counter = malloc(sizeof(char) * 7);
        sprintf(counter, "%06i", resIDCounter);
        if (!strcmp(MTI, reversal))
            strcat(result, "0209MCC");
        else
            strcat(result, "0109MCC");
        strcat(result, counter);
        free(counter);
    }

    DE[data_element].mallocd = true;
    return result;
}

// If a data element needs to be prefixed with its length, this function calculates the value to be prepended
char * set_len(int len_prefix, char *value)
{
    int n = strlen(value);
    char *l = malloc(sizeof(char) * (len_prefix + 1));
    if (l == NULL)
    {
        return NULL;
    }
    if (len_prefix == 2)
    {
        sprintf(l, "%02i", n);
    }
    else
    {
        sprintf(l, "%03i", n);
    }
    return l;
}

// Updates counters used in sprintf_counter whenever a line in the infile is done processing
// While loops based on the struct rand_archive used array impose no re-usability of any given randomly generated number
void update_counters(void)
{
    sys_tm = get_time();

    while (used[STANCounter].STAN)
    {
        STANCounter = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
    }
    used[STANCounter].STAN = true;

    // Check reversal indicator
    char *rev_ind = strsep(&line, ",");
    // If reversal indicator false, update counters
    if (strcmp(rev_ind, "Y"))
    {
        while (used[AuthCounter].AuthCode)
        {
            AuthCounter = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
        }
        used[AuthCounter].AuthCode = true;

        while (used[resIDCounter].resID)
        {
            resIDCounter = (random() / ((double) RAND_MAX + 1)) * COUNT_MAX;
        }
        used[resIDCounter].resID = true;

        AmtCounter++;

        OriginalSTAN = STANCounter;

        Originaltm = sys_tm;
    }
}

// Adds padding for fixed length fields that require it
void add_padding(void)
{
    // Add 0s at the start of DE004 and DE006
    // Remove decimal point if present
    if (strlen(DE[4].value) < DE[4].len)
    {
        float n = atof(DE[4].value);
        n = n * 100;
        char *s = malloc(sizeof(char) * (DE[4].len + 1));
        sprintf(s, "%012i", (int) n);
        DE[4].value = s;
        DE[4].mallocd = true;
    }
    if (strlen(DE[6].value) < DE[6].len)
    {
        float n = atof(DE[6].value);
        n = n * 100;
        char *t = malloc(sizeof(char) * (DE[6].len + 1));
        sprintf(t, "%012i", (int) n);
        DE[6].value = t;
        DE[6].mallocd = true;
    }

    // Add spaces at the end of DE102
    while (strlen(DE[102].value) < DE[102].len)
    {
        strcat(DE[102].value, " ");
    }
}

// Print the headers of the outfile
void print_headers(void)
{
    fprintf(outptr, "Scenario, ISO Request, ISO Response\n");
}

// Prints raw ISO message to outfile
// Takes each DE.value and concatenates them into a str
void print_msg(void)
{
    // Initialize ISO message string
    msg = malloc(sizeof(char) * MAX);
    if (msg == NULL)
    {
        printf("Not enough memory for msg buffer\n");
        fclose(inptr);
        fclose(outptr);
        free(buffer);
        free(DE[1].value);
        free(datetime);
        exit(2);
    }
    msg[0] = '\0';

    // Print the ISO message
    for (int i = 0; i < field_n; i++)
    {
        int ispresent = atoi(&DE[i].present);

        if (i == 1)
        {
            print_bitmap();
        }
        else if (ispresent && DE[i].var_len)
        {
            // Prefix value length at the beginning of variable length DEs
            char *len = set_len(DE[i].var_len, DE[i].value);
            if (len == NULL)
            {
                fclose(inptr);
                fclose(outptr);
                free(buffer);
                free(DE[1].value);
                free(datetime);
                free(msg);
                exit(2);
            }
            strcat(msg, len);
            free(len);
            // Print DE value
            strcat(msg, DE[i].value);
        }
        else if (ispresent && !DE[i].var_len)
        {
            strcat(msg, DE[i].value);
        }
    }
    fprintf(outptr, "%s,%s\n", scenario, msg);

    free(msg);
}

// Converts binary bitmap into hexadecimal bitmap
void print_bitmap(void)
{
    int len = strlen(DE[1].value);
    long ltok = 0;
    for (int i = 0; i < len; i += 4)
    {
        char *stok = malloc(sizeof(char) * 5);
        if (stok == NULL)
        {
            fclose(inptr);
            fclose(outptr);
            free(buffer);
            free(DE[1].value);
            free(datetime);
            free(msg);
            exit(2);
        }
        strncpy(stok, DE[1].value + i, 4);
        stok[4] = '\0';
        ltok = strtol(stok, NULL, 2);
        free(stok);
        char *d = malloc(sizeof(char) * 2);
        if (d == NULL)
        {
            fclose(inptr);
            fclose(outptr);
            free(buffer);
            free(DE[1].value);
            free(datetime);
            free(msg);
            exit(2);
        }
        sprintf(d, "%lX", ltok);
        strcat(msg, d);
        free(d);
    }
}

// Frees memory for Data Elements allocated dynamically
void free_DEs(void)
{
    free(DE[1].value);
    for (int i = 0; i < field_n + 1; i++)
    {
        if (DE[i].mallocd)
            free(DE[i].value);
    }
}