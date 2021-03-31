/*
 * @lc app=leetcode.cn id=104 lang=cpp
 *
 * [104] 二叉树的最大深度
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <stack>

using std::vector;
using std::stack;

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

// 思路：
class Solution {
public:
    int maxDepth(TreeNode* root) {
        return _maxdepth(root);
    }
    
    int _maxdepth(TreeNode* node) {
        if (node == nullptr)
            return 0;
        
        int leftDepth = _maxdepth(node->left);
        int rightDepth = _maxdepth(node->right);
        return std::max(leftDepth, rightDepth) + 1;
    }
};
// @lc code=end

