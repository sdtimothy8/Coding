#include <iostream>
#include <string>

using std::string;

class Sales_data {
public:
	//Constructor
	Sales_data() = default;
	Sales_data(const string& s):
		bookNo(s),units_sold(0),revenue(0){ }
	Sales_data(const string& s, unsigned u, double r):
		bookNo(s),units_sold(u),revenue(u*r){ }

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

