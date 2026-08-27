class Solution {
public:
    bool possible(vector<int>&piles,int h ,int k)
    {
        long long hours =0;
        for(int i=0;i<piles.size();i++)
        {
            hours+=(piles[i]+k-1)/k;
        }
        return hours<=h;
     }
    int minEatingSpeed(vector<int>& piles, int h) {
        int s=1;
        int e= *max_element(piles.begin(), piles.end());
        int ans =e;
        while(s<=e)
        {
            int mid=s+(e-s)/2;
            if(possible(piles,h,mid))
            {
                ans = mid;
                e =mid-1;
            }
            else
            {
                s=mid+1;
            }
        }
        return ans;
    }
};