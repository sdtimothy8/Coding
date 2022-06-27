#include <stdio.h>
#include <string.h>

char *mfgets(char* line, int maxline, FILE* fp)
{
	int c;
	char* cs = line;
	int count = 0;
	while ((c = getc(fp)) != EOF) {
		if (++count < maxline)
			*cs++ = c;
		else
			break;
		if (c == '\n')
			break;
	}
	*cs = '\0';
	return (c == EOF || cs == line)? NULL : line;
}

char *mfgets_standard(char* line, int maxline, FILE* fp)
{
	register int c;
	register char* cs;
	cs = line;
	while (--maxline > 0 && (c = getc(fp)) != EOF) {
		if ((*cs++ = c) == '\n')
			break;
	}
	*cs = '\0';

	return (c == EOF && cs == line)? NULL : line;
}

int getline(char* line, int max)
{
	if (fgets(line, max, stdin) == NULL)
		return 0;
	else
		return strlen(line);
}

int main(int argc, char** argv)
{
	char line[1024];
	FILE* fp;
	if((fp = fopen("test.txt", "r")) == NULL) {
		fprintf(stderr, "Open file error!\n");
		exit(-1);
	}
	mfgets_standard(line, 1024, fp);
	printf("Output line: %s\n", line);
	fclose(fp);
	
	return 0;
}
