#include <iostream>
#include <memory>
#include <string>


class Query_base {
	friend class Query;
	protected:
		using line_no = TextQuery::line_no;
		virtual ~Query_base() = default;
	private:
		virtual QueryResult eval(const TextQuery&) const = 0;
		virtual string rep() const = 0;
};


// Definition: WordQuery
class WordQuery : public Query_base {
	friend class Query;
	WordQuery(const string& s) : query_word(s) {}
	QueryResult eval(const TextQuery&) const { return t.query(query_word); }
	string rep() const { return query_word; }
};

// Definition: WordQuery
class NotQuery : public Query_base {
	friend Query operator~(const Query&);
	NotQuery(const Query& q) : query(q) { }
	// 定义继承而来的eval() 和 rep()
	string rep() const { return "~(" + query.rep() + ")"; }
	QueryResult eval(const TextQuery&) const;
	Query query;
};

Query operator~(const Query& operand)
{
	return shared_ptr<Query_base>(new NotQuery(operand));
}

QueryResult NotQuery::eval(const TextQuery& text) const
{
	auto result = query.eval(text);
	auto ret_lines = make_shared<set<line_no>>();
	auto beg = result.begin(), end = result.end();
	auto sz = result.get_file()->size();
	for (size_t n = 0; n != sz; ++n)
	{
		if (beg == end || *beg != n)
			ret_lines.insert(n);
		else if (beg != end)
			++beg;
	}
	return QueryResult(rep(), ret_lines, result.get_file());
}

// Definition BinaryQuery
class BinaryQuery : public Query_base {
protected:
	BinaryQuery(const Query& l, const Query& r, string s) : 
		lhs(l), rhs(r), opSym(s) { }
	string rep() const { return "(" + lhs.rep() + " " 
									+ opSym + " "
									+ rhs.rep() + ")"; }
	Query lhs, rhs;
	string opSym;
};

class AndQuery : public BinaryQuery {
	friend Query operator&(const Query& lhs, const Query& rhs);
	AndQuery(const Query& left, const Query& right) : BinaryQuery(left, right, "&") { }
	QueryResult eval(const TextQuery&) const;
};

Query operator&(const Query& lhs, const Query& rhs)
{
	return shared_ptr<Query_base>(new AndQuery(lhs, rhs));
}

class OrQuery : public BinaryQuery {
	friend Query operator|(const Query& lhs, const Query& rhs);
	OrQuery(const Query& left, const Query& right) : BinaryQuery(left, right, "|") { }
	QueryResult eval(const TextQuery&) const;
};

Query operator|(const Query& lhs, const Query& rhs)
{
	return shared_ptr<Query_base>(new OrQuery(lhs, rhs));
}

QueryResult OrQuery::eval(const TextQuery& text) const
{
	auto right = rhs.eval(text), left = lhs.eval(text);
	auto ret_lines = make_shared<set<line_no>>(left.begin(), left.end());
	ret_lines.insert(right.begin(), right.end());
	return QueryResult(rep(), ret_lines, left.get_file());
}
// Class Query
class Query {
	friend Query operator~(const Query&);
	friend Query operator&(const Query&, const Query&);
	friend Query operator|(const Query&, const Query&);
public:
	Query(const string&) : q(new WordQuery(s)) { }
	QueryResult eval(const TextQuery& t) { return q->eval(t); }
	string rep() { return q->rep(); }
private:
	Query(shared_ptr<Query_base> query) : q(query) {}
	shared_ptr<Query_base> q;
};
