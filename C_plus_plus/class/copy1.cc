#include <iostream>
#include <vector>
using namespace std;

class obj
{
    public :
        obj(int val):_value(val) { cout << ">> create obj " << endl; }
        obj(const obj& other) {
			cout << ">> copy create obj " << endl; 
		}
	private:
		int _value;
 };

vector<obj> foo()
{
        vector<obj> c;
		c.reserve(8);
		obj t(8);
        c.push_back(t);
		cout << "---- 222222 ----" << endl;
		cout << "222 c's capacity() is: " << c.capacity() << endl;
        c.push_back(t);
		cout << "---- 333333 ----" << endl;
		cout << "333 c's capacity() is: " << c.capacity() << endl;
        c.push_back(t);
		cout << "---- 444444 ----" << endl;
        c.push_back(t);
		cout << "444 c's capacity() is: " << c.capacity() << endl;
		
		cout << "---- exit foo ----" << endl;
	    return c;
 }

int main()
{
	vector<obj> k;
	k = foo();
}
