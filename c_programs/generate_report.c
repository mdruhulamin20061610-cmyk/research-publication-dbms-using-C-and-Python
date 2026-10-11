// generate_report.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: generate_report.exe <report_type>\n");
        return 0;
    }
    
    char *report_type = argv[1];
    
    if (strcmp(report_type, "faculty_info") == 0) {
        printf("\n------------- FACULTY INFORMATION -------------\n");
        printf("ID       Name                      Short  Designation           Research\n");
        printf("--------------------------------------------------------------------------\n");

        FILE *file = fopen("data_files/faculty.dat", "r");
        if (file) {
            char line[500];
            int count = 0;
            while (fgets(line, sizeof(line), file)) {
                char id[20], name[100], sname[20], desig[50], research[200];
                if (sscanf(line, "%[^,],%[^,],%[^,],%[^,],%[^\n]", id, name, sname, desig, research) == 5) {
                    printf("%-8s %-25s %-6s %-21s %s\n", id, name, sname, desig, research);
                    count++;
                }
            }
            printf("--------------------------------------------------------------------------\n");
            printf("Total Faculty: %d\n", count);
            fclose(file);
        }
    }
    else if (strcmp(report_type, "year_pub") == 0) {
        printf("\n------------- YEAR-WISE PUBLICATION COUNT -------------\n");
        printf("Year     Number of Publications\n");
        printf("--------------------------------\n");
        
        // Read publication.dat and count by year (REMOVED ../)
        FILE *file = fopen("data_files/publication.dat", "r");
        if (file) {
            char line[500];
            int year_counts[51] = {0};  // 2000-2050
            int min_year = 2050, max_year = 2000;
            
            while (fgets(line, sizeof(line), file)) {
                int year;
                sscanf(line, "%d,", &year);
                if (year >= 2000 && year <= 2050) {
                    year_counts[year - 2000]++;
                    if (year < min_year) min_year = year;
                    if (year > max_year) max_year = year;
                }
            }
            
            for (int i = min_year - 2000; i <= max_year - 2000; i++) {
                if (year_counts[i] > 0) {
                    printf("%-9d %d\n", 2000 + i, year_counts[i]);
                }
            }
            fclose(file);
        }
        printf("--------------------------------\n");
    }
    else if (strcmp(report_type, "type_summary") == 0) {
        printf("\n------------- PUBLICATION TYPE SUMMARY -------------\n");
        printf("Type             Count\n");
        printf("-----------------------------------\n");
        
        // REMOVED ../
        FILE *file = fopen("data_files/publication.dat", "r");
        if (file) {
            char line[500];
            int journal = 0, conference = 0, review = 0, other = 0;
            
            while (fgets(line, sizeof(line), file)) {
                char type[30];
                sscanf(line, "%*[^,],%[^,]", type);
                if (strcmp(type, "Journal") == 0) journal++;
                else if (strcmp(type, "Conference") == 0) conference++;
                else if (strcmp(type, "Review") == 0) review++;
                else other++;
            }
            
            printf("Journal          %d\n", journal);
            printf("Conference       %d\n", conference);
            printf("Review           %d\n", review);
            printf("Other            %d\n", other);
            fclose(file);
        }
        printf("-----------------------------------\n");
    }
    else if (strcmp(report_type, "faculty_pub") == 0) {
        printf("\n------------- FACULTY-WISE PUBLICATIONS -------------\n");
        printf("Faculty   Number of Publications\n");
        printf("--------------------------------\n");
        
        // REMOVED ../
        FILE *pub_file = fopen("data_files/publication.dat", "r");
        FILE *fac_file = fopen("data_files/faculty.dat", "r");
        if (pub_file && fac_file) {
            // Simple count using array, assume max 100 faculty
            char fac_shorts[100][20];
            int counts[100] = {0};
            int num_fac = 0;
            
            char fac_line[500];
            while (fgets(fac_line, sizeof(fac_line), fac_file)) {
                char short_name[20];
                sscanf(fac_line, "%*[^,],%*[^,],%[^,]", short_name);
                strcpy(fac_shorts[num_fac], short_name);
                num_fac++;
            }
            
            char pub_line[500];
            while (fgets(pub_line, sizeof(pub_line), pub_file)) {
                char faculty[20];
                sscanf(pub_line, "%*[^,],%*[^,],%[^,]", faculty);
                for (int i = 0; i < num_fac; i++) {
                    if (strcmp(faculty, fac_shorts[i]) == 0) {
                        counts[i]++;
                        break;
                    }
                }
            }
            
            for (int i = 0; i < num_fac; i++) {
                printf("%-9s %d\n", fac_shorts[i], counts[i]);
            }
            
            fclose(pub_file);
            fclose(fac_file);
        }
        printf("--------------------------------\n");
    }
    else if (strcmp(report_type, "dept_stats") == 0) {
        printf("\n------------- DEPARTMENT STATISTICS -------------\n");
        
        int total_fac = 0, total_pub = 0;
        
        // REMOVED ../
        FILE *fac_file = fopen("data_files/faculty.dat", "r");
        if (fac_file) {
            char line[500];
            while (fgets(line, sizeof(line), fac_file)) total_fac++;
            fclose(fac_file);
        }
        
        FILE *pub_file = fopen("data_files/publication.dat", "r");
        if (pub_file) {
            char line[500];
            while (fgets(line, sizeof(line), pub_file)) total_pub++;
            fclose(pub_file);
        }
        
        printf("Total Faculty: %d\n", total_fac);
        printf("Total Publications: %d\n", total_pub);
        if (total_fac > 0) printf("Average Publications per Faculty: %.2f\n", (float)total_pub / total_fac);
        printf("--------------------------------\n");
    }
    
    return 1;
}