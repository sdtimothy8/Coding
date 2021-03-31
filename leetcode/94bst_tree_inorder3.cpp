/*
 * @lc app=leetcode.cn id=94 lang=cpp
 *
 * [94] 二叉树的中序遍历
 */

// @lc code=start
 //Definition for a binary tree node.

 // 采用迭代的思路
#include <iostream>
#include <vector>
#include <stack>

using std::vector;
using std::stack;

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
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> result;
        stack<TreeNode*> stk;
        TreeNode* current = root;
        while (!stk.empty() || current != nullptr) {
            if (current != nullptr) {
                stk.push(current);    
                current = current->left;
            }
            else
            {
                TreeNode* temp = stk.top();
                result.push_back(temp->val);
                stk.pop();
                current = temp->right;
            }
        }
        return result;
    }
};
// @lc code=end

