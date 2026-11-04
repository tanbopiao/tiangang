import unittest
from guard import TiangangGuard, ESCALATION_THRESHOLD

class T(unittest.TestCase):
    def test_all_green_quiet_sweep(self):
        g = TiangangGuard(probes={"门禁": lambda: (True, 0, "正常")})
        self.assertEqual(g.sweep(), [])
    def test_fault_detected_and_resolved(self):
        def broken(): return (False, 4, "服务无响应")
        g = TiangangGuard(probes={"围栏服务": broken})
        out = g.sweep()
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0]["resolved"]); self.assertFalse(out[0]["escalated"])
        self.assertEqual(g.reports, [])            # 常规故障不上报
    def test_severe_fault_escalates_to_zongyuan(self):
        def critical(): return (False, ESCALATION_THRESHOLD, "内核基准被改")
        g = TiangangGuard(probes={"真值库": critical})
        out = g.sweep()
        self.assertTrue(out[0]["escalated"]); self.assertFalse(out[0]["resolved"])
        self.assertEqual(len(g.reports), 1)        # 越阈必上报，台账留痕
        self.assertIn("体系总控", g.reports[0]["action"])
    def test_mixed_patrol(self):
        g = TiangangGuard(probes={
            "心跳": lambda: (True, 0, "正常"),
            "档案": lambda: (False, 3, "快照滞后")})
        out = g.sweep()
        self.assertEqual(len(out), 1)              # 绿的不生成事件

if __name__ == "__main__":
    unittest.main()
