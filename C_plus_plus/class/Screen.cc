#include <string>
#include <vector>
#include <iostream>

using namespace std;

class Screen {
	friend class Window_mgr;
	public:
		typedef string::size_type pos;
		// Constructors
		Screen() = default;
		Screen(pos ht, pos wd, char c):
			height(ht), width(wd), contents(ht*wd, c){ }

		// Memberfunction
		inline char get(pos ht, pos wd) const;
		char get() const {return contents[cursor];}
		Screen& move(pos r, pos c); 
		Screen& set(char);
		Screen& set(pos, pos, char);
		void some_function() const;

	private:
		pos cursor = 0;
		pos height, width = 0;
		string contents;
		mutable size_t access_ctr;
};

inline Screen& Screen::move(pos r, pos c)
{
	pos row = r * width;
	cursor = row + c;
	return *this;
}

char Screen::get(pos r, pos c) const
{
	pos row = r * width;
	return contents[row + c];
}

void Screen::some_function() const
{
	++access_ctr;
}

inline Screen& Screen::set(char c)
{
	contents[cursor] = c;
	return *this;
}

inline Screen& Screen::set(pos r, pos col, char ch)
{
	contents[r*width + col] = ch;
	return *this;
}

// Class Window_mgr
class Window_mgr {
public:
	typedef std::vector<Screen>::size_type ScreenIndex;
	void clear(ScreenIndex);
private:
	std::vector<Screen> screens{Screen(24, 80, ' ')};

};

void Window_mgr::clear(ScreenIndex i)
{
	Screen& s = screens[i];
	s.contents = string(s.height * s.width, ' ');
}

int main(int argc, char* argv[])
{
	return 0;
}
