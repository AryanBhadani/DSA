class Solution {
public:

    bool isPossible(vector<int>& weights, int days, int capacity)
    {
        int dayCount = 1;
        int load = 0;

        for(int i = 0; i < weights.size(); i++)
        {
            if(load + weights[i] <= capacity)
            {
                load += weights[i];
            }
            else
            {
                dayCount++;

                if(dayCount > days || weights[i] > capacity)
                {
                    return false;
                }

                load = weights[i];
            }
        }

        return true;
    }

    int shipWithinDays(vector<int>& weights, int days) {

        int s = *max_element(weights.begin(), weights.end());

        int e = accumulate(weights.begin(), weights.end(), 0);

        int ans = -1;

        while(s <= e)
        {
            int mid = s + (e - s) / 2;

            if(isPossible(weights, days, mid))
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