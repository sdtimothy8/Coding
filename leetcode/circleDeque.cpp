/*
 * @lc app=leetcode.cn id=641 lang=cpp
 *
 * [641] 设计循环双端队列
 */

// @lc code=start
#include <list>
#include <iostream>
#include <vector>

using std::list;

class MyCircularDeque {
public:
    /** Initialize your data structure here. Set the size of the deque to be k. */
    MyCircularDeque(int k) :
    iList(),
    size(k)
    {
    }
    
    /** Adds an item at the front of Deque. Return true if the operation is successful. */
    bool insertFront(int value) {
        if (iList.size() < size) {
            iList.push_front(value);
            return true;
        }
        else
        {
            return false;
        }
    }
    
    /** Adds an item at the rear of Deque. Return true if the operation is successful. */
    bool insertLast(int value) {
        if (iList.size() < size) {
            iList.push_back(value);
            return true;
        }
        else
        {
            return false;
        }
    }
    
    /** Deletes an item from the front of Deque. Return true if the operation is successful. */
    bool deleteFront() {
        if (!iList.empty()) {
            iList.pop_front();
            return true;
        }
        else
        {
            return false;
        }
    }
    
    /** Deletes an item from the rear of Deque. Return true if the operation is successful. */
    bool deleteLast() {
        if (!iList.empty()) {
            iList.pop_back();
            return true;
        }
        else
        {
            return false;
        }
    }
    
    /** Get the front item from the deque. */
    int getFront() {
        if (!iList.empty())
            return iList.front();
        else
        {
            return -1;
        }
    }
    
    /** Get the last item from the deque. */
    int getRear() {
        if (!iList.empty())
            return iList.back();
        else
        {
            return -1;
        }
    }
    
    /** Checks whether the circular deque is empty or not. */
    bool isEmpty() {
        return iList.empty();
    }
    
    /** Checks whether the circular deque is full or not. */
    bool isFull() {
        return iList.size() == size;
    }
private:
    list<int> iList;
    int       size;
};

/**
 * Your MyCircularDeque object will be instantiated and called as such:
 * MyCircularDeque* obj = new MyCircularDeque(k);
 * bool param_1 = obj->insertFront(value);
 * bool param_2 = obj->insertLast(value);
 * bool param_3 = obj->deleteFront();
 * bool param_4 = obj->deleteLast();
 * int param_5 = obj->getFront();
 * int param_6 = obj->getRear();
 * bool param_7 = obj->isEmpty();
 * bool param_8 = obj->isFull();
 */
// @lc code=end

