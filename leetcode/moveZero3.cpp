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
        // 优化单次遍历的解法，避免对开头非零元素比必要的交换
        size_t j = 0;
        for (size_t i = 0; i < nums.size(); i++) {
            if (nums[i] != 0) {
                // 只有i和j不相等时才作交换，避免了不必要的交换操作
                // 参考std::remove实现
                if (i > j) {
                    std::swap(nums[j], nums[i]);
                }
                ++j; // 元素非零时，i，j一起移动;否则值移动i
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

