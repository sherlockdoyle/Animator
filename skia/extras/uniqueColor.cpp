#include "common.h"
#include "include/core/SkColor.h"
#include <cfloat>

// The following contains relevant codes (simplified) to calculate rgb2hsluv and is copied from
// https://github.com/hsluv/hsluv-c/blob/59539e04a6fa648935cbe57c2104041f23136c4a/src/hsluv.c
// START OF COPY
/*
 * HSLuv-C: Human-friendly HSL
 * <https://github.com/hsluv/hsluv-c>
 * <https://www.hsluv.org/>
 *
 * Copyright (c) 2015 Alexei Boronine (original idea, JavaScript implementation)
 * Copyright (c) 2015 Roger Tallada (Obj-C implementation)
 * Copyright (c) 2017 Martin Mitas (C implementation, based on Obj-C implementation)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */
struct Triplet
{
    double a, b, c;
};
struct Bounds
{
    double a, b;
};

constexpr Triplet m[3] = {{3.24096994190452134377, -1.53738317757009345794, -0.49861076029300328366},
                          {-0.96924363628087982613, 1.87596750150772066772, 0.04155505740717561247},
                          {0.05563007969699360846, -0.20397695888897656435, 1.05697151424287856072}};
constexpr double ref_u = 0.19783000664283680764, ref_v = 0.46831999493879100370, kappa = 903.29629629629629629630,
                 epsilon = 0.00885645167903563082;

constexpr void get_bounds(const double l, Bounds bounds[6])
{
    const double tl = l + 16.0;
    const double sub1 = (tl * tl * tl) / 1560896.0;
    const double sub2 = sub1 > epsilon ? sub1 : (l / kappa);

    for (int channel = 0; channel < 3; ++channel)
    {
        const double m1 = m[channel].a;
        const double m2 = m[channel].b;
        const double m3 = m[channel].c;

        for (int t = 0; t < 2; ++t)
        {
            const double top1 = (284517.0 * m1 - 94839.0 * m3) * sub2;
            const double top2 = (838422.0 * m3 + 769860.0 * m2 + 731718.0 * m1) * l * sub2 - 769860.0 * t * l;
            const double bottom = (632260.0 * m3 - 126452.0 * m2) * sub2 + 126452.0 * t;

            bounds[channel * 2 + t].a = top1 / bottom;
            bounds[channel * 2 + t].b = top2 / bottom;
        }
    }
}

static double ray_length_until_intersect(const double theta, const Bounds *line)
{
    return line->b / (sin(theta) - line->a * cos(theta));
}

static double max_chroma_for_lh(const double l, const double h)
{
    double min_len = DBL_MAX;
    const double hrad = h * 0.01745329251994329577; // 2 * pi / 360
    Bounds bounds[6];

    get_bounds(l, bounds);
    for (int i = 0; i < 6; ++i)
    {
        const double len = ray_length_until_intersect(hrad, &bounds[i]);
        if (len >= 0 && len < min_len)
            min_len = len;
    }
    return min_len;
}

constexpr double dot_product(const Triplet *t1, const Triplet *t2)
{
    return t1->a * t2->a + t1->b * t2->b + t1->c * t2->c;
}

constexpr double from_linear(const double c)
{
    return c <= 0.0031308 ? (12.92 * c) : (1.055 * pow(c, 1.0 / 2.4) - 0.055);
}

constexpr void xyz2rgb(Triplet *in_out)
{
    const double r = from_linear(dot_product(&m[0], in_out));
    const double g = from_linear(dot_product(&m[1], in_out));
    const double b = from_linear(dot_product(&m[2], in_out));
    in_out->a = r;
    in_out->b = g;
    in_out->c = b;
}

constexpr double l2y(const double l)
{
    if (l <= 8.0)
        return l / kappa;
    else
    {
        const double x = (l + 16.0) / 116.0;
        return x * x * x;
    }
}

constexpr void luv2xyz(Triplet *in_out)
{
    if (in_out->a <= 0.00000001)
    {
        in_out->a = 0.0;
        in_out->b = 0.0;
        in_out->c = 0.0;
    }
    else
    {
        const double var_u = in_out->b / (13.0 * in_out->a) + ref_u;
        const double var_v = in_out->c / (13.0 * in_out->a) + ref_v;
        const double y = l2y(in_out->a);
        const double x = -(9.0 * y * var_u) / ((var_u - 4.0) * var_v - var_u * var_v);
        const double z = (9.0 * y - (15.0 * var_v * y) - (var_v * x)) / (3.0 * var_v);
        in_out->a = x;
        in_out->b = y;
        in_out->c = z;
    }
}

static void lch2luv(Triplet *in_out)
{
    const double hrad = in_out->c * 0.01745329251994329577; /* (pi / 180.0) */
    const double u = cos(hrad) * in_out->b;
    const double v = sin(hrad) * in_out->b;

    in_out->b = u;
    in_out->c = v;
}

constexpr void hsluv2lch(Triplet *in_out)
{
    double h = in_out->a;
    const double s = in_out->b;
    const double l = in_out->c;
    const double c = l > 99.9999999 || l < 0.00000001 ? 0.0 : (max_chroma_for_lh(l, h) / 100.0 * s);

    if (s < 0.00000001)
        h = 0.0;

    in_out->a = l;
    in_out->b = c;
    in_out->c = h;
}

static inline void hsluv2rgb(Triplet *tmp)
{
    hsluv2lch(tmp);
    lch2luv(tmp);
    luv2xyz(tmp);
    xyz2rgb(tmp);
}
// END OF COPY

void initUniqueColor(py::module &m)
{
    m.def(
        "uniqueColor",
        [](const double &l, const double &s)
        {
            static double h = 0;
            Triplet hsluv = {h, s, l};
            hsluv2rgb(&hsluv);
            h = fmod(h + 222.492235949962145 /* 360 / golden_ratio */, 360);
            return SkColor4f{static_cast<float>(hsluv.a), static_cast<float>(hsluv.b), static_cast<float>(hsluv.c),
                             1.0f};
        },
        R"doc(
            Returns a unique color every time it is called. Uses HSLuv (https://www.hsluv.org/) internally.

            :param l: Lightness of the generated color. Must be between 0 and 100. Interesting values: 50, 71, 76.
            :param s: Saturation of the generated color. Must be between 0 and 100.
            :return: A tuple of (r, g, b, a). a is always 1.
        )doc",
        "l"_a = 71, "s"_a = 100);
}