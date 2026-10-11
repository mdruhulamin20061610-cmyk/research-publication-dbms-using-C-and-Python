// faculty_update.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Faculty {
    char faculty_id[20];
    char full_name[100];
    char short_name[20];
    char designation[50];
    char research_interest[200];
};

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("ERROR: No faculty data provided\n");
        return 0;
    }
    
    // For simplicity, using CSV format
    char* data = argv[1];
    
    // Open file in append mode (REMOVED ../)
    FILE *file = fopen("data_files/faculty.dat", "a");
    if (file == NULL) {
        printf("ERROR: Cannot open faculty data file\n");
        return 0;
    }
    
    // Write data (format: id,full_name,short_name,designation,research)
    fprintf(file, "%s\n", data);
    fclose(file);
    
    printf("SUCCESS: Faculty data saved\n");
    return 1;
}