#include <string>
#include <iostream>
#include <vector>

using namespace std;

class HasPtr
{
	public:
		HasPtr(const string &s = string()):
			ps(new string(s)),i(0){}
		//这个类需要析构函数，那它也需要拷贝构造函数
		~HasPtr(){ delete ps; }

	private:
		string *ps;
		int i;
};

int main(int argc, char** argv)
{
	HasPtr test;
	HasPtr test1 = test;
	return 0;
}
