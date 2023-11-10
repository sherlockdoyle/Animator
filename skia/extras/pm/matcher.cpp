#include "pm.h"
#include <queue>

void Contour::copyToMoveOnly(Contour &moveOnly) const
{
    const SkPoint start = moveOnly.segments[0].points[0];
    const SkPoint points[4] = {start, start, start, start};
    moveOnly.segments.clear();
    for (const Segment &seg : segments)
        moveOnly.segments.emplace_back(seg.verb, points);
}

void Contour::rotateToStartOf(const Contour &startOf)
{
    const SkPoint &centeredStart = startOf.segments[0].points[0] - startOf.getCenter(), thisCenter = getCenter();
    float minDist = std::numeric_limits<float>::max();
    int minIndex = -1;
    for (size_t i = 0, l = segments.size(); i < l; ++i)
    {
        const float dist = distanceSqd(centeredStart, segments[i].points[0] - thisCenter);
        if (dist < minDist)
        {
            minDist = dist;
            minIndex = i;
        }
    }
    std::rotate(segments.begin(), segments.begin() + minIndex, segments.end());
}

void Contour::addEmptySegmentsInBetween(const int numToAdd)
{
    const SkPath::Verb verb = segments[0].verb;
    const size_t l = segments.size();
    const auto [numReps, numExtra] = std::div(numToAdd, l + 1);
    std::vector<Segment> matchedSegments;
    matchedSegments.reserve(l + numToAdd);

    int D = 2 * numExtra - l; // bresenham line algorithm for inserting extra segments
    for (size_t i = 0; i < l; ++i)
    {
        const SkPoint &firstPoint = segments[i].points[0];
        const SkPoint points[4] = {firstPoint, firstPoint, firstPoint, firstPoint};
        for (int j = 0; j < numReps; ++j)
            matchedSegments.emplace_back(verb, points);
        if (D > 0)
        {
            matchedSegments.emplace_back(verb, points);
            D += 2 * (numExtra - l);
        }
        else
            D += 2 * numExtra;
        matchedSegments.push_back(segments[i]);
    }

    const Segment &lastSegment = matchedSegments.back();
    const SkPoint &lastPoint = lastSegment.points[lastSegment.numPoints - 1];
    const SkPoint points[4] = {lastPoint, lastPoint, lastPoint, lastPoint};
    for (int j = 0; j < numReps; ++j)
        matchedSegments.emplace_back(verb, points);
    segments.swap(matchedSegments);
}

struct Node
{
    Segment seg;
    Node *next;
    Node(Segment seg) : seg(seg), next(nullptr) {}
};
struct CompareNode
{
    bool operator()(Node *n1, Node *n2) { return n1->seg.getLength() < n2->seg.getLength(); }
};
class HeapList
{
private:
    Node *tail;
    std::priority_queue<Node *, std::vector<Node *>, CompareNode> maxHeap;

    void insert(Node *n)
    {
        if (tail == nullptr)
            n->next = n;
        else
        {
            n->next = tail->next;
            tail->next = n;
        }
        tail = n;
        maxHeap.push(n);
    }

public:
    HeapList(std::vector<Segment> &segments) : tail(nullptr)
    {
        for (Segment &seg : segments)
            insert(new Node(seg));
    }
    ~HeapList()
    {
        if (tail != nullptr)
        {
            Node *head = tail->next;
            tail->next = nullptr;
            while (head != nullptr)
            {
                Node *tmp = head;
                head = head->next;
                delete tmp;
            }
        }
    }
    void splitMax()
    {
        Node *const maxNode = maxHeap.top(), *const nextNode = maxNode->next;
        maxHeap.pop();
        maxNode->next = new Node(maxNode->seg.splitAndGet());
        maxHeap.push(maxNode);
        maxHeap.push(maxNode->next);
        maxNode->next->next = nextNode;
        if (maxNode == tail)
            tail = maxNode->next;
    }
    void getSegments(std::vector<Segment> &segments) const
    {
        Node *head = tail->next, *curr = head;
        segments.clear();
        do
        {
            segments.push_back(curr->seg);
            curr = curr->next;
        } while (curr != head);
    }
};
void Contour::splitLargestSegments(const int numToAdd)
{
    HeapList heapList(segments);
    for (int i = 0; i < numToAdd; ++i)
        heapList.splitMax();
    heapList.getSegments(segments);
}

inline void ContourMatcher::reorderPath1(const int order[])
{
    const size_t l0 = path0.contours.size(), l1 = path1.contours.size();
    std::vector<bool> visited(l1, false);
    std::vector<Contour> sortedContours;
    sortedContours.reserve(l1);
    for (size_t i = 0; i < l0; ++i)
    {
        sortedContours.push_back(path1.contours[order[i]]);
        visited[order[i]] = true;
    }
    for (size_t i = 0; i < l1; ++i)
        if (!visited[i])
            sortedContours.push_back(path1.contours[i]);
    path1.contours.swap(sortedContours);
}

ContourMatcher::ContourMatcher(const SkPath &p0, const SkPath &p1, const float distFactor, const MatchType matchType)
    : path0(p0), path1(p1)
{
    if (path1.contours.size() < path0.contours.size())
    {
        std::swap(path0, path1);
        swapped = true;
    }
    auto matcher = std::bind(matchType == MatchType::inBetween ? &Contour::addEmptySegmentsInBetween
                                                               : &Contour::splitLargestSegments,
                             std::placeholders::_1, std::placeholders::_2);

    const size_t l0 = path0.contours.size(), l1 = path1.contours.size();
    float cost[l0 * l1];
    Path::getContourCost(path0, path1, distFactor, cost);
    int order[l0];
    solveLSA(l0, l1, cost, order);

    reorderPath1(order);             // reorder path1 contours as per order
    for (size_t i = l0; i < l1; ++i) // add dummy contours for unmatched contours
        path0.contours.push_back(path1.contours[i].getDummyContour());
    for (size_t i = 0; i < l0; ++i)
    {
        Contour &c0 = path0.contours[i], &c1 = path1.contours[i];
        const size_t l0 = c0.size(), l1 = c1.size();
        if (!(c1.isClosed && l0 < l1) && c0.isClosed)
            c0.rotateToStartOf(c1);
        if ((!c0.isClosed || l0 < l1) && c1.isClosed)
            c1.rotateToStartOf(c0);

        if (c0.verbsDiffer(c1))
        {
            if (c0.isMoveOnly())
                c1.copyToMoveOnly(c0);
            else if (c1.isMoveOnly())
                c0.copyToMoveOnly(c1);
            else
            {
                SkPath::Verb verb0, verb1;
                if (!(c0.allVerbsSame(verb0) && c1.allVerbsSame(verb1) && verb0 == verb1))
                {
                    c0.convertToCubic();
                    c1.convertToCubic();
                }
                if (l0 < l1)
                    matcher(&c0, l1 - l0);
                else if (l1 < l0)
                    matcher(&c1, l0 - l1);
            }
        }
    }

    for (size_t i = 0; i < l1; ++i)
        if (path0.contours[i].isClosed != path1.contours[i].isClosed)
            path0.contours[i].isClosed = path1.contours[i].isClosed = false;
}

void ContourMatcher::writeToPath(SkPath &p0, SkPath &p1) const
{
    if (swapped)
    {
        path0.writeToPath(p1);
        path1.writeToPath(p0);
    }
    else
    {
        path0.writeToPath(p0);
        path1.writeToPath(p1);
    }
}