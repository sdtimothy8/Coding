#include <iostream>
#include <string>

using namespace std;

class Quote {
	public:
		Quote() = default;
		Quote(const string& book, double p) : bookNo(book), price(p) {}
		virtual double net_price(size_t n) const;
		string isbn() const { return bookNo; }
		virtual ~Quote() = default;
	private:
		string bookNo;
	protected:
		double price = 0.0;

};

class Disc_quote : public Quote {
	public:
		Disc_quote() = default;
		Disc_quote(const string& s, double p, size_t qty, double disc) :
			Quote(s, p), min_qty(qty), discount(disc) { }
		double net_price(size_t cnt) const = 0;
	protected:
		size_t min_qty = 0;
		double discount = 0.0;
};

double Quote::net_price(size_t n) const
{
	return n * price;
}

class Bulk_quote : public Disc_quote {
	public:
		Bulk_quote() = default;
		Bulk_quote(const string& s, double p, size_t n, double dis) :
			Disc_quote(s, p, n, dis) { }
		double net_price(size_t n) const override;
};

double Bulk_quote::net_price(size_t cnt) const
{
	if (cnt < min_qty)
		return cnt * price;
	else {
		return cnt * (1 - discount) * price;
	}
}

int main() {
	Quote q;
	Disc_quote dq;
	return 0;
}
