#include <iostream>
// Point class with no virtual deconstructor
class Point {
	public:
		Point(int x = 0, int y = 0) :
			_x(x),
			_y(y) {}
		~Point() {  }
		void print() {}
	private:
		int _x;
		int _y;
};

// Point class with no virtual deconstructor
class Pointv {
	public:
		Pointv(int x = 0, int y = 0) :
			_x(x),
			_y(y) {}
		virtual ~Pointv() {  }
		virtual void print() { }
	private:
		int _x;
		int _y;
};


int main() {
	Point p1(4, 5);
	// 8 Bytes
	std::cout << "The size of the Class Point: " << sizeof(Point) << std::endl;
	std::cout << "The size of the Objec p1: " << sizeof(p1) << std::endl;

	Pointv p2(4, 5);
	// 16 Bytes: int 4 + int 4 + vptr pointer 8
	std::cout << "The size of the Class Pointv: " << sizeof(Pointv) << std::endl;
	std::cout << "The size of the Objec p2: " << sizeof(p2) << std::endl;
	return 0;
}
