class Solution {
public:
    int mySqrt(int x) {
        int start = 0;
        int end = x;
        int ans = 0;
        while (start <= end) {
            long long mid = start + (end - start) / 2;
            long long square = mid * mid;

            if (square == x) {
                return mid;
            }

            if (square < x) {
                ans = mid;
                start = mid + 1;
            } else {
                end = mid - 1;
            }
        }
        return ans;
    }
};