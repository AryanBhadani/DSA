class Solution {
public:
    void reverseString(vector<char>& s) {
    int left=0;
    int right =s.size()-1;
    while(right>left)
    {
        swap(s[right],s[left]);

        right--;
        left++;

    }

    }
};