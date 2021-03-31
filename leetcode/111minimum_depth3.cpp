/*
 * @lc app=leetcode.cn id=111 lang=cpp
 *
 * [111] 二叉树的最小深度
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <deque>

using std::vector;
using std::deque;

// Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

// 最短路径问题，使用BFS
// 找到第一个叶子节点
class Solution {
public:
    int minDepth(TreeNode* root) {
        if (root == nullptr)
            return 0;
        deque<TreeNode*> queue;
        queue.push_back(root);
        TreeNode* current = root;
        int depth = 1;
        while (!queue.empty()) {
            int n = queue.size();
            for (int i = 0; i < n; ++i) {
                TreeNode* head = queue.front();
                if (head->left == nullptr && head->right == nullptr)
                    return depth;
                queue.pop_front();
                if (head->left)
                    queue.push_back(head->left);
                if (head->right)
                    queue.push_back(head->right);
            }
            ++depth;
        }
        return depth;
    }

};
// @lc code=end

