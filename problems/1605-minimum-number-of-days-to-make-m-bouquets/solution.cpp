bool isPossible(vector<int>& bloomDay, int m, int k, int day)
    {
        int flowerCount = 0;
        int bouquetCount = 0;

        for(int i = 0; i < bloomDay.size(); i++)
        {
            if(bloomDay[i] <= day)
            {
                flowerCount++;

                if(flowerCount == k)
                {
                    bouquetCount++;
                    flowerCount = 0;
                }
            }
            else
            {
                flowerCount = 0;
            }
        }

        return bouquetCount >= m;
    }
class Solution {
public:
    int minDays(vector<int>& bloomDay, int m, int k) {

        if((long long)m * k > bloomDay.size())
        {
            return -1;
        }

        int s = 0;
        int e = *max_element(bloomDay.begin(), bloomDay.end());


        int ans = -1;

        while(s <= e)
        {
            int mid = s + (e - s) / 2;

            if(isPossible(bloomDay, m, k, mid))
            {
                ans = mid;
                e = mid - 1;
            }
            else
            {
                s = mid + 1;
            }
        }

        return ans;
    }
};