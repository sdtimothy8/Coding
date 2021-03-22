/*
 * @lc app=leetcode.cn id=15 lang=cpp
 *
 * [15] 三数之和
 */

// @lc code=start
#include <vector>
#include <algorithm>
#include <iostream>
using std::vector; 

class Solution {
public:
    void bubbleSort(vector<int>& nums) {
        for (size_t i = 1; i < nums.size(); ++i) {
            for (size_t j = 0; j < nums.size() - 1; ++j) {
                if (nums[j] > nums[j+1]) {
                    std::swap(nums[j], nums[j+1]);
                }
            }
        }
    }
};
void printIntVec(const vector<int>& resVec) {
    std::cout << "[";
    for (auto iter1 = resVec.begin(); iter1 != resVec.end(); ++iter1) {
        std::cout << *iter1;
    }
    std::cout << "]" << std::endl;
}

int main (int argc, char** argv) {
    Solution obj;
    vector<int> iVec = {-1,0,1,2,-1,-4};
    obj.bubbleSort(iVec);
    printIntVec(iVec);
    return 0;
}
// @lc code=end

