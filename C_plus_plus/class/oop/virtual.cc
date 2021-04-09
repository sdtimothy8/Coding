#include <iostream>
#include <string>

using std::string;

class Base {
public:
    string name() { return baseName; }
    virtual void print(std::ostream& os) { os << baseName; } 
    string pubName;
private:
    string baseName;
protected:
    string procName;
};


class Derived : public Base {
public:
    void print(std::ostream& os);
private:
    int i;
};

void Derived::print(std::ostream& os) {
    // 调用基类版本的虚函数
    Base::print(os);
    os << " " << i;
}

int main() {
    Derived dev;
    Base& bas = dev;
    bas.print(std::cout);
    std::cout << bas.pubName << std::endl;
    //std::cout << bas.procName << std::endl;

    return 0;
}