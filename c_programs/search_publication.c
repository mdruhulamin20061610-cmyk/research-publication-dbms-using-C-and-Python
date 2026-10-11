// search_publication.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Publication {
    char title[200];
    char authors[100];
    int year;
    char type[30];
    char venue[100];
    char faculty_id[20];
};

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: search_publication.exe <criteria> <term>\n");
        return 0;
    }
    
    char *criteria = argv[1];
    char *term = argv[2];
    
    // REMOVED ../
    FILE *file = fopen("data_files/publication.dat", "r");
    if (file == NULL) {
        printf("No publication records found.\n");
        return 0;
    }
    
    // If searching by faculty name, find that faculty's short name in faculty.dat
    // (publication.dat only stores the short name, e.g. MHK)
    char wanted_short[20] = "";
    if (strcmp(criteria, "Faculty Name") == 0) {
        FILE *ffile = fopen("data_files/faculty.dat", "r");
        if (ffile) {
            char fline[500];
            while (fgets(fline, sizeof(fline), ffile)) {
                char id[20], full_name[100], short_name[20];
                sscanf(fline, "%[^,],%[^,],%[^,]", id, full_name, short_name);
                if (strstr(full_name, term)) {
                    strcpy(wanted_short, short_name);
                    break;
                }
            }
            fclose(ffile);
        }
    }

    printf("\n========== SEARCH RESULTS: %s = '%s' ==========\n", criteria, term);
    printf("Year  Type        Faculty   Title\n");
    printf("-----------------------------------------------------------\n");
    
    char line[500];
    int found = 0;
    
    while (fgets(line, sizeof(line), file)) {
        // Parse publication data
        char year_str[10], type[30], faculty[20], title[200];
        sscanf(line, "%[^,],%[^,],%[^,],%[^\n]", year_str, type, faculty, title);
        
        // Search based on criteria
        int match = 0;
        if (strcmp(criteria, "Faculty Name") == 0) {
            if (strstr(faculty, term)) match = 1;                                       // typed short name
            if (wanted_short[0] != '\0' && strcmp(faculty, wanted_short) == 0) match = 1; // typed full name
        }
        if (strcmp(criteria, "Year") == 0 && strcmp(year_str, term) == 0) match = 1;
        if (strcmp(criteria, "Publication Type") == 0 && strcmp(type, term) == 0) match = 1;
        if (strcmp(criteria, "Research Topic") == 0 && strstr(title, term)) match = 1;
        
        if (match) {
            printf("%-6s %-11s %-9s %s\n", year_str, type, faculty, title);
            found++;
        }
    }
    
    printf("-----------------------------------------------------------\n");
    printf("Total Found: %d\n", found);
    fclose(file);
    return 1;
}