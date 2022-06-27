#include <iostream>
#include <memory>

using namespace std;

//class Quote;

class Basket {
	public:
		void add_item(const Quote& sale)
		{ items.insert(shared_ptr<Quote>(sale.clone())); }
		double total_receipt(osstream&) const;
	private:
		static bool compare( const shared_ptr<Quote>& lhs, const shared_ptr<Quote>& rhs )
		{ return lhs->isbn() < rhs->isbn(); }
		multiset<shared_ptr<Quote>, decltype(compare)*> items{compare};
};

double Basket::total_receipt(ostream& os) const
{
	double sum = 0.0;

	for (auto iter = items.cbegin(); iter != items.cend(); iter = items.upper_bound(*iter))
	{
		//sum += print_total(os, **iter, items.count(*iter));
		sum += 1;
	}
	os << "Total Sale: " << sum << endl;
}

int main() {
	return 0;
}
