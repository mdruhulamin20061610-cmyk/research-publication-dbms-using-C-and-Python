// save_data.c
// Records are written to the files as soon as they are added, so here we
// just check that both data files are there and report how many records are saved.
#include <stdio.h>

int main() {
    char line[500];
    int fac = 0, pub = 0;

    FILE *f1 = fopen("data_files/faculty.dat", "r");
    FILE *f2 = fopen("data_files/publication.dat", "r");

    if (f1 == NULL || f2 == NULL) {
        printf("ERROR: Data file missing, data could not be saved\n");
        return 0;
    }

    while (fgets(line, sizeof(line), f1)) fac++;
    while (fgets(line, sizeof(line), f2)) pub++;
    fclose(f1);
    fclose(f2);

    printf("SUCCESS: %d faculty and %d publication records saved\n", fac, pub);
    return 1;
}
