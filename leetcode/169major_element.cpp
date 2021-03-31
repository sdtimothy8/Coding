/*
 * @lc app=leetcode.cn id=169 lang=cpp
 *
 * [169] 多数元素
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>

using std::vector;
using std::unordered_map;

// 思路1：排序方法
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        std::sort(nums.begin(), nums.end());
        return nums[nums.size() / 2];
    }
};

// 思路2：映射方法
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        unordered_map<int, int> intMap;
        for (int i = 0; i < nums.size(); ++i) {
            if (++intMap[nums[i]] > nums.size() / 2)
                return intMap[i];
        }
    }
};

// 思路3：摩尔选举法
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int elected = nums[0];
        int count = 1;
        for (int i = 1; i < nums.size(); ++i) {
            if (nums[i] == elected) {
                count++;
            }
            else if (--count == 0) {
                elected = nums[i];
                count = 1;
            }
        }
        return elected;
    }
};

// 思路4：随机数法
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        
    }
};

// @lc code=end

