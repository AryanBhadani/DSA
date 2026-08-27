class Solution {
public:
    int firstUniqChar(string s) {
        
        int arr[26] = {0};

        // Frequency count
        for (int i = 0; i < s.length(); i++) {
            int number = s[i] - 'a';
            arr[number]++;
        }

        // Find first character with frequency 1
        for (int i = 0; i < s.length(); i++) {
            int number = s[i] - 'a';

            if (arr[number] == 1) {
                return i;
            }
        }

        return -1;
    }
};