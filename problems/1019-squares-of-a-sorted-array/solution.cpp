class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int left = 0;
        int right = nums.size() - 1;
        vector<int> ans(nums.size());
        int k = nums.size() - 1;

        while (right >= left) {
            if (abs(nums[left]) > abs(nums[right])) {
                ans[k] = nums[left] * nums[left];
                left++;
            } else {
                ans[k] = nums[right] * nums[right];
                right--;
            }
            k--;
        }
        return ans;
    }
};