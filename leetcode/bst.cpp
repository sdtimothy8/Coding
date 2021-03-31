#include <iostream>

struct TreeNode {
    TreeNode* left;
    TreeNode* right;
    int   value;
    TreeNode(int x): left(NULL), right(NULL),value(x) {}
};

// 前序遍历
void preOrder(TreeNode* node) {
    if (node == NULL)
        return;
    std::cout << node->value;
    preOrder(node->left);
    preOrder(node->right);
}

// 中序遍历
void inOrder(TreeNode* node) {
    if (node == NULL)
        return;
    inOrder(node->left);
    std::cout << node->value;
    inOrder(node->right);    
}

// 后序遍历
void postOrder(TreeNode* node) {
    if (node == NULL)
        return;
    postOrder(node->left);
    postOrder(node->right);
    std::cout << node->value;
}

int main(int argc, char** argv) {

    return 0;
}