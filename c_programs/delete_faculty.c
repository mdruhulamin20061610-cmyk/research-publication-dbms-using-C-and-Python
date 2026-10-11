// delete_faculty.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("ERROR: Usage: delete_faculty.exe <criteria> <value>\n");
        return 0;
    }

    char *criteria = argv[1];  // "ID" or "Name" or "Short Name"
    char *value    = argv[2];

    FILE *file = fopen("data_files/faculty.dat", "r");
    if (file == NULL) {
        printf("ERROR: Cannot open faculty data file\n");
        return 0;
    }

    // Read all lines into memory
    char lines[500][500];
    int  total = 0;
    while (fgets(lines[total], sizeof(lines[total]), file)) {
        // strip trailing newline
        lines[total][strcspn(lines[total], "\n")] = 0;
        if (strlen(lines[total]) > 0) total++;
    }
    fclose(file);

    // Find and remove matching line(s)
    int deleted = 0;
    FILE *out = fopen("data_files/faculty.dat", "w");
    if (out == NULL) {
        printf("ERROR: Cannot write to faculty data file\n");
        return 0;
    }

    for (int i = 0; i < total; i++) {
        char copy[500];
        strcpy(copy, lines[i]);

        // Parse: id,full_name,short_name,designation,research
        char id[50]    = "", full[100] = "", sname[30] = "";
        sscanf(copy, "%[^,],%[^,],%[^,]", id, full, sname);

        int match = 0;
        if (strcmp(criteria, "ID") == 0 && strcmp(id, value) == 0)         match = 1;
        if (strcmp(criteria, "Name") == 0 && strcmp(full, value) == 0)     match = 1;
        if (strcmp(criteria, "Short Name") == 0 && strcmp(sname, value) == 0) match = 1;

        if (match) {
            deleted++;
        } else {
            fprintf(out, "%s\n", lines[i]);
        }
    }
    fclose(out);

    if (deleted > 0) {
        printf("SUCCESS: %d faculty record(s) deleted\n", deleted);
        return 1;
    } else {
        printf("NOT_FOUND: No matching faculty record found\n");
        return 0;
    }
}
