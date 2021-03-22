/*
 * @lc app=leetcode.cn id=155 lang=cpp
 *
 * [155] 最小栈
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <climits>
using std::vector;

class MinStack {
public:
    /** initialize your data structure here. */
    MinStack() :
    iVec(),
    minValue(INT_MAX)
    {
    }
    
    void push(int x) {
        if (x < minValue) {
            minValue = x;
        }
        iVec.push_back(x);
    }
    
    void pop() {
        // 1）如果最小值不是最后一个元素，不用管
        // 2）如果最小值是最后一个元素，重新选择最小的元素
        int lastVal = iVec.back();
        iVec.pop_back();

        if (lastVal == minValue) {
            if (iVec.empty())
                minValue = INT_MAX;
            else {
                minValue = iVec.front();
                for (auto iter = iVec.begin(); iter != iVec.end(); ++iter)
                    if (minValue > *iter)
                        minValue = *iter;
            }
        }
    }
    
    int top() {
        return iVec.back();
    }
    
    int getMin() {
        return minValue;
    }

private:
    void setMin(int value) { minValue = value; }
    vector<int> iVec;
    int minValue;
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

