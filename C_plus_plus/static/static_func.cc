#include <iostream>

class Widget {
	public:
		Widget(int n) : nval(n) {}
		static void prints();
		void print();
	private:
		static int sval;
		int nval;
};

int Widget::sval = 88;

void Widget::print()
{
	std::cout << "print nval: " << nval << std::endl;
	std::cout << "print sval: " << sval << std::endl;
}

void Widget::prints()
{
	// static member function has no this pointer, so it can't
	// call none static data member and none static member function
	//std::cout << "prints nval: " << nval << std::endl; // Error!! nval is none static function
	std::cout << "prints sval: " << Widget::sval << std::endl; 
}

int main() {
	Widget w(99);
	w.print();
	w.prints();

	return 0;
}
