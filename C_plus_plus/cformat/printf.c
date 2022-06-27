#include <stdio.h>

int main() {
	int a = 100;
	int b = 88;
	int c = 20220527;
	double d = 31415.926788;
	char s[] = "hello, world";

	printf("%-8d|%-8.4d|\n", a, c);
	printf("print %%\n");
	printf("%e\n", d);
	printf("%s, sizeof() is %d\n", s, sizeof(s));
	printf(":%10s:\n", s);
	printf(":%.10s:\n", s);
	printf(":%.15s:\n", s);
	printf(":%-15s:\n", s);
	printf(":%15s:\n", s);
	printf(":%15.10s:\n", s);
	int count = printf(":%-15.10s:\n", s);
	printf("printf output %d chars\n", count);
	return 0;
}
