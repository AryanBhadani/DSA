class Solution {
public:
    bool isPerfectSquare(int num) {
        int s=1;
        int e=num;

        while(s<=e)
        {
            int mid=s+(e-s)/2;
            long long square=1ll*mid*mid;
            if(square == num)
            {
                return true;
            
            }
            if(square<num)
            {
                s=mid+1;
            }
            else
            {
                e=mid-1;
            }

        }
        return false;
        
    }
};