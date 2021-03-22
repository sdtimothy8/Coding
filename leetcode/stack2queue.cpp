/*
 * @lc app=leetcode.cn id=232 lang=cpp
 *
 * [232] 用栈实现队列
 */
#include <stack>
#include <iostream>
#include <vector>

using std::stack;

// @lc code=start
class MyQueue {
public:
    /** Initialize your data structure here. */
    MyQueue() {

    }
    
    /** Push element x to the back of queue. */
    void push(int x) {
        while (!stack1.empty()) {
            stack2.push(stack1.top());
            stack1.pop();
        }
        stack2.push(x);
        //再把stack2中的元素push到stack1中。
        while (!stack2.empty()) {
            stack1.push(stack2.top());
            stack2.pop();
        }
    }
    
    /** Removes the element from in front of queue and returns that element. */
    int pop() {
        int top = stack1.top();
        stack1.pop();
        return top;
    }
    
    /** Get the front element. */
    int peek() {
        return stack1.top();
    }
    
    /** Returns whether the queue is empty. */
    bool empty() {
        return stack1.empty();
    }
private:
    // 真正存放数据
    stack<int>  stack1;
    // 辅助栈
    stack<int>  stack2;
};

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue* obj = new MyQueue();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->peek();
 * bool param_4 = obj->empty();
 */
// @lc code=end

