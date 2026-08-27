class Solution {
public:
    int heightChecker(vector<int>& heights) {

        vector<int> expected = heights;
        int n = expected.size();

        for (int i = 0; i < n - 1; i++) {

            int minIndex = i;

            for (int j = i + 1; j < n; j++) {

                if (expected[j] < expected[minIndex]) {
                    minIndex = j;
                }
            }

            swap(expected[i], expected[minIndex]);
        }

        int count = 0;

        for (int i = 0; i < n; i++) {

            if (heights[i] != expected[i]) {
                count++;
            }
        }

        return count;
    }
};