#include <iostream>
#include <string>
#include <memory>
#include <vector>

using namespace std;

class Sales_data {
public:
	//Constructor
	Sales_data() = default;
	Sales_data(const string& s):
		bookNo(s),units_sold(0),revenue(0){ }
	Sales_data(const string& s, unsigned u, double r):
		bookNo(s),units_sold(u),revenue(u*r){ }
	//重载拷贝运算符
	Sales_data& operator=(const Sales_data &rhs);
	//析构函数
	~Sales_data() = default;

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

void testFunc()
{
	Sales_data *p = new Sales_data;
	auto p2 = make_shared<Sales_data>();
	Sales_data item(*p);
	vector<Sales_data> vec;
	vec.push_back(*p2);
	delete p;
}

// Main function
int main(int argc, char** argv)
{

	return 0;
}

