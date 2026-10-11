// faculty_info.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    // REMOVED ../
    FILE *file = fopen("data_files/faculty.dat", "r");
    if (file == NULL) {
        printf("No faculty records found.\n");
        return 0;
    }
    
    char line[500];
    int count = 0;
    
    printf("\n==================== FACULTY INFORMATION ====================\n");
    printf("Faculty ID   Full Name                       Short Name   Designation             Research Area\n");
    printf("------------------------------------------------------------------------------------\n");
    
    while (fgets(line, sizeof(line), file)) {
        // Remove newline
        line[strcspn(line, "\n")] = 0;
        
        // Parse CSV: id,full,short,desig,research
        char *token = strtok(line, ",");
        int col = 0;
        
        while (token != NULL) {
            switch(col) {
                case 0: printf("%-12s ", token); break;  // ID
                case 1: printf("%-31s ", token); break;  // Full Name
                case 2: printf("%-12s ", token); break;  // Short Name
                case 3: printf("%-23s ", token); break;  // Designation
                case 4: printf("%s", token); break;      // Research
            }
            token = strtok(NULL, ",");
            col++;
        }
        printf("\n");
        count++;
    }
    
    printf("------------------------------------------------------------------------------------\n");
    printf("Total Faculty: %d\n", count);
    fclose(file);
    return 1;
}