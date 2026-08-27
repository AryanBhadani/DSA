bool ispossible(vector<int>& nums, int k,int mid)
{
    int subarraycount =1;
    int sum =0;
    for(int i=0;i<nums.size();i++)
    {
        if(sum+nums[i]<=mid)
        {
            sum+=nums[i];
        }
        else{
            subarraycount++;
            if(subarraycount >k||nums[i]>mid)
            {
                return false;
            }
            sum =nums[i];
        }
    }
    return true;
}

class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int s=0;
        int sum=0;
        for(int i=0;i<nums.size();i++)
        {
            sum += nums[i];

        }
        int e =sum;
        int ans=-1;
        while(s<=e)
        {
            int mid=s+(e-s)/2;
            if(ispossible(nums,k,mid))
            {
                ans=mid;
                e=mid-1;
            }
            else{
                s=mid+1;
            }
        }
        return ans;
    }
};