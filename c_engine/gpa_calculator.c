/* 
 * gpa_calculator.c - C Language Engine for EduPulse Academic System
 * Calculates weighted GPA and evaluates attendance risk flags.
 */

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 6) {
        printf("Error: Missing arguments. Usage: gpa_calculator physics maths chemistry comp_sci attendance\n");
        return 1;
    }

    double physics = atof(argv[1]);
    double maths = atof(argv[2]);
    double chemistry = atof(argv[3]);
    double comp_sci = atof(argv[4]);
    double attendance = atof(argv[5]);

    double avg_score = (physics + maths + chemistry + comp_sci) / 4.0;
    double gpa = (avg_score / 100.0) * 4.0;

    int risk_flag = 0; // 0 = LOW, 1 = MEDIUM, 2 = HIGH
    if (avg_score < 60.0 || attendance < 75.0) {
        risk_flag = 2; // HIGH RISK
    } else if (avg_score < 75.0 || attendance < 85.0) {
        risk_flag = 1; // MEDIUM RISK
    }

    // Output JSON-formatted string for Python to read easily
    printf("{\"average\": %.2f, \"gpa\": %.2f, \"risk_flag\": %d}\n", avg_score, gpa, risk_flag);
    return 0;
}
