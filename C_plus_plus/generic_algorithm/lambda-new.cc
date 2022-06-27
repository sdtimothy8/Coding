#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

void fcn1()
{
	size_t v1 = 42;
	auto f = [v1] {return v1;};
	v1 = 0;
	auto j = f(); // j为42
	cout << "v1's value is: " << j << endl;
}

void fcn2()
{
	size_t v1 = 42;
	auto f = [&v1] {return v1;};
	v1 = 0;
	auto j = f(); // j为42
	cout << "v1's value is: " << j << endl;
}

int main() {
	fcn1();
	fcn2();

	return 0;
}
