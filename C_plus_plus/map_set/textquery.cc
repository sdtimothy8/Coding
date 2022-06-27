#include <map>
#include <vector>
#include <set>
#include <memory>
#include <iostream>
#include <string>
#include <utility>

using std::vector;
using std::pair;
using std::map;
using std::set;
using std::ifstream;
using std::ofstream;
using std::ostream;
using std::string;
using std::shared_ptr;

class QueryResult {

	public:
		typedef set<int>		IntSet;
		typedef vector<string> 	StrVec;

		QueryResult(string& word, shared_ptr<IntSet> l, shared_ptr<StrVec> f):
			_word(word), _lines(l), _file(f) {  }
		ostream& print(ostream& outfile);
	private:
		string				_word;
		shared_ptr<IntSet>	_lines;
		shared_ptr<StrVec>	_file;	
		
};

class TextQuery {
	public:
		typedef vector<string> 	StrVec;
		typedef set<int>		IntSet;
		typedef pair<string, shared_ptr<set<int>>> StrSetPair;
		typedef map<string, shared_ptr<set<int>>> StrSetMap;

		TextQuery(ifstream& infile) { buildtext(infile); }
		QueryResult query(const string& s);

	private:
		void buildtext(ifstream &infile);

		shared_ptr<StrVec>		_file;
		StrSetMap 				_wordmap;
};

ostream& print(ostream& outfile, QueryResult& qr)
{
	qr.print(outfile);
	return outfile;
}

void runQueries(ifstream& infile)
{
	//infile是一个ifstream指向我们的输入文件
	TextQuery tq(infile);

	while (true) {
		std::cout << "enter word to look for, or q to quit: ";
		string word;
		if (!(std::cin >> word) || word != "q") break;
		QueryResult qr = tq.query(word);
		print(std::cout, qr);
	}
}

int main(int argc, char** argv)
{
	return 0;
}
