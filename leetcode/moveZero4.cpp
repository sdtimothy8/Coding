/*
 * @lc app=leetcode.cn id=283 lang=cpp
 *
 * [283] 移动零
 */

#include <vector>
#include <iostream>
#include <algorithm>
using std::vector;
// @lc code=start
class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        // 双重遍历法
        size_t j = 0;
        for (size_t i = 0; i < nums.size(); ++i) {
            if (nums[i] != 0) {
                if (i != j) {
                    nums[j] = nums[i];
                }
                ++j;
            }
        }
        // 第二重遍历
        for (; j < nums.size(); ++j) {
            nums[j] = 0;
        }
    }
};

class Solution1 {
public:
    void moveZeroes(vector<int>& nums) {
        // 单重遍历，交换元素法
        size_t j = 0;
        for (size_t i = 0; i < nums.size(); ++i) {
            if (nums[i] != 0) {
                if (i != j) {
                    std::swap(nums[i], nums[j]);
                }
                ++j;
            }
        }
    }
};

void printIntVecValues(const vector<int>& iVec) {
    for (auto iter = iVec.begin(); iter != iVec.end(); ++iter)
        std::cout << *iter << std::endl;
}

int main (int argc, char** argv) {
    Solution obj;
    Solution1 obj1;
    vector<int> iVec = {1,2,0,3};
    vector<int> iVec2 = {1,2,3,4};
    obj.moveZeroes(iVec);
    obj.moveZeroes(iVec2);
    printIntVecValues(iVec);
    printIntVecValues(iVec2);

    return 0;
}
// @lc code=end

