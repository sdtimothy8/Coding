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
        size_t j = 0;
        // 非零元素前移
        for (size_t i = 0; i < nums.size(); i++) {
            if (nums[i]) {
                nums[j++] = nums[i];
            }
        }
        // j为非零元素的个数并指向非零元素序列的尾部
        // 将[j,num.size()]元素置零
        while (j < nums.size()) {
            nums[j++] = 0;
        }
    }
};

void printIntVecValues(const vector<int>& iVec) {
    for (auto iter = iVec.begin(); iter != iVec.end(); ++iter)
        std::cout << *iter << std::endl;
}

int main (int argc, char** argv) {
    Solution obj;
    vector<int> iVec = {1,2,2,3,4};
    // obj.moveZeroes(iVec);
    std::remove(iVec.begin(), iVec.end(), 2);
    printIntVecValues(iVec);
    return 0;
}
// @lc code=end

