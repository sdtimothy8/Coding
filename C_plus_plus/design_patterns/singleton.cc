#include <memory>
#include <iostream>

class Singleton {
	public:
		static Singleton* getInstance();
		//static Singleton* _ginstance;
		void print() { std::cout << "I am a singleton object!!" <<
								 << test << std::endl; }
	private:
		Singleton( int d = 0);
		~Singleton() { delete _ginstance; }

		static Singleton* _ginstance;
		static int test;
		int _data;
};

Singleton::Singleton(int d)
	: _data(d)
{}


Singleton* Singleton::getInstance()
{
	if (nullptr == _ginstance) 
		_ginstance = new Singleton();

	return _ginstance;
}

Singleton* Singleton::_ginstance = nullptr;
Singleton* Singleton::test = 88;

int main() {
	Singleton::getInstance()->test = 99;
	Singleton::getInstance()->print();
	//Singleton t(88);

	return 0;
}


