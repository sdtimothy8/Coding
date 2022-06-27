#include <iostream>

class Base {
	public:
		virtual void f1(int) const;
		virtual void f2();
	private:
};


class Derived : public Base {
	public:
		void f1(int) const override;
		void f2() final;
	private:
};

class Derived2 : public Derived {
	public:
		void f2();

};


int main() {

	return 0;
}
