#include <stdarg.h>
#include <stdio.h>




void minprintf(char* fmt, ...)
{
	va_list ap; /* 依次指向每个无名参数 */
	char *p, *sval;
	int ival;
	double dval;

	va_start(ap, fmt);
	for (p = fmt; *p; p++) {
		if (*p != '%') {
			putchar(*p);
			continue;
		}
		switch (*++p) {
			case 'd':
				ival = va_arg(ap, int);
				printf("%d", ival);
				break;
			case 'f':
				dval = va_arg(ap, double);
				printf("%f", dval);
				break;
			case 's':
				for (sval = va_arg(ap, char*);*sval;sval++)
					putchar(*sval);
				break;
			default:
				putchar(*p);
				break;
		}
	}
	va_end(ap);
}

int main() {
	int ival = 2022;
	minprintf("print the int val %d\n", ival);
	return 0;
}
