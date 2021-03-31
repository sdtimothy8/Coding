/*
 * @lc app=leetcode.cn id=102 lang=cpp
 *
 * [102] 二叉树的层序遍历
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <deque>

using std::vector;
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
        deque<TreeNode*> queue;
        queue.push_back(root);
        while (!queue.empty()) {
            int n = queue.size();
            vector<int> tempResult;
            for (int i = 0; i < n; ++i) {
                TreeNode* current = queue.front();
                tempResult.push_back(current->val);
                queue.pop_front();
                if (current->left)
                    queue.push_back(current->left);
                if (current->right)
                    queue.push_back(current->right);
            }
            result.push_back(tempResult);
        }
        return result;
    }
};
// @lc code=end

