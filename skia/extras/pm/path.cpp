#include "pm.h"
#include "src/core/SkGeometry.h"

static inline int getNumPoints(const SkPath::Verb verb)
{
    switch (verb)
    {
    case SkPath::Verb::kMove_Verb:
        return 1;
    case SkPath::Verb::kLine_Verb:
        return 2;
    case SkPath::Verb::kQuad_Verb:
        return 3;
    case SkPath::Verb::kCubic_Verb:
        return 4;
    default:
        return 0;
    }
}
Segment::Segment(const SkPath::Verb verb, const SkPoint pts[4]) : verb(verb), numPoints(getNumPoints(verb))
{
    std::copy(pts, pts + numPoints, points);
    for (int i = 1; i < numPoints; ++i)
        length += SkPoint::Distance(points[i - 1], points[i]);
}

void Segment::covertToCubic()
{
    switch (verb)
    {
    case SkPath::Verb::kMove_Verb:
        points[1] = points[2] = points[3] = points[0];
        break;
    case SkPath::Verb::kLine_Verb:
    {
        points[3] = points[1];
        SkPoint diff = points[3] - points[0];
        points[1] = points[0] + diff * (1.0f / 3.0f);
        points[2] = points[0] + diff * (2.0f / 3.0f);
        break;
    }
    case SkPath::Verb::kQuad_Verb:
        SkConvertQuadToCubic(points, points);
        break;
    default:
        break;
    }
    verb = SkPath::Verb::kCubic_Verb;
    numPoints = 4;
}

Segment::Segment(const SkPath::Verb vrb, const int numPoints, const float length)
    : length(length), verb(vrb), numPoints(numPoints)
{
}
Segment Segment::splitAndGet()
{
    length /= 2;
    Segment second(verb, numPoints, length);
    second.points[numPoints - 1] = points[numPoints - 1];
    switch (verb)
    {
    case SkPath::Verb::kLine_Verb:
    {
        points[1] = second.points[0] = (points[0] + points[1]) * 0.5f;
        break;
    }
    case SkPath::Verb::kQuad_Verb:
    {
        SkPoint pts[5];
        SkChopQuadAtHalf(points, pts);
        points[1] = pts[1];
        points[2] = second.points[0] = pts[2];
        second.points[1] = pts[3];
        break;
    }
    case SkPath::Verb::kCubic_Verb:
    {
        SkPoint pts[7];
        SkChopCubicAtHalf(points, pts);
        points[1] = pts[1];
        points[2] = pts[2];
        points[3] = second.points[0] = pts[3];
        second.points[1] = pts[4];
        second.points[2] = pts[5];
        break;
    }
    default:
        break;
    }
    return second;
}

void Contour::addConic(const SkPoint pts[4], const SkScalar w)
{
    SkAutoConicToQuads quadder;
    const SkPoint *quadPts = quadder.computeQuads(pts, w, SK_Scalar1 / 1024);
    for (int i = 0; i < quadder.countQuads(); ++i)
    {
        SkPoint quad[4] = {quadPts[i * 2], quadPts[i * 2 + 1], quadPts[i * 2 + 2]};
        segments.emplace_back(SkPath::Verb::kQuad_Verb, quad);
    }
}

void Contour::addClose()
{
    const Segment &lastSegment = segments.back();
    const SkPoint &firstPoint = segments[0].points[0], lastPoint = lastSegment.points[lastSegment.numPoints - 1];
    if (!(SkScalarNearlyEqual(firstPoint.fX, lastPoint.fX) && SkScalarNearlyEqual(firstPoint.fY, lastPoint.fY)))
        segments.emplace_back(SkPath::Verb::kLine_Verb, (SkPoint[4]){lastPoint, firstPoint, {0, 0}, {0, 0}});
    isClosed = true;
}

void Contour::addSegment(const SkPath::Verb vrb, const SkPoint pts[4], const SkScalar w)
{
    if (vrb == SkPath::Verb::kClose_Verb)
        addClose();
    else
    {
        if (segments.size() == 1 && segments[0].verb == SkPath::Verb::kMove_Verb)
            segments.pop_back();
        if (vrb == SkPath::Verb::kConic_Verb)
            addConic(pts, w);
        else
            segments.emplace_back(vrb, pts);
    }
}

void Contour::convertToCubic()
{
    for (Segment &seg : segments)
        seg.covertToCubic();
}

void Contour::calcDirCenter() const
{
    float area = 0;
    SkPoint center{segments[0].points[0]};
    int numPoints = 1;
    for (const Segment &seg : segments)
        for (int j = 1; j < seg.numPoints; ++j)
        {
            area += seg.points[j - 1].fX * seg.points[j].fY - seg.points[j].fX * seg.points[j - 1].fY;
            center += seg.points[j];
            ++numPoints;
        }
    dir = area < 0 ? Dir::ccw : Dir::cw;
    this->center = center * (1.0f / numPoints);
}

Contour::Dir Contour::getDir(const bool force) const
{
    if (dir == Dir::unknown || force)
        calcDirCenter();
    return dir;
}

