#ifndef _PATH_MATCHER_H_
#define _PATH_MATCHER_H_

#include "include/core/SkPath.h"

bool solveLSA(const int nr, /* <= */ const int nc, const float cost[/* nr*nc */], int order[/* nr */]);
int levenshtein(const std::vector<int> &s1, const std::vector<int> &s2);

class Segment
{
private:
    mutable float length = 0;
    Segment(const SkPath::Verb verb, const int numPoints, const float length);

public:
    SkPath::Verb verb;
    int numPoints = 0;
    SkPoint points[4];

    Segment(const SkPath::Verb verb, const SkPoint pts[4]);
    void covertToCubic();
    inline float getLength() const { return length; }
    /**
     * Split the current segment in two halves, assign the first half to the current segment and return the second half.
     */
    Segment splitAndGet();
};
class Contour
{
private:
    std::vector<Segment> segments;

    enum class Dir
    {
        ccw,
        cw,
        unknown
    };
    mutable Contour::Dir dir = Contour::Dir::unknown;
    mutable SkPoint center{SK_ScalarInfinity, SK_ScalarInfinity};
    void addConic(const SkPoint pts[4], const SkScalar w);
    void addClose();
    void calcDirCenter() const;

public:
    bool isClosed = false;

    void addSegment(const SkPath::Verb vrb, const SkPoint pts[4], const SkScalar w = 0);
    void convertToCubic();
    Contour::Dir getDir(const bool force = false) const;
    SkPoint getCenter(const bool force = false) const;
    inline size_t size() const { return segments.size(); }
    inline bool empty() const;
    std::vector<int> getVerbs() const;
    Contour getDummyContour() const;
    bool verbsDiffer(const Contour &other) const;
    bool isMoveOnly() const;
    void copyToMoveOnly(Contour &moveOnly) const;
    bool allVerbsSame(SkPath::Verb &verb) const;
    void rotateToStartOf(const Contour &startOf);
    void addEmptySegmentsInBetween(const int numToAdd);
    void splitLargestSegments(const int numToAdd);
    inline void writeToPath(SkPath &path) const;
};
SkScalar distanceSqd(const SkPoint &p0, const SkPoint &p1);
class Path
{
public:
    std::vector<Contour> contours;

    Path(const SkPath &path);
    void convertToCubic();
    void writeToPath(SkPath &path) const;

    static void getContourCost(const Path &p0, const Path &p1, const float distFactor, float cost[]);
};

class ContourMatcher
{
private:
    Path path0, path1;
    bool swapped = false;

    inline void reorderPath1(const int order[]);

public:
    enum class MatchType
    {
        inBetween,
        split
    };

    ContourMatcher(const SkPath &p0, const SkPath &p1, const float distFactor = 1.0f,
                   const MatchType matchType = MatchType::inBetween);
    void writeToPath(SkPath &p0, SkPath &p1) const;
};

#endif