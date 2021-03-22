/*
 * @lc app=leetcode.cn id=225 lang=cpp
 *
 * [225] 用队列实现栈
 */

// @lc code=start
#include <deque>
#include <iostream>
#include <vector>

using std::deque;

// 2、使用一个队列来实现栈
class MyStack {
public:
    /** Initialize your data structure here. */
    MyStack() {

    }
    
    /** Push element x onto stack. */
    void push(int x) {
        int n = queue1.size();
        queue1.push_back(x);
        for (int i = 0; i < n; ++i) {
            queue1.push_back(queue1.front());
            queue1.pop_front();
        }
    }
    
    /** Removes the element on top of the stack and returns that element. */
    int pop() {
        int value = queue1.front();
        queue1.pop_front();
        return value;
    }
    
    /** Get the top element. */
    int top() {
        return queue1.front();
    }
    
    /** Returns whether the stack is empty. */
    bool empty() {
        return queue1.empty();
    }
private:
    // save the stack elements
    deque<int> queue1;
};

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */
// @lc code=end

