#include <iostream>
#include <random>

using namespace std;

int main() {
	//定义一个随机数分布对象
	uniform_int_distribution<unsigned> u(0,100);
	//定义一个随机数引擎
	default_random_engine e;
	for (size_t i = 0; i < 10; ++i)
		cout << u(e) << " ";
	cout << endl;

	cout << "max e: " << e.max() << " min e: " << e.min() << endl;

	return 0;
}
