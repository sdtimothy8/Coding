#include <string>
#include <iostream>
#include <vector>

using std::string;

class Base
{
public:
    static void statmem() {}

};

class Derived : public Base {
public:
    void f(const Derived&);
};

void Derived::f(const Derived& obj) {
    Base::statmem();
    Derived::statmem();
    obj.statmem(); // 通过Derived对象访问
    statmem(); //使用this指针访问
}

int main(int argc, char** argv)
{
	std::cout << "Hello, main()!!" << std::endl;

	return 0;
}
