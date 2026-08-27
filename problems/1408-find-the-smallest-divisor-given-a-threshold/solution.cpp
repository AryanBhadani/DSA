class Solution {
public:
    bool possible(vector<int> nums,int threshold,int divisor)
    {   
        long long sum =0;
        for(int i=0;i<nums.size();i++)
        {
            sum += (nums[i]+divisor-1)/divisor;
        }
        return sum<=threshold;
    }
    int smallestDivisor(vector<int>& nums, int threshold) {
        int s=1;
        int e= *max_element(nums.begin(),nums.end());
        int ans=e;
        
        while(s<=e)
        {
            int mid=s+(e-s)/2;
            
            if(possible(nums,threshold,mid))
            {
                ans=mid;
                e=mid-1;
            }
            else
            {
                s=mid+1;
            }

        }
        return ans;
    
    }
        
    
};