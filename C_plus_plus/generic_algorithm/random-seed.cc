#include <iostream>
#include <random>

using namespace std;

int main() {

	//定义一个随机数引擎
	default_random_engine e1;
	default_random_engine e2(217654);
	default_random_engine e3;
	e3.seed(32767);
	default_random_engine e4(32767);

	for (size_t i = 0; i < 8; ++i) {
		cout << "U(e1) is: " << e1() << " ";
		cout << "U(e2) is: " << e2() << " ";
		cout << "U(e3) is: " << e3() << " ";
		cout << "U(e4) is: " << e4() << " ";
		cout << endl;
	}

	return 0;
}
