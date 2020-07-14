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
	//重载复合赋值运算符
	Sales_data& operator+=(const Sales_data &rhs);

	//Member function
	string isbn() const { return bookNo; }	
	unsigned getUnitsSold() const {return units_sold;}
	double getRevenue() const {return revenue;}
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

Sales_data &Sales_data::operator+=(const Sales_data &rhs)
{
	units_sold += rhs.units_sold;
	revenue = rhs.revenue;

	return *this;
}

bool
operator==(const Sales_data &lhs, const Sales_data &rhs)
{
	return ( lhs.isbn() == rhs.isbn() &&
			 lhs.getUnitsSold() == rhs.getUnitsSold() &&
			 lhs.getRevenue() == rhs.getRevenue()
			);
}

bool
operator!=(const Sales_data &lhs, const Sales_data &rhs)
{
	return !(lhs == rhs);
}

Sales_data operator+(const Sales_data &lhs, const Sales_data &rhs)
{
	auto sum = lhs;
	sum += rhs;

	return sum;
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

// Main function
int main(int argc, char** argv)
{
	
	return 0;
}

