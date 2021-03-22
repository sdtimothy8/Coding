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
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        //排序+双指针的解法
        // 1）对数组进行排序
        std::sort(nums.begin(), nums.end());
        // 2) 固定最左边的k，对剩余通过i，j双指针移动
        for (size_t k = 0; k < nums.size(); ++k) {
            if (nums[k] > 0) break;
            if ( k > 0 && nums[k] == nums[k-1]) continue;
            // 定义双指针
            size_t i = k + 1;
            size_t j = nums.size() - 1;
            while (i < j) {
                int sum = nums[i] + nums[j] + nums[k];
                if (sum < 0) {
                    ++i;
                    while (i < j && nums[i] == nums[i-1]) ++i;
                }
                else if (sum > 0) {
                    --j;
                    while (i < j && nums[j] == nums[j+1]) --j;
                    
                }
                else {
                    // vector<int> tmpVec = {nums[i], nums[j], nums[k]};
                    resVecVec.push_back({nums[i], nums[j], nums[k]});
                    ++i;
                    --j;
                    while (i < j && nums[i-1] == nums[i] && nums[j+1] == nums[j]) {
                        ++i;
                        --j;
                    }
                }
            }
        }
        return resVecVec;
    }
};
void printIntVecVec(const vector<vector<int>>& resVec) {
    if (resVec.empty()) {
        std::cout << "[ ]" << std::endl;
        return;
    }

    std::cout << "[";
    for (auto iter1 = resVec.begin(); iter1 != resVec.end(); ++iter1) {
        std::cout << "[";
        for (auto iter2 = (*iter1).begin(); iter2 != (*iter1).end(); ++iter2) {
            std::cout << *iter2;
        }
        std::cout << "]";
    }
    std::cout << "]" << std::endl;
}

int main (int argc, char** argv) {
    Solution obj;
    vector<int> iVec = {0};
    vector<vector<int>> resVecVec = obj.threeSum(iVec);
    printIntVecVec(resVecVec);
    return 0;
}
// @lc code=end

