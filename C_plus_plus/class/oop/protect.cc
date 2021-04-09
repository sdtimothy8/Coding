#include <iostream>
#include <string>

using std::string;

class Base {
public:
    void pub_mem() { } //public 成员
    void memfcn(Base& b) { b = *this; }
protected:
    int proc_mem;   // protected 成员
private:
    char priv_mem;  // private 成员
};

class Pub_Derv : public Base {
public:
    void memfcn(Base& b) { b = *this; }
    int f() { return proc_mem; }
    //char g() { return priv_mem; } // Error:
};

class Priv_Derv : private Base {
    int f1() const { return proc_mem; } // right
    void memfcn(Base& b) { b = *this; }
};

int main() {
    Base b1;
    Pub_Derv d1;
    Priv_Derv d2;
    d1.pub_mem();
    b1 = d1;
    // b1 = d2;    //错误：不允许 
    // d2.pub_mem(); //错误：pub_mem()在派生类中是private的
    return 0;
}