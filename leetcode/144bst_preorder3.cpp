/*
 * @lc app=leetcode.cn id=144 lang=cpp
 *
 * [144] 二叉树的前序遍历
 */

// 使用迭代的思路求解
// @lc code=start
#include <iostream>
#include <vector>
#include <stack>

using std::vector;
using std::stack;
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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        stack<TreeNode*> stk;
        TreeNode* current = root;
        while (!stk.empty() || current != nullptr) {
            if (current != nullptr) {
                result.push_back(current->val); //保存根节点值
                stk.push(current);
                current = current->left; //步骤2：遍历左子树
            }
            else
            {
                TreeNode* temp = stk.top();
                stk.pop();
                current = temp->right; //步骤3：遍历右子树
            }
        }

        return result;
    }
};
// @lc code=end
