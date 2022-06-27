#include <iostream>
#include <string>

using namespace std;

class Quote {
	public:
		Quote() = default;
		Quote(const string& book, double p) : bookNo(book), price(p) {}
		virtual Quote* clone() const { return  new Quote(*this); }
		virtual double net_price(size_t n) const;
		string isbn() const { return bookNo; }
		virtual ~Quote() = default;
	private:
		string bookNo;
	protected:
		double price = 0.0;

};

double Quote::net_price(size_t n) const
{
	return n * price;
}

class Bulk_quote : public Quote {
	public:
		Bulk_quote() = default;
		Bulk_quote(const string& s, double p, size_t n, double dis) :
			Quote(s, p), min_qty(n), discount(dis) { }
		Bulk_quote* clone() const { return new Bulk_quote(*this); }
		double net_price(size_t n) const override;
	private:
		size_t min_qty;
		double discount = 0.0;
};

double Bulk_quote::net_price(size_t cnt) const
{
	if (cnt < min_qty)
		return cnt * price;
	else {
		return cnt * (1 - discount) * price;
	}
}
