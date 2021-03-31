/*
 * @lc app=leetcode.cn id=102 lang=cpp
 *
 * [102] 二叉树的层序遍历
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <map>
#include <deque>

using std::vector;
using std::map;
using std::deque;

//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (root == nullptr)
            return result;
        int level = 0;
        bfs(root, level, result);
        return result;
    }

    void bfs(TreeNode* current, int level, vector<vector<int>>& result) {
        if (level >= result.size()) {
            result.push_back(vector<int>());
        }
        result[level].push_back(current->val);
        if (current->left)
            bfs(current->left, level + 1, result);
        if (current->right)
            bfs(current->right, level + 1, result);
    }
};
// @lc code=end

