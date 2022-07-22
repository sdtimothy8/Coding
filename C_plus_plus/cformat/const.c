#include <string.h>
#include <stdio.h>

int main() {
	enum boolen { NO, YES };
	enum months { JAN = 1, FEB, MAR, APR, MAY };
	int ival = 555l;

	printf("The enum values is: %d\\\n", FEB);
	printf("The int value is %d\n", ival);
	return 0;
}
