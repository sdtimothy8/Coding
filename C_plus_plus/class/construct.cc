#include <iostream>
#include <cstdio>
#include <string>

using namespace std;

// Class Definition

class ConstRef
{
	public:
		ConstRef(int ii);

	private:
		int i;
		const int ci;
		int &ri;
};

ConstRef::ConstRef(int ii):
	i(ii),
	ci(ii),
	ri(i)
{}

int main(int argc, char** argv)
{
	int value(10);
	ConstRef test(value);

	return 0;
}


