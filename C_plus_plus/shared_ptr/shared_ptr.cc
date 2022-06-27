#include <memory>
#include <iostream>

using std::shared_ptr;
using std::unique_ptr;

int main(int argc, char** argv)
{
	shared_ptr<int> p1 = std::make_shared<int>(88);
	//shared_ptr<int> p2 = new int(99); /*Error*/
	shared_ptr<int> p3(new int(99));

	std::cout << *p1 << std::endl;
	std::cout << *p3 << std::endl;

	// unique_ptr用法
	unique_ptr<int> up1(new int(77));
	unique_ptr<int> up2(up1.release());
	std::cout << *up2 << std::endl;

	int *ptr = new int[10];
	int *pi = new int[0];
	std::cout << *pi << std::endl;
	

	return 0;
}
