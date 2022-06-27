#include <stdio.h>
#include <ctype.h>

int main() {
	int c; /*这里使用int而不是char类型，因为EOF的值为-1*/
	while ((c = getchar()) != EOF)
		putchar(tolower(c));
	return 0;
}
