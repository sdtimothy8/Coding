#include <iostream>
#include <fstream>
#include <string>


using std::string;
using std::ifstream;
using std::fstream;

int main (int argc, char** argv)
{
	fstream input;
	input.open("test.txt", fstream::out | fstream::app);
	if (!input.is_open()) {
		std::cout << "Open file error!" << std::endl;
		return -1;
	}

	// 写入文件
	string text("believe god!!");
	input << text;

	// 读取文件
	string line;
	/*
	while (std::getline(input, line))
		std::cout << line << std::endl;
	*/
	
	/*
	while (input >> line)
		std::cout << line << std::endl;
	*/
	
	/*
	char buf[1024] = {0};
	while (input.getline(buf, sizeof(buf))) // 保证缓冲区足够大，每行的字符数如果超过缓冲区大小，循环会终止。
		std::cout << buf << std::endl;
		*/

	char c;
	while ((c = input.get()) != EOF)
		std::cout << c;
	std::cout << std::endl;

	input.close();

	return 0;
}

