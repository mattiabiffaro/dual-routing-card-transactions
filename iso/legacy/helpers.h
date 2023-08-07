#ifndef HELPERS_H
#define HELPERS_H

#define MAX 4096
#define COUNT_MAX 999999
#define field_n 128
#define field_n16 32
#define authReq "1100"
#define advice "1120"
#define adviceRepeat "1121"
#define reversal "1420"
#define reversalRepeat "1421"
#define STATE_SIZE 256

// Define field
typedef struct
{
    char present;
    char *value;
    int var_len;
    int len;
    bool default_used;
    bool mallocd;
}
field;

// Define mandatory fields
typedef struct
{
    bool mandatory;
    char *def_val;
}
mandatory_fields;

// Define archive of random numbers already used
typedef struct
{
    bool STAN;
    bool AuthCode;
    bool resID;
}
rand_archive;

// Declare array of Data Elements
extern field DE[field_n + 1];

// Declare mandatory fields
extern mandatory_fields authDE[field_n + 1];
extern mandatory_fields advDE[field_n + 1];
extern mandatory_fields revDE[field_n + 1];

// Declare archive of counters already used
// A counter will not be repeated twice
// The program supports up to COUNT_MAX different counters
extern rand_archive used[COUNT_MAX + 1];

// Declare counters
extern int AuthCounter;
extern int resIDCounter;
extern int STANCounter;
extern int OriginalSTAN;
extern int AmtCounter;

// Declare time objects and state array for random()
extern struct tm *sys_tm;
extern struct tm *Originaltm;
extern char state[STATE_SIZE];

// Declare pointers
extern FILE *inptr;
extern FILE *outptr;
extern char *buffer;
extern char *line;
extern char *scenario;
extern char *msg;
extern char *datetime;

// Prototypes
void define_len(void);
void define_mandatory(void);
struct tm * get_time(void);
void writer(void);
void init_counters(void);
void set_DEs(void);
bool ismandatory(char *MTI, int i);
char * set_default(int i, char *MTI);
void update_counters(void);
void add_padding(void);
void print_headers(void);
void print_msg(void);
void print_bitmap(void);
char * set_len(int len_prefix, char *value);
char * sprintf_counter(int data_element, char *MTI);
char * set_resIDcounter(char *MTI);
void free_DEs(void);
void clear_defaults(void);

#endif // HELPERS_H