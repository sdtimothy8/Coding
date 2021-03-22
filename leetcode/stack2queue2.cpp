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
// 思路：使用双栈，一个栈负责元素入队，一个栈负责元素出队
// 注意：代码复用问题，peek和pop函数代码可以复用
class MyQueue {
public:
    /** Initialize your data structure here. */
    MyQueue() {

    }
    
    /** Push element x to the back of queue. */
    void push(int x) {
        stack_in.push(x);
    }
    
    /** Removes the element from in front of queue and returns that element. */
    int pop() {
        // 代码复用
        int top = peek();
        stack_out.pop();
        return top;
    }
    
    /** Get the front element. */
    int peek() {
        if (stack_out.empty()) {
            while (!stack_in.empty()) {
                stack_out.push(stack_in.top());
                stack_in.pop();
            }
        }
        return stack_out.top();
    }
    
    /** Returns whether the queue is empty. */
    bool empty() {
        return (stack_in.empty() && stack_out.empty());
    }
private:
    // 负责队列入队
    stack<int>  stack_in;
    // 负责队列出队
    stack<int>  stack_out;
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

