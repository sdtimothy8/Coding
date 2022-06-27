#include <stdio.h>

char* fgets(char* line, int maxline, FILE* fp)
{
	int c;
	char* cs = line;
	while (--maxline > 0 && (c = getc(fp)) != EOF) {
		if ((*cs++ = c) == '\n')
			break;
	}
	*cs = '\0';

	return (cs == line && c == EOF) NULL : line;
}
