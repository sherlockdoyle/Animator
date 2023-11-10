#include "pm.h"

// Slightly stripped down version of
// https://github.com/scipy/scipy/blob/main/scipy/optimize/rectangular_lsap/rectangular_lsap.cpp

static int augmenting_path(const int nc, const float *cost, const std::vector<float> &u, const std::vector<float> &v,
                           std::vector<int> &path, const std::vector<int> &row4col,
                           std::vector<float> &shortestPathCosts, int i, std::vector<bool> &SR, std::vector<bool> &SC,
                           std::vector<int> &remaining, float *p_minVal)
{
    float minVal = 0;

    int num_remaining = nc;
    for (int it = 0; it < nc; ++it)
        remaining[it] = nc - it - 1;

    std::fill(SR.begin(), SR.end(), false);
    std::fill(SC.begin(), SC.end(), false);
    std::fill(shortestPathCosts.begin(), shortestPathCosts.end(), INFINITY);

    int sink = -1;
    while (sink == -1)
    {
        int index = -1;
        float lowest = INFINITY;
        SR[i] = true;

        for (int it = 0; it < num_remaining; ++it)
        {
            int j = remaining[it];

            float r = minVal + cost[i * nc + j] - u[i] - v[j];
            if (r < shortestPathCosts[j])
            {
                path[j] = i;
                shortestPathCosts[j] = r;
            }

            if (shortestPathCosts[j] < lowest || (shortestPathCosts[j] == lowest && row4col[j] == -1))
            {
                lowest = shortestPathCosts[j];
                index = it;
            }
        }

        minVal = lowest;
        if (minVal == INFINITY)
            return -1;

        int j = remaining[index];
        if (row4col[j] == -1)
            sink = j;
        else
            i = row4col[j];

        SC[j] = true;
        remaining[index] = remaining[--num_remaining];
    }

    *p_minVal = minVal;
    return sink;
}

bool solveLSA(const int nr, const int nc, const float cost[], int order[])
{
    std::vector<float> u(nr, 0), v(nc, 0);
    std::vector<float> shortestPathCosts(nc);
    std::vector<int> path(nc, -1);
    std::vector<int> col4row(nr, -1), row4col(nc, -1);
    std::vector<bool> SR(nr), SC(nc);
    std::vector<int> remaining(nc);

    for (int curRow = 0; curRow < nr; ++curRow)
    {
        float minVal;
        int sink =
            augmenting_path(nc, cost, u, v, path, row4col, shortestPathCosts, curRow, SR, SC, remaining, &minVal);
        if (sink < 0)
            return false;

        u[curRow] += minVal;
        for (int i = 0; i < nr; ++i)
            if (SR[i] && i != curRow)
                u[i] += minVal - shortestPathCosts[col4row[i]];

        for (int j = 0; j < nc; ++j)
            if (SC[j])
                v[j] -= minVal - shortestPathCosts[j];

        int j = sink;
        while (true)
        {
            int i = path[j];
            row4col[j] = i;
            std::swap(col4row[i], j);
            if (i == curRow)
                break;
        }
    }

    for (int i = 0; i < nr; ++i)
        order[i] = col4row[i];
    return true;
}