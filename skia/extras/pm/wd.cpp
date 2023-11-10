#include "pm.h"
#include <numeric>

int levenshtein(const std::vector<int> &v0, const std::vector<int> &v1)
{
    const size_t l0 = v0.size(), l1 = v1.size();

    if (l0 < l1)
        return levenshtein(v1, v0);

    if (l1 == 0)
        return l0;

    std::vector<int> previous_row(l1 + 1);
    std::iota(previous_row.begin(), previous_row.end(), 0);
    std::vector<int> current_row(l1 + 1);

    for (size_t i = 0; i < l0; ++i)
    {
        current_row[0] = i + 1;
        for (size_t j = 0; j < l1; ++j)
        {
            int insertions = previous_row[j + 1] + 1;
            int deletions = current_row[j] + 1;
            int substitutions = previous_row[j] + (v0[i] != v1[j]);
            current_row[j + 1] = std::min({insertions, deletions, substitutions});
        }

        previous_row.swap(current_row);
    }

    return previous_row[l1];
}