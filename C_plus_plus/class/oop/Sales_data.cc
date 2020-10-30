#include <iostream>
#include <string>

using std::string;

class Sales_data {
public:
	//Constructor
	Sales_data() = default; //显示的让编译器生成合成构造函数
	Sales_data(const string& s):
		bookNo(s),units_sold(0),revenue(0){ }
	Sales_data(const string& s, unsigned u, double r):
		bookNo(s),units_sold(u),revenue(u*r){ }
	//重载拷贝运算符
	Sales_data& operator=(const Sales_data &rhs);
	//Deconstructor
	~Sales_data();

	//Member function
	string isbn() const { return bookNo; }	
	Sales_data&	combine(const Sales_data&);

private:
	double avg_price() const;
	//Data member
	string		bookNo;
	unsigned	units_sold;
	double		revenue;
};

Sales_data& Sales_data::operator=(const Sales_data &rhs)
{
	bookNo = rhs.bookNo;
	units_sold = rhs.units_sold;
	revenue = rhs.revenue;

	return *this;
}

Sales_data add( const Sales_data&, const Sales_data& );

Sales_data add( const Sales_data& lhs, const Sales_data& rhs )
{
	Sales_data sum = lhs;
	sum = sum.combine(rhs);
	return sum;
}

double Sales_data::avg_price() const 
{
	if ( units_sold )
		return revenue / units_sold;
	else
		return 0;
}

Sales_data& Sales_data::combine( const Sales_data& rhs)
{
	units_sold += rhs.units_sold;
	revenue += rhs.revenue;
	return *this;
}

Sales_data::~Sales_data()
{
	std::cout << "Class Data Member: " << std::endl;
	std::cout << "Book Num: " << bookNo << std::endl;
	std::cout << "Units Sold: " << units_sold << std::endl;
	std::cout << "Revenue: " << revenue << std::endl;
}

// Main function
int main(int argc, char** argv)
{
	Sales_data* p = new Sales_data("love", 10, 0.8);
	//Sales_data* p = nullptr;
	delete p;

	return 0;
}

