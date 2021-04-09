#include <cstdio>
#include <string>
#include <iostream>
#include <utility>
#include <vector>
#include <memory>
#include <set>

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
    virtual Quote* clone() const { return new Quote(*this); }

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
    Quote* clone() const = 0;
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
    virtual Quote* clone() const { return new Bulk_quote(*this); }
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
double print_total(std::ostream& os, Quote& item, size_t n) {
	double ret = item.net_price(n);
	os << "ISBN: " << item.isbn()
			  << " # sold: " << n
			  << " total due: " << ret << std::endl;
	return ret;
}

class Basket {
    void add_item(const std::shared_ptr<Quote>& sale) {
        items.insert(sale);
    }
    void add_item(const Quote& sale);
    // 打印每本书的总价和购物篮中所有书的总价
    double total_receipt(std::ostream&) const;
private:
    static bool compare(const std::shared_ptr<Quote>& lhs, 
                        const std::shared_ptr<Quote>& rhs) 
    { return lhs->isbn() < rhs->isbn(); }
    // multiset 保存多个报价，按照compare成员排序
    std::multiset<std::shared_ptr<Quote>, decltype(compare)*> items{compare};
};

void Basket::add_item(const Quote& sale) {
    // 这种用法有个问题：sale实际的类型可能不是Quote，而是Quote的派生类对象。
    //shared_ptr<Quote> ptr(new Quote(sale));
    //使用虚拷贝的方式
    items.insert(shared_ptr<Quote>(sale.clone()));
}

double Basket::total_receipt(std::ostream& os) const {
    double sum = 0.0;
    for (auto iter = items.cbegin(); iter != items.cend(); 
         iter = items.upper_bond(*iter)) {
             sum += print_total(os, **iter, items.count(*iter));
         }
    os << "Total Sale: " << sum << std::endl;
    return sum; 
}

int main(int argc, char** argv)
{
    vector<std::shared_ptr<Quote>> basket;
    basket.push_back(make_shared<Quote>("100-01", 8.8));
	basket.push_back(make_shared<Bulk_quote>("100-02", 9.9, 10, 0.2));

    std::cout << basket.back()->net_price(20) << std::endl;
	return 0;
}
