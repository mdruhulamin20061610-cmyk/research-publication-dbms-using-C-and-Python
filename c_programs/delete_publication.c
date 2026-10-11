// delete_publication.c

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    if (argc < 3) {
        printf("ERROR: Usage: delete_publication.exe <criteria> <value>\n");
        return 0;
    }

    char *criteria = argv[1];
    char *value    = argv[2];

    FILE *file = fopen("data_files/publication.dat", "r");
    if (file == NULL) {
        printf("ERROR: Cannot open publication data file\n");
        return 0;
    }

    char lines[1000][500];
    int total = 0;

    // Read all lines
    while (fgets(lines[total], sizeof(lines[total]), file)) {
        lines[total][strcspn(lines[total], "\n")] = '\0';
        if (strlen(lines[total]) > 0) {
            total++;
        }
    }
    fclose(file);

    int deleted = 0;

    FILE *out = fopen("data_files/publication.dat", "w");
    if (out == NULL) {
        printf("ERROR: Cannot write to publication data file\n");
        return 0;
    }

    for (int i = 0; i < total; i++) {

        char copy[500];
        strcpy(copy, lines[i]);

        // Format: year,type,faculty_short,title
        char year[10] = "", type[30] = "", faculty[30] = "", title[300] = "";

        sscanf(copy, "%[^,],%[^,],%[^,],%[^\n]", year, type, faculty, title);

        int match = 0;

        if (strcmp(criteria, "Year") == 0 && strcmp(year, value) == 0) {
            match = 1;
        }

        if (strcmp(criteria, "Type") == 0 && strcmp(type, value) == 0) {
            match = 1;
        }

        if (strcmp(criteria, "Faculty Short Name") == 0 && strcmp(faculty, value) == 0) {
            match = 1;
        }

        if (strcmp(criteria, "Title Keyword") == 0 && strstr(title, value)) {
            match = 1;
        }

        if (match) {
            deleted++;
        } else {
            fprintf(out, "%s\n", lines[i]);
        }
    }

    fclose(out);

    if (deleted > 0) {
        printf("SUCCESS: %d publication record(s) deleted\n", deleted);
        return 1;
    } else {
        printf("NOT_FOUND: No matching publication record found\n");
        return 0;
    }
}