SkPoint Contour::getCenter(const bool force) const
{
    if (!center.isFinite() || force)
        calcDirCenter();
    return center;
}

inline bool Contour::empty() const { return segments.empty(); }

std::vector<int> Contour::getVerbs() const
{
    std::vector<int> verbs;
    for (const Segment &seg : segments)
        verbs.push_back(seg.verb);
    return verbs;
}

Contour Contour::getDummyContour() const
{
    const SkPoint center = getCenter();
    const SkPoint points[] = {center, center, center, center};
    Contour dummy;
    for (const Segment &seg : segments)
        dummy.addSegment(seg.verb, points);
    return dummy;
}

bool Contour::verbsDiffer(const Contour &other) const
{
    const size_t l = segments.size();
    if (l != other.segments.size())
        return true;
    for (size_t i = 0; i < l; ++i)
        if (segments[i].verb != other.segments[i].verb)
            return true;
    return false;
}

bool Contour::isMoveOnly() const { return segments.size() == 1 && segments[0].verb == SkPath::Verb::kMove_Verb; }

bool Contour::allVerbsSame(SkPath::Verb &verb) const
{
    verb = segments[0].verb;
    for (int i = 1, l = segments.size(); i < l; ++i)
        if (segments[i].verb != verb)
            return false;
    return true;
}

inline void Contour::writeToPath(SkPath &path) const
{
    if (segments[0].verb != SkPath::Verb::kMove_Verb)
        path.moveTo(segments[0].points[0]);

    for (const Segment &seg : segments)
        switch (seg.verb)
        {
        case SkPath::Verb::kMove_Verb:
            path.moveTo(seg.points[0]);
            break;
        case SkPath::Verb::kLine_Verb:
            path.lineTo(seg.points[1]);
            break;
        case SkPath::Verb::kQuad_Verb:
            path.quadTo(seg.points[1], seg.points[2]);
            break;
        case SkPath::Verb::kCubic_Verb:
            path.cubicTo(seg.points[1], seg.points[2], seg.points[3]);
            break;
        default:
            break;
        }

    if (isClosed)
        path.close();
}

Path::Path(const SkPath &path)
{
    SkPath::Iter iter(path, false);
    SkPath::Verb verb;
    SkPoint points[4];
    Contour contour;
    while ((verb = iter.next(points)) != SkPath::Verb::kDone_Verb)
    {
        if (verb == SkPath::Verb::kMove_Verb)
        {
            if (!contour.empty())
                contours.push_back(contour);
            contour = Contour();
        }
        contour.addSegment(verb, points, iter.conicWeight());
    }
    if (!contour.empty())
        contours.push_back(contour);
}

void Path::convertToCubic()
{
    for (Contour &contour : contours)
        contour.convertToCubic();
}

void Path::writeToPath(SkPath &path) const
{
    path.rewind();
    for (const Contour &contour : contours)
        contour.writeToPath(path);
}

SkScalar distanceSqd(const SkPoint &p0, const SkPoint &p1)
{
    SkScalar dx = p0.fX - p1.fX;
    SkScalar dy = p0.fY - p1.fY;
    return dx * dx + dy * dy;
}
static float getCost(const Contour &c0, const Contour &c1, const SkPoint &center0, const SkPoint &center1,
                     const SkScalar distFactor)
{
    std::vector<int> v0s = c0.getVerbs(), v1s = c1.getVerbs();
    float cost = (1 + distanceSqd(c0.getCenter() - center0, c1.getCenter() - center1) * distFactor) *
                 (1 + levenshtein(v0s, v1s) / std::max<float>(v0s.size(), v1s.size()));
    if (c0.getDir() != c1.getDir())
        return cost * 2;
    return cost;
}
void Path::getContourCost(const Path &p0, const Path &p1, const float distFactor, float cost[])
{
    const size_t l0 = p0.contours.size(), l1 = p1.contours.size();
    SkPoint center0{0, 0}, center1{0, 0}, leftTop{SK_FloatInfinity, SK_FloatInfinity},
        rightBottom{SK_FloatNegativeInfinity, SK_FloatNegativeInfinity};
    for (const Contour &c0 : p0.contours)
    {
        SkPoint center = c0.getCenter();
        center0 += center;
        leftTop.fX = std::min(leftTop.fX, center.fX);
        leftTop.fY = std::min(leftTop.fY, center.fY);
    }
    for (const Contour &c1 : p1.contours)
    {
        SkPoint center = c1.getCenter();
        center1 += center;
        rightBottom.fX = std::max(rightBottom.fX, center.fX);
        rightBottom.fY = std::max(rightBottom.fY, center.fY);
    }
    center0 *= 1.0 / l0;
    center1 *= 1.0 / l1;
    const SkScalar scaledDist = distFactor / distanceSqd(leftTop, rightBottom);

    for (size_t i = 0; i < l0; ++i)
        for (size_t j = 0; j < l1; ++j)
            cost[i * l1 + j] = getCost(p0.contours[i], p1.contours[j], center0, center1, scaledDist);
}
