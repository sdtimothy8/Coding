#include <stdio.h>

int main() {
	double sum, v;
	char line[1024];

	sum = 0;
	while (scanf("%lf", &v) == 1)
		printf("\t%.2f\n", sum += v);

	int day, mouth, year;
	char mothname[20];
	while (getline(line, sizeof(line)) > 0) {
		if (sscanf(line, "%d %s %d", &day, mothname, &year ) == 3)
			printf("valid: %s\n", line);
		else if (sscanf(line, "%d/%d/%d", &mouth, &day, &year ) == 3)
			printf("valid: %s\n", line);
		else
			printf("invalid format: %s\n", line);
	}
	return 0;
}
