#include <iostream>
#include <string>

using std::string;

class Figure {
public:
    Figure() = default;
    Figure(double x, double y):
    x_size(x),
    y_size(y) { }
protected:
    double x_size;
    double y_size;
};

class Figure_2D : public Figure {
public:
    Figure_2D() = default;
    Figure_2D(double x, double y):
    Figure(x, y) {}
    virtual double area() = 0;
    virtual double pcrimeter() = 0;
};

class Circle : public Figure_2D {
public:
    Circle(double, double);
    virtual double area();
    virtual double pcrimeter();
};

class Rectangle: public Figure_2D {
public:
    Rectangle(double, double);
    virtual double area();
    virtual double pcrimeter();
};

int main() {

    return 0;
}