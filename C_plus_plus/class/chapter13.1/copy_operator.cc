#include <iostream>
#include <string>
#include <vector>

using std::string;

class Sales_data {
public:
	//Constructor
	Sales_data() = default; //显示的让编译器生成合成构造函数
	Sales_data(const string& s):
		bookNo(s),units_sold(0),revenue(0){ }
	Sales_data(const string& s, unsigned u, double r):
		bookNo(s),units_sold(u),revenue(u*r){ }

	// Copy construtor
	Sales_data( const Sales_data &obj );

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

Sales_data::Sales_data( const Sales_data& obj ):
bookNo(obj.bookNo),
units_sold(obj.units_sold),
revenue(obj.revenue)
{
	std::cout << "Call copy constructor function!!" << std::endl;
}

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

Sales_data foo( Sales_data test )
{
	std::cout << "test foo:" << std::endl;
    return Sales_data();
}

// Main function
int main(int argc, char** argv)
{
	Sales_data local("love",10,0.8);
	Sales_data copy = local;
	//Sales_data* p = new Sales_data(local);
	//Sales_data* p = nullptr;
    //Sales_data obj(foo( *p ));
    /*
    std::cout << "======" << std::endl;	
    std::cout << "======" << std::endl;	
	std::vector<Sales_data> svec;
	svec.push_back(obj);
    */
	//delete p;
	return 0;
}

