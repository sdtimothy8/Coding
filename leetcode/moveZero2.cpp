/*
 * @lc app=leetcode.cn id=283 lang=cpp
 *
 * [283] 移动零
 */

// @lc code=start
#include <vector>
#include <iostream>
#include <algorithm>
using std::vector;

class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        // 一次遍历，交换非零和零元素位置的元素
        for (size_t i = 0, j = 0; i < nums.size(); i++) {
            if (nums[i] != 0) {
                std::swap(nums[j++], nums[i]);
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
    vector<int> iVec = {0,0,0,1};
    obj.moveZeroes(iVec);
    printIntVecValues(iVec);
    return 0;
}
// @lc code=end

