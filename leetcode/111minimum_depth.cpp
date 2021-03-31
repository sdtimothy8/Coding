/*
 * @lc app=leetcode.cn id=111 lang=cpp
 *
 * [111] 二叉树的最小深度
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

class Solution {
public:
    int minDepth(TreeNode* root) {
        return _minDepth(root);
    }

    int _minDepth(TreeNode* node) {
        if (node == nullptr)
            return 0;
        int left = _minDepth(node->left);
        int right = _minDepth(node->right);
        if (node->left == nullptr || node->right ==nullptr)
            return left + right + 1;
        else 
        {
            // 当前节点同时有左右子树
            // 最小深度为左右子树最小深度的较小值+1
            return 1 + std::min(_minDepth(node->left), _minDepth(node->right));
        }
    }
};
// @lc code=end

