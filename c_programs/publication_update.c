// publication_update.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("ERROR: No publication data provided\n");
        return 0;
    }
    
    char* data = argv[1];
    
    // REMOVED ../
    FILE *file = fopen("data_files/publication.dat", "a");
    if (file == NULL) {
        printf("ERROR: Cannot open publication data file\n");
        return 0;
    }
    
    // Write data (format: year,type,faculty_short,title)
    fprintf(file, "%s\n", data);
    fclose(file);
    
    printf("SUCCESS: Publication data saved\n");
    return 1;
}