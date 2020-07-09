#include <iostream>
#include <cstdio>
#include <string>

using namespace std;

// Class Definition

class Test
{
	public:
		Test() { cout << "Constructor: Test()" << endl; }
		//Copy constors
		Test(const Test &t) { cout << "Copy constructor: Test(const Test &t)" << endl;}
		Test& operator= (const Test &rhs) {cout << "Copy = operator: =" << endl;}
		~Test() { cout << "Deconstructor：~Test()" << endl; }

	private:
		int value;
};

Test global;

Test func1(Test t)
{
	cout << "---------begin function call------------" << endl;
	//Test t11(t);
	Test local = t, *heap = new Test(global);
	*heap = local; 
	Test ta[4] = {local, *heap};

	cout << "---------end function call------------" << endl;

	return  *heap;
}

int main(int argc, char** argv)
{
	Test tt;
	func1(tt);
	cout << "---------main after call func1------------" << endl;

	return 0;
}


