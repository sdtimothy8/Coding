#include <string>
#include <iostream>
#include <vector>

using std::string;

struct Data
{
	string	str;
	int		iVal;
};

class Account
{
public:
	void calculate() { amount += amount * interestRate; }
	static double rate(){ return interestRate; }
	static void rate(double);
private:
	string owner;
	double amount;
	static double interestRate;
	static double initRate(); 
};

double Account::initRate()
{
	interestRate = 0.006;
	return interestRate;
}

double Account::interestRate = initRate();

void Account::rate(double newRate)
{
	interestRate = newRate;
}

int main(int argc, char** argv)
{
	Data dVal = {"love", 5};
	return 0;
}
