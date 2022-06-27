#include <stdio.h>

int main(int argc, char** argv)
{
	int i;
	FILE* fp = NULL;
	for (i = 1; i < argc; ++i) {
		if ((fp = fopen(argv[i], "r")) == NULL) {
			fprintf(stderr, "open file %s error!\n", argv[i]);
			//exit(-1);
		} else {
			int c;
			while ((c = getc(fp)) != EOF)
				putc(c, stdout);
		}
		fclose(fp);
	}
	return 0;
}
