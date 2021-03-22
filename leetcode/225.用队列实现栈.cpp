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

class MyStack {
public:
    /** Initialize your data structure here. */
    MyStack() {

    }
    
    /** Push element x onto stack. */
    void push(int x) {
        // 元素先入队queue2, 再把queue1中元素入队到queue2中
        queue2.push_back(x);
        while (!queue1.empty()) {
            queue2.push_back(queue1.front());
            queue1.pop_front();
        }
        std::swap(queue2, queue1);       
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
    // 辅助队列
    deque<int> queue2;
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

