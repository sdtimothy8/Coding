/*
 * @lc app=leetcode.cn id=155 lang=cpp
 *
 * [155] 最小栈
 */

// @lc code=start
#include <iostream>
#include <stack>
#include <climits>
using std::stack;

class MinStack {
public:
    // 使用单栈+minValue的思路
    /** initialize your data structure here. */
    MinStack() :
    intStack(),
    minValue(INT_MAX)
    {
    }
    
    void push(int x) {
        // 注意相等的情况也要考虑进来x
        if (x <= minValue) {
            intStack.push(minValue); // 把之前的最小值也压进栈中
            minValue = x;
        }
        intStack.push(x);
    }
    
    void pop() {
        // 如果intStack和minStack栈顶元素相同，那么同时pop minStack栈。
        if (intStack.top() == minValue) {
            intStack.pop();
            minValue = intStack.top();
        }
        intStack.pop();
    }
    
    int top() {
        return intStack.top();
    }
    
    int getMin() {
        return minValue;
    }

private:
    stack<int>  intStack;
    int         minValue;
};

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack* obj = new MinStack();
 * obj->push(x);
 * obj->pop();
 * int param_3 = obj->top();
 * int param_4 = obj->getMin();
 */
// @lc code=end

