import sys
if sys.path[0] != "../..":
    sys.path.insert(0, "../..")

import unittest

from pyx import *
from pyx.path import *
from pyx.normpath import normpathparam
import math
set(epsilon=1e-7)

class NormpathTestCase(unittest.TestCase):

    def assertAlmostEqualNormsubpathitem(self, nspi1, nspi2):
        if isinstance(nspi1, normline_pt):
            assert isinstance(nspi2, normline_pt), "%s != %s" % (nspi1, nspi2)
            self.assertAlmostEqual(nspi1.x0_pt, nspi2.x0_pt)
            self.assertAlmostEqual(nspi1.y0_pt, nspi2.y0_pt)
            self.assertAlmostEqual(nspi1.x1_pt, nspi2.x1_pt)
            self.assertAlmostEqual(nspi1.y1_pt, nspi2.y1_pt)
        else:
            assert isinstance(nspi1, normcurve_pt), "%s != %s" % (nspi1, nspi2)
            assert isinstance(nspi2, normcurve_pt), "%s != %s" % (nspi1, nspi2)
            self.assertAlmostEqual(nspi1.x0_pt, nspi2.x0_pt)
            self.assertAlmostEqual(nspi1.y0_pt, nspi2.y0_pt)
            self.assertAlmostEqual(nspi1.x1_pt, nspi2.x1_pt)
            self.assertAlmostEqual(nspi1.y1_pt, nspi2.y1_pt)
            self.assertAlmostEqual(nspi1.x2_pt, nspi2.x2_pt)
            self.assertAlmostEqual(nspi1.y2_pt, nspi2.y2_pt)
            self.assertAlmostEqual(nspi1.x3_pt, nspi2.x3_pt)
            self.assertAlmostEqual(nspi1.y3_pt, nspi2.y3_pt)

    def assertAlmostEqualNormsubpath(self, nsp1, nsp2):
        assert len(nsp1) == len(nsp2), "%s != %s" % (nsp1, nsp2)
        assert nsp1.closed == nsp2.closed, "%s != %s" % (nsp1, nsp2)
        for nspi1, nspi2 in zip(nsp1, nsp2):
            self.assertAlmostEqualNormsubpathitem(nspi1, nspi2)

    def assertAlmostEqualNormpath(self, np1, np2):
        assert len(np1) == len(np2), "%s != %s" % (np1, np2)
        for nsp1, nsp2 in zip(np1, np2):
            self.assertAlmostEqualNormsubpath(nsp1, nsp2)

    def testparam(self):
        p = ( normpath([normsubpath([normline_pt(0, 0, 10, 0),
                                   normline_pt(10, 0, 10, 20),
                                   normline_pt(10, 20, 0, 20),
                                   normline_pt(0, 20, 0, 0)], closed=1)]) +
              circle_pt(0, 0, 10) +
              line_pt(0, 0, 2, 0))

        param = normpathparam(p, 0, 1.5)
        param = param + 0
        self.assertEqual(param.normsubpathindex, 0)
        self.assertAlmostEqual(param.normsubpathparam, 1.5)
        param = param + 15 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 0)
        self.assertAlmostEqual(param.normsubpathparam, 2.5)
        param += 24.9 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 0)
        self.assertAlmostEqual(param.normsubpathparam, 3.995)
        param = 0.1 * unit.t_pt + param
        self.assertEqual(param.normsubpathindex, 1)
        self.assertAlmostEqual(param.normsubpathparam, 0)
        param = param + 0.5*circle_pt(0, 0, 10).arclen()
        circlerange = len(p.normsubpaths[1])
        self.assertEqual(param.normsubpathindex, 1)
        self.assertAlmostEqual(param.normsubpathparam, 0.5*circlerange, 4)
        param = param + 0.5*circle_pt(0, 0, 10).arclen()
        param = param + 2 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 2)
        self.assertAlmostEqual(param.normsubpathparam, 1, 4)
        param = param + 1 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 2)
        self.assertAlmostEqual(param.normsubpathparam, 1.5, 4)

        param = normpathparam(p, 0, 1.5)
        param = param - 15 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 0)
        self.assertAlmostEqual(param.normsubpathparam, 0.5)
        param -= 10 * unit.t_pt
        self.assertEqual(param.normsubpathindex, 0)
        self.assertAlmostEqual(param.normsubpathparam, -0.5)
        
        param = normpathparam(p, 0, 1.2)
        param2 = 2*param
        param += param
        self.assertEqual(param.normsubpathindex, param2.normsubpathindex)
        self.assertEqual(param.normsubpathparam, param2.normsubpathparam)

        param = normpathparam(p, 0, 1.2)
        self.assertTrue(param < 15 * unit.t_pt)
        self.assertTrue(15 * unit.t_pt > param)
        self.assertTrue(param > 12 * unit.t_pt)
        self.assertTrue(12 * unit.t_pt < param)
        self.assertTrue(param < 1)
        self.assertTrue(1 > param)

    def testat(self):
        p = normpath([normsubpath([normline_pt(0, 0, 10, 0),
                                   normline_pt(10, 0, 10, 20),
                                   normline_pt(10, 20, 0, 20),
                                   normline_pt(0, 20, 0, 0)], closed=1)])
        params = [-5, 0, 5, 10, 20, 30, 35, 40, 50, 60, 70]
        ats = (-5, 0), (0, 0), (5, 0), (10, 0), (10, 10), (10, 20), (5, 20), (0, 20), (0, 10), (0, 0), (0, -10)
        for param, (at_x, at_y) in zip(params, ats):
            self.assertAlmostEqual(p.at_pt(param)[0], at_x)
            self.assertAlmostEqual(p.at_pt(param)[1], at_y)
        for (at_x, at_y), (at2_x, at2_y) in zip(p.at_pt(params), ats):
            self.assertAlmostEqual(at_x, at2_x)
            self.assertAlmostEqual(at_y, at2_y)
        p = normpath([normsubpath([normline_pt(0, 0, 3, 0),
                                   normcurve_pt(3, 0, 3, 2, 3, 4, 3, 6),
                                   normcurve_pt(3, 6, 2, 6, 1, 6, 0, 6),
                                   normline_pt(0, 6, 0, 0)], closed=1)])
        self.assertAlmostEqual(p.at_pt(6)[0], 3)
        self.assertAlmostEqual(p.at_pt(6)[1], 3)
        self.assertAlmostEqual(p.at_pt(4.5)[0], 3)
        self.assertAlmostEqual(p.at_pt(4.5)[1], 1.5)

    def testarclentoparam(self):
        p = ( normpath([normsubpath([normline_pt(0, 0, 10, 0),
                                   normline_pt(10, 0, 10, 20),
                                   normline_pt(10, 20, 0, 20),
                                   normline_pt(0, 20, 0, 0)], closed=1)]) +
              circle_pt(0, 0, 10) +
              line_pt(0, 0, 2, 0))

        arclens_pt = [20, 30, -2, 61, 100, 200, -30, 1000]
        for arclen_pt, arclen2_pt in zip(arclens_pt, p.paramtoarclen_pt(p.arclentoparam_pt(arclens_pt))):
            self.assertAlmostEqual(arclen_pt, arclen2_pt, 4)

        arclens = [x*unit.t_pt for x in [20, 30, -2, 61, 100, 200, -30, 1000]]
        for arclen, arclen2 in zip(arclens, p.paramtoarclen(p.arclentoparam(arclens))):
            self.assertAlmostEqual(unit.tom(arclen), unit.tom(arclen2), 4)

    def testsplit(self):
        p = normline_pt(0, 0, 10, 0)
        self.assertRaises(ValueError, p.segments, [])
        self.assertRaises(ValueError, p.segments, [0.2])
        s = p.segments([0.2, 0.8])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpathitem(s[0], normline_pt(2, 0, 8, 0))
        s = p.segments([-0.2, 1.8])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpathitem(s[0], normline_pt(-2, 0, 18, 0))

        p = normcurve_pt(0, 0, 10, 0, 20, 0, 30, 0)
        self.assertRaises(ValueError, p.segments, [])
        self.assertRaises(ValueError, p.segments, [0.2])
        s = p.segments([0.2, 0.8])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpathitem(s[0], normcurve_pt(6, 0, 12, 0, 18, 0, 24, 0))
        s = p.segments([-0.2, 1.8])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpathitem(s[0], normcurve_pt(-6, 0, 14, 0, 34, 0, 54, 0))

        p = normsubpath([normline_pt(0, 0, 1, 0),
                         normline_pt(1, 0, 1, 1),
                         normline_pt(1, 1, 0, 1),
                         normline_pt(0, 1, 0, 0)])
        self.assertRaises(ValueError, p.segments, [])
        self.assertRaises(ValueError, p.segments, [0.2])
        s = p.segments([0.5, 2.5])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0.5, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0.5, 1)]))
        s = p.segments([4.5, -1])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0, -0.5, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, -1, 0)]))
        s = p.segments([0, 0.1, 1.2, 1.3, 3.4, 0.5, 4])
        self.assertEqual(len(s), 6)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0, 0, 0.1, 0)]))
        self.assertAlmostEqualNormsubpath(s[1], normsubpath([normline_pt(0.1, 0, 1, 0), normline_pt(1, 0, 1, 0.2)]))
        self.assertAlmostEqualNormsubpath(s[2], normsubpath([normline_pt(1, 0.2, 1, 0.3)]))
        self.assertAlmostEqualNormsubpath(s[3], normsubpath([normline_pt(1, 0.3, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.6)]))
        self.assertAlmostEqualNormsubpath(s[4], normsubpath([normline_pt(0, 0.6, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, 0.5, 0)]))
        self.assertAlmostEqualNormsubpath(s[5], normsubpath([normline_pt(0.5, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0)]))

        p = normsubpath([normline_pt(0, 0, 1, 0),
                         normline_pt(1, 0, 1, 1),
                         normline_pt(1, 1, 0, 1)], closed=1)
        self.assertRaises(ValueError, p.segments, [])
        self.assertRaises(ValueError, p.segments, [0.5])
        s = p.segments([0.5, 2.5])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0.5, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0.5, 1)]))
        s = p.segments([4.5, -1])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0, -0.5, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, -1, 0)]))
        s = p.segments([0, 0.1, 1.2, 1.3, 3.4, 0.5, 4])
        self.assertEqual(len(s), 5)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0.5, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0), normline_pt(0, 0, 0.1, 0)]))
        self.assertAlmostEqualNormsubpath(s[1], normsubpath([normline_pt(0.1, 0, 1, 0), normline_pt(1, 0, 1, 0.2)]))
        self.assertAlmostEqualNormsubpath(s[2], normsubpath([normline_pt(1, 0.2, 1, 0.3)]))
        self.assertAlmostEqualNormsubpath(s[3], normsubpath([normline_pt(1, 0.3, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.6)]))
        self.assertAlmostEqualNormsubpath(s[4], normsubpath([normline_pt(0, 0.6, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, 0.5, 0)]))
        s = p.segments([4, 0.1, 1.2, 1.3, 3.4, 0.5, 0])
        self.assertEqual(len(s), 5)
        self.assertAlmostEqualNormsubpath(s[0], normsubpath([normline_pt(0.5, 0, 0, 0), normline_pt(0, 0, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, 0.1, 0)]))
        self.assertAlmostEqualNormsubpath(s[1], normsubpath([normline_pt(0.1, 0, 1, 0), normline_pt(1, 0, 1, 0.2)]))
        self.assertAlmostEqualNormsubpath(s[2], normsubpath([normline_pt(1, 0.2, 1, 0.3)]))
        self.assertAlmostEqualNormsubpath(s[3], normsubpath([normline_pt(1, 0.3, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.6)]))
        self.assertAlmostEqualNormsubpath(s[4], normsubpath([normline_pt(0, 0.6, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, 0.5, 0)]))

        p = normpath([normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 2, 0), normline_pt(2, 0, 3, 0), normline_pt(3, 0, 4, 0)]),
                      normsubpath([normline_pt(0, 1, 1, 1), normline_pt(1, 1, 2, 1), normline_pt(2, 1, 3, 1), normline_pt(3, 1, 4, 1)]),
                      normsubpath([normline_pt(0, 2, 1, 2), normline_pt(1, 2, 2, 2), normline_pt(2, 2, 3, 2), normline_pt(3, 2, 4, 2)]),
                      normsubpath([normline_pt(0, 3, 1, 3), normline_pt(1, 3, 2, 3), normline_pt(2, 3, 3, 3), normline_pt(3, 3, 4, 3)]),
                      normsubpath([normline_pt(0, 4, 1, 4), normline_pt(1, 4, 2, 4), normline_pt(2, 4, 3, 4), normline_pt(3, 4, 4, 4)])])
        s = p.split([normpathparam(p, 3, 0.1),
                     normpathparam(p, 4, 1.2),
                     normpathparam(p, 2, 2.3),
                     normpathparam(p, 0, 3.4),
                     normpathparam(p, 1, 0.5)])
        self.assertEqual(len(s), 6)
        self.assertAlmostEqualNormpath(s[0], normpath([normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 2, 0), normline_pt(2, 0, 3, 0), normline_pt(3, 0, 4, 0)]),
                                                           normsubpath([normline_pt(0, 1, 1, 1), normline_pt(1, 1, 2, 1), normline_pt(2, 1, 3, 1), normline_pt(3, 1, 4, 1)]),
                                                           normsubpath([normline_pt(0, 2, 1, 2), normline_pt(1, 2, 2, 2), normline_pt(2, 2, 3, 2), normline_pt(3, 2, 4, 2)]),
                                                           normsubpath([normline_pt(0, 3, 0.1, 3)])]))
        self.assertAlmostEqualNormpath(s[1], normpath([normsubpath([normline_pt(0.1, 3, 1, 3), normline_pt(1, 3, 2, 3), normline_pt(2, 3, 3, 3), normline_pt(3, 3, 4, 3)]),
                                                           normsubpath([normline_pt(0, 4, 1, 4), normline_pt(1, 4, 1.2, 4)])]))
        self.assertAlmostEqualNormpath(s[2], normpath([normsubpath([normline_pt(1.2, 4, 1, 4), normline_pt(1, 4, 0, 4)]),
                                                           normsubpath([normline_pt(4, 3, 3, 3), normline_pt(3, 3, 2, 3), normline_pt(2, 3, 1, 3), normline_pt(1, 3, 0, 3)]),
                                                           normsubpath([normline_pt(4, 2, 3, 2), normline_pt(3, 2, 2.3, 2)])]))
        self.assertAlmostEqualNormpath(s[3], normpath([normsubpath([normline_pt(2.3, 2, 2, 2), normline_pt(2, 2, 1, 2), normline_pt(1, 2, 0, 2)]),
                                                           normsubpath([normline_pt(4, 1, 3, 1), normline_pt(3, 1, 2, 1), normline_pt(2, 1, 1, 1), normline_pt(1, 1, 0, 1)]),
                                                           normsubpath([normline_pt(4, 0, 3.4, 0)])]))
        self.assertAlmostEqualNormpath(s[4], normpath([normsubpath([normline_pt(3.4, 0, 4, 0)]),
                                                           normsubpath([normline_pt(0, 1, 0.5, 1)])]))
        self.assertAlmostEqualNormpath(s[5], normpath([normsubpath([normline_pt(0.5, 1, 1, 1), normline_pt(1, 1, 2, 1), normline_pt(2, 1, 3, 1), normline_pt(3, 1, 4, 1)]),
                                                           normsubpath([normline_pt(0, 2, 1, 2), normline_pt(1, 2, 2, 2), normline_pt(2, 2, 3, 2), normline_pt(3, 2, 4, 2)]),
                                                           normsubpath([normline_pt(0, 3, 1, 3), normline_pt(1, 3, 2, 3), normline_pt(2, 3, 3, 3), normline_pt(3, 3, 4, 3)]),
                                                           normsubpath([normline_pt(0, 4, 1, 4), normline_pt(1, 4, 2, 4), normline_pt(2, 4, 3, 4), normline_pt(3, 4, 4, 4)])]))

        p = normpath([normsubpath([normline_pt(0, -5, 1, -5)]),
                      normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1)], closed=1),
                      normsubpath([normline_pt(0, 5, 1, 5)])])
        s = p.split([normpathparam(p, 1, 3.5)])
        self.assertEqual(len(s), 1)
        self.assertAlmostEqualNormpath(s[0], normpath([normsubpath([normline_pt(0, -5, 1, -5)]),
                                                           normsubpath([normline_pt(0, 0.5, 0, 0), normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.5)]),
                                                           normsubpath([normline_pt(0, 5, 1, 5)])]))

        p = normpath([normsubpath([normline_pt(0, -5, 1, -5)]),
                      normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1)], closed=1),
                      normsubpath([normline_pt(0, 5, 1, 5)])])
        s = p.split([normpathparam(p, 0, 0.5),
                     normpathparam(p, 1, 3.5),
                     normpathparam(p, 0, 0.5),
                     normpathparam(p, 2, 0.5)])
        self.assertEqual(len(s), 5)
        self.assertAlmostEqualNormpath(s[0], normpath([normsubpath([normline_pt(0, -5, 0.5, -5)])]))
        self.assertAlmostEqualNormpath(s[1], normpath([normsubpath([normline_pt(0.5, -5, 1, -5)]),
                                                           normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.5)])]))
        # XXX should we do ???: normsubpath([normline_pt(0, 0.5, 0, 0), normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0.5)])]))
        # same question in the next line ...
        self.assertAlmostEqualNormpath(s[2], normpath([normsubpath([normline_pt(0, 0.5, 0, 1), normline_pt(0, 1, 1, 1), normline_pt(1, 1, 1, 0), normline_pt(1, 0, 0, 0)]),
                                                           normsubpath([normline_pt(1, -5, 0.5, -5)])]))
        self.assertAlmostEqualNormpath(s[3], normpath([normsubpath([normline_pt(0.5, -5, 1, -5)]),
                                                           normsubpath([normline_pt(0, 0, 1, 0), normline_pt(1, 0, 1, 1), normline_pt(1, 1, 0, 1), normline_pt(0, 1, 0, 0)], closed=1),
                                                           normsubpath([normline_pt(0, 5, 0.5, 5)])]))
        self.assertAlmostEqualNormpath(s[4], normpath([normsubpath([normline_pt(0.5, 5, 1, 5)])]))

    def testshortnormsubpath(self):
        sp = normsubpath(epsilon=1)
        sp.append(normline_pt(0, 0, 0.5, 0))
        sp.append(normline_pt(0.5, 0, 1.5, 0))

        sp.append(normline_pt(1.5, 0, 1.5, 0.3))
        sp.append(normline_pt(1.5, 0.3, 1.5, 0.6))
        sp.append(normline_pt(1.5, 0.6, 1.5, 0.9))
        sp.append(normline_pt(1.5, 0.9, 1.5, 1.2))

        sp.append(normline_pt(1.5, 1.2, 1.3, 1.6))
        sp.append(normcurve_pt(1.3, 1.6, 1.4, 1.7, 1.3, 1.7, 1.3, 1.8))
        sp.append(normcurve_pt(1.3, 1.8, 2.4, 2.7, 3.3, 3.7, 1.4, 1.8))

        self.assertAlmostEqualNormsubpath(sp, normsubpath([normline_pt(0, 0, 1.5, 0), normline_pt(1.5, 0, 1.5, 1.2), normcurve_pt(1.5, 1.2, 2.4, 2.7, 3.3, 3.7, 1.4, 1.8)]))

    def testintersectnormsubpath(self):
        smallposy = 0.09
        smallnegy = -0.01
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=0)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 2)
        self.assertAlmostEqual(intersect[0][0], 0.9)
        self.assertAlmostEqual(intersect[0][1], 2.99)

        smallposy = 0.09
        smallnegy = -0.01
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=1)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 2)
        self.assertAlmostEqual(intersect[0][0], 0.9)
        self.assertAlmostEqual(intersect[0][1], 2.99)

        smallposy = 0.01
        smallnegy = -0.09
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=0)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 4)
        self.assertAlmostEqual(intersect[0][0], 0.1)
        self.assertAlmostEqual(intersect[0][1], 1.09)
        self.assertAlmostEqual(intersect[0][2], 2.91)
        self.assertAlmostEqual(intersect[0][3], 3.9)

        smallposy = 0.01
        smallnegy = -0.09
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=1)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 3)
        self.assertAlmostEqual(intersect[0][0], 0.1)
        self.assertAlmostEqual(intersect[0][1], 1.09)
        self.assertAlmostEqual(intersect[0][2], 2.91)

        smallposy = 0.01
        smallnegy = -0.01
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=0)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 2)
        self.assertAlmostEqual(intersect[0][0], 0.5)
        self.assertAlmostEqual(intersect[0][1], 2.99)

        smallposy = 0.01
        smallnegy = -0.01
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=1)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 1)
        self.assertAlmostEqual(intersect[0][0], 0.5)

        smallposy = 0.1
        smallnegy = -0.1
        p1 = normsubpath([normline_pt(-1, 0, 1, 0)])
        p2 = normsubpath([normline_pt(0, smallposy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, 1+smallnegy),
                          normline_pt(0, 1+smallnegy, 0, smallnegy),
                          normline_pt(0, smallnegy, 0, smallposy)], closed=0)
        p1.epsilon = p2.epsilon = 0.05
        intersect = p2.intersect(p1)
        self.assertEqual(len(intersect[0]), 4)
        self.assertAlmostEqual(intersect[0][0], 0.5)
        self.assertAlmostEqual(intersect[0][1], 1.1)
        self.assertAlmostEqual(intersect[0][2], 2.9)
        self.assertAlmostEqual(intersect[0][3], 3.5)


if __name__ == "__main__":
    unittest.main()
