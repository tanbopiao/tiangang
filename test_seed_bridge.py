"""天罡外壳接通回归：种子 API（describe/run）必须走 guard.py 内核。"""
import unittest
from tiangang import Guardian


def probe_ok():
    return (True, 0, "全绿")


def probe_mild():
    return (False, 6, "端点失联")          # 未逾阈：七步治乱收口


def probe_severe():
    return (False, 10, "根本性偏差")        # 逾阈：上报体系总控


class T(unittest.TestCase):
    def test_describe_stage_m1(self):
        self.assertEqual(Guardian().describe()["stage"], "m1")

    def test_run_delegates_to_kernel(self):
        g = Guardian(probes={"p1": probe_ok})
        self.assertEqual(g.run(), [])  # 内核 sweep 结果原样透出

    def test_mild_incident_resolved_in_order(self):
        g = Guardian(probes={"p2": probe_mild})
        results = g.run()
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]["resolved"])
        self.assertFalse(results[0]["escalated"])
        self.assertEqual(g.reports, [])   # 未逾阈不上报

    def test_severe_incident_escalated_to_zongyuan(self):
        g = Guardian(probes={"p3": probe_severe})
        results = g.run()
        self.assertTrue(results[0]["escalated"])
        self.assertEqual(len(g.reports), 1)
        self.assertIn("上报体系总控", g.reports[0]["action"])


if __name__ == "__main__":
    unittest.main()
