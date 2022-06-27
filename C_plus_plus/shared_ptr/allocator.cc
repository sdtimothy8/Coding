#include <memory>
#include <string>
#include <vector>
#include <iostream>

using std::allocator;
using std::string;
using std::vector;

int main(int argc, char** argv)
{
	int n = 10;
	allocator<string> alloc;
	auto const p = alloc.allocate(n);
	auto q = p;
	alloc.construct(q++, "love");
	alloc.construct(q++);
	alloc.construct(q++, 10, 'c');

	std::cout << *p << std::endl;

	//销毁构造的对象
	while (q != p)
		alloc.destroy(--q);
	//释放内存
	alloc.deallocate(p, n);

	//伴随算法的应用
	std::vector<int> ivec(10, 88);
	allocator<int> ialloc;
	auto pp = ialloc.allocate(ivec.size() * 2);
	auto qq = std::uninitialized_copy(ivec.begin(), ivec.end(), pp);
	std::uninitialized_fill_n(qq, ivec.size(), 99);

	return 0;
}
