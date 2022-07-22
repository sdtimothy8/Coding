#include <iostream>

class Widget {
	public:
		Widget(int v = 0) : _data(v), _pdata(new int(0)) {}
		Widget& operator=(const Widget& rhs);
		~Widget() { delete _pdata; }
	private:
		int _data;
		int* _pdata;
};

Widget&
Widget::operator=(const Widget& rhs)
{
	//考虑自我赋值问题和异常安全问题
	int* p = new int(*(rhs._pdata));
	delete _pdata;

	_pdata = p;
	_data = rhs._data;

	return *this;
}

int main()
{
	return 0;
}
