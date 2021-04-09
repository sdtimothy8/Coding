#include <cstdio>
#include <string>
#include <iostream>
#include <utility>
#include <vector>
#include <memory>

using std::pair;
using std::vector;
using std::shared_ptr;
using std::make_shared;

class Quote
{
public:
	Quote() = default;
	Quote(const std::string& book, double sales_price):
	bookNo(book),price(sales_price) {}
	std::string isbn() const { return bookNo; }
	virtual double net_price(std::size_t n) const;
	virtual ~Quote() = default;
	//定义与派生类同名的非虚函数
	void print() const { std::cout << "Quote: print()!!" << std::endl; }

private:
	std::string bookNo;
protected:
	double price = 0.0;
};

double Quote::net_price(std::size_t cnt) const {
	return cnt * price;
}

class Disc_quote : public Quote {
public:
    Disc_quote() = default;
    Disc_quote(const std::string& book, double price, std::size_t qty, double disc) :
    Quote(book, price),
    quantity(qty),
    discount(disc) { }
    double net_price(std::size_t cnt) const = 0;
    pair<std::size_t, double> discount_policy() const { return {quantity, discount}; }
protected:
    std::size_t quantity = 0;
    double discount = 0.0;
};

// Derived classisc
class Bulk_quote : public Disc_quote {
public:
	Bulk_quote() = default;
	Bulk_quote(const std::string& book, double p, std::size_t qty, double dis):
    Disc_quote(book, p, qty, dis) { }
	double net_price(std::size_t n) const override;
	//定义与派生类同名的非虚函数
	void print() const { std::cout << "Bulk_quote: print()!!" << std::endl; }
};

// Derived class
// 当购买数量超过一定的限量时原价销售
class Bulk_quote2 : public Disc_quote {
public:
	Bulk_quote2() = default;
	Bulk_quote2(const std::string& book, double p, std::size_t qty, double dis):
    Disc_quote(book, p, qty, dis) { }
	double net_price(std::size_t) const;
};

double Bulk_quote::net_price(std::size_t cnt) const {
	if (cnt < quantity) 
		return cnt * price;
	else
		return cnt * price * (1 - discount);

	// 使用基类的私有数据成员,Error!
	//std::cout << bookNo << std::endl;
}

double Bulk_quote2::net_price(std::size_t cnt) const {
	if (cnt >= quantity)
		return cnt * price;
	else
		return cnt * price * (1 - discount);
}

// 动态绑定
double print_total(const Quote& item, size_t n) {
	double ret = item.net_price(n);
	std::cout << "ISBN: " << item.isbn()
			  << " # sold: " << n
			  << " total due: " << ret << std::endl;
	return ret;
}


int main(int argc, char** argv)
{
    vector<std::shared_ptr<Quote>> basket;
    basket.push_back(make_shared<Quote>("100-01", 8.8));
	basket.push_back(make_shared<Bulk_quote>("100-02", 9.9, 10, 0.2));

    std::cout << basket.back()->net_price(20) << std::endl;
	return 0;
}
