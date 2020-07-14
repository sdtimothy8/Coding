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
	//Account(const string &s, double val):
	//	owner(s), amount(val){}
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

// 在类外给static成员进行初始化
double Account::interestRate = initRate();
//double Account::interestRate = 0.06;

void Account::rate(double newRate)
{
	interestRate = newRate;
}

int main(int argc, char** argv)
{
	double r = 0;
	// 使用作用域运算符直接访问静态成员
	r = Account::rate();
	std::cout << "Current rate is: " << r << std::endl;
	Account ac1 = Account();
	Account *ac2 = &ac1;
	r = ac1.rate(); //像调用普通成员函数一样调用静态成员函数
	r = ac2->rate();
	std::cout << "Current rate is: " << r << std::endl;

	return 0;
}
