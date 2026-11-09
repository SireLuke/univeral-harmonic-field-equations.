"""PAN-UDFE-SPEC-001 acceptance tests UDFE-001..010 (reference level). A test passes only when executed."""
import math, unittest
from pan_harmonics.udfe import qubit, graph, dissipation, coupling
from pan_harmonics.udfe.common import UdfeError

E_GAP = {"value": 1.6e-19, "unit": "J"}
R0 = qubit.state(0.5, 0.5)            # equal superposition in the energy basis, C(0) = 1

class TestUDFE(unittest.TestCase):
    def test_001_pure_dephasing_reduces_coherence(self):
        ts = [0, 0.5, 1, 2, 4]
        hc = [qubit.retention(qubit.analytic(R0, t, 0.0, 0.8), R0) for t in ts]
        self.assertTrue(all(a > b for a, b in zip(hc, hc[1:])))
        for t, h in zip(ts, hc): self.assertAlmostEqual(h, math.exp(-0.8 * t), places=12)
        # independent check: RK4 Lindblad integration agrees with the closed form
        n = qubit.lindblad(R0, 2.0, 0.0, 0.8, omega=3.0); a = qubit.analytic(R0, 2.0, 0.0, 0.8, omega=3.0)
        self.assertLess(max(abs(n[i][j] - a[i][j]) for i in range(2) for j in range(2)), 1e-9)

    def test_002_pure_dephasing_preserves_energy_and_populations(self):
        e0 = qubit.energy(R0, E_GAP)
        for t in (0.3, 1.0, 5.0):
            r = qubit.analytic(R0, t, 0.0, 0.8)
            self.assertAlmostEqual(r[0][0].real, 0.5, places=14)
            self.assertAlmostEqual(qubit.energy(r, E_GAP), e0, places=30)
        # in the declared energy eigenbasis only; dephasing along another axis would not conserve energy
        self.assertIn("energy eigenbasis", qubit.BASIS)

    def test_003_amplitude_damping_populations_energy_and_rate_relation(self):
        g1 = 0.6; t = 1.7; r = qubit.analytic(R0, t, g1, 0.0)
        self.assertAlmostEqual(r[0][0].real, 0.5 * math.exp(-g1 * t), places=14)
        self.assertLess(qubit.energy(r, E_GAP), qubit.energy(R0, E_GAP))
        # coherence decays at G1/2 with no pure dephasing, i.e. G2 = G1/2 + Gphi (Markovian qubit)
        self.assertAlmostEqual(qubit.retention(r, R0), math.exp(-g1 / 2 * t), places=12)
        n = qubit.lindblad(R0, t, g1, 0.0)
        self.assertAlmostEqual(qubit.coherence_l1(n), qubit.coherence_l1(r), places=9)
        self.assertTrue(dissipation.rates_consistency(g1, 0.3, g1 / 2 + 0.3, "markovian_qubit")["consistent"])
        with self.assertRaises(UdfeError): dissipation.rates_consistency(1, 1, 1.5, "arbitrary_system")

    def test_004_edge_removal_changes_graph_integrity(self):
        g0 = graph.ring(8); m0 = graph.metrics(g0, g0)
        self.assertEqual((m0["giant_component_ratio"], m0["fragmentation_measure"], m0["functional_retention"]), (1, 0, 1))
        self.assertAlmostEqual(m0["algebraic_connectivity"], 1.0, places=12)
        one = graph.metrics(g0.remove([(0, 1)]), g0); two = graph.metrics(g0.remove([(0, 1), (4, 5)]), g0)
        self.assertLess(one["algebraic_connectivity"], 1.0); self.assertEqual(two["algebraic_connectivity"], 0.0)
        self.assertEqual(two["giant_component_ratio"], 0.5); self.assertAlmostEqual(two["functional_retention"], 12 / 28, places=12)

    def test_004b_laplacian_spectrum_matches_closed_forms(self):
        for n in (5, 8, 11):
            self.assertAlmostEqual(graph.algebraic_connectivity(graph.ring(n)), 2 - 2 * math.cos(2 * math.pi / n), places=9)
            self.assertAlmostEqual(graph.algebraic_connectivity(graph.path(n)), 2 - 2 * math.cos(math.pi / n), places=9)
            self.assertAlmostEqual(graph.algebraic_connectivity(graph.complete(n)), n, places=9)
        full = graph.grid(4, 4)   # removing edges never increases lambda_2; lam = graph.algebraic_connectivity(full); cur = full
        for e in full.edges()[:5]:
            cur = cur.remove([e]); l = graph.algebraic_connectivity(cur); self.assertLessEqual(l, lam + 1e-9); lam = l

    def test_005_dissolution_without_quantum_inputs(self):
        g0 = graph.grid(4, 4); res = graph.evaluate(g0, g0.remove([(0, 1), (0, 4)]))
        self.assertGreater(res["dissolution_index"], 0)
        self.assertEqual(res["provenance"]["evidence"], "HYPOTHESIS")
        self.assertEqual(sum(res["components"].values()), res["dissolution_index"])
        self.assertIsNone(res["measurement_confidence"])            # not assessed; not silently zero
        for key in ("dissolution_index", "giant_component_ratio", "algebraic_connectivity", "fragmentation_measure", "functional_retention", "recovery_threshold", "measurement_confidence"):
            self.assertIn(key, res)

    def test_006_dissipation_without_structure(self):
        out = dissipation.evaluate({"value": 3e-19, "unit": "J"}, {"value": 1e-19, "unit": "J"}, {"value": 2e-19, "unit": "J"}, {"value": 4e-19, "unit": "J"},
                                   2.0, "qubit plus drive", "positive_into_system", {"value": 0.0, "unit": "J"})
        self.assertAlmostEqual(out["energy_balance"], 0.0, places=30); self.assertAlmostEqual(out["power_transfer_w"], 1e-19, places=30)
        self.assertAlmostEqual(out["heat_flow"], 2e-19, places=30); self.assertIsNone(out["entropy_production"])
        self.assertEqual(dissipation.heat_flow({"value": 2e-19, "unit": "J"}, "positive_out_of_system", {"value": 0.0, "unit": "J"}), -2e-19)
        with self.assertRaises(UdfeError): dissipation.heat_flow({"value": 1e-19, "unit": "J"}, "positive_into_system")   # work must be declared

    def test_007_coupling_reports_association_not_causation(self):
        t = [0, 1, 2, 3, 4, 5]
        r = coupling.analyze({"D_org": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5], "P_diss": [0.0, 0.2, 0.4, 0.6, 0.8, 1.0], "D_C": [0, .2, .3, .5, .6, .9]})
        self.assertEqual(r["outcome"], "correlated_dissolution_and_dissipation"); self.assertIs(r["causal_claim"], False)
        self.assertEqual(coupling.analyze({"D_org": [0, .1, .2, .3], "P_diss": [.5, .5, .5, .5]})["outcome"], "dissolution_without_measurable_dissipation")
        self.assertEqual(coupling.analyze({"D_org": [.2, .2, .2, .2], "P_diss": [0, .1, .2, .3]})["outcome"], "dissipation_without_measurable_dissolution")
        self.assertEqual(coupling.analyze({"D_org": [0, .4, .0, .4, .0], "P_diss": [0, .0, .4, .4, .2]}, corr_threshold=0.9)["outcome"], "weak_or_absent_coupling")
        self.assertIsNone(coupling.analyze({"D_org": [1, 1, 1], "P_diss": [1, 2, 3]})["pairs"]["D_org~P_diss"]["pearson"])    # undefined, not 0
        self.assertEqual(coupling.analyze({"D_C": [0, 1, 2], "D_org": [2, 1, 0]})["unavailable"], ["P_diss"])
        with self.assertRaises(UdfeError): coupling.analyze({"D_C": [0, 1, 2]})

    def test_008_recovery_tracked_separately(self):
        # coherence can recover while structure stays fragmented: a qubit with C restored, graph still broken
        r_before, r_after = qubit.analytic(R0, 3.0, 0.2, 0.5), R0
        self.assertGreater(qubit.retention(r_after, R0), qubit.retention(r_before, R0))
        g0 = graph.ring(8); broken = g0.remove([(0, 1), (4, 5)])
        self.assertEqual(graph.evaluate(g0, broken, restore_order=[], tolerance=0.01)["recovery_threshold"], None)   # never recovers without restoration
        self.assertEqual(graph.evaluate(g0, broken, restore_order=[(0, 1), (4, 5)], tolerance=1e-9)["recovery_threshold"], 2)
        self.assertEqual(graph.evaluate(g0, broken, restore_order=[(0, 1), (4, 5)], tolerance=0.5)["recovery_threshold"] <= 1, True)

    def test_009_invalid_missing_and_incompatible_inputs_rejected(self):
        for bad in (float("nan"), float("inf"), "x", True):
            with self.assertRaises(UdfeError): qubit.analytic(R0, bad, 0.1, 0.1)
        with self.assertRaises(UdfeError): qubit.analytic(R0, 1.0, -0.1, 0.1)
        with self.assertRaises(UdfeError): qubit.run_experiment({"name": "x"})                               # missing metadata
        with self.assertRaises(UdfeError): qubit.energy(R0, {"value": 1.0, "unit": "s"})                   # incompatible unit
        with self.assertRaises(UdfeError): qubit.energy(R0, 1.6e-19)                                         # unitless quantity
        with self.assertRaises(UdfeError): qubit.retention(qubit.state(0.5, 0.0), qubit.state(0.5, 0.0))     # C(0) = 0
        with self.assertRaises(UdfeError): graph.dissolution_index({"giant_component_ratio": 1, "algebraic_connectivity": 1, "fragmentation_measure": 0, "functional_retention": 1}, (0.5, 0.5, 0.5, 0.5))
        with self.assertRaises(UdfeError): dissipation.energy_balance({"value": 1, "unit": "J"}, {"value": 1, "unit": "J"}, {"value": 0, "unit": "J"}, "")
        with self.assertRaises(UdfeError): graph.metrics(graph.path(4).remove([(1, 2)]), graph.path(4).remove([(1, 2)]))   # disconnected baseline

    def test_010_determinism_and_provenance(self):
        cfg = {"name": "A", "e_gap": E_GAP, "p_excited": 0.5, "c0": 0.5, "gamma_1": 0.0, "gamma_phi": 0.8, "times": [0, 1, 2]}
        a, b = qubit.run_experiment(cfg), qubit.run_experiment(cfg)
        self.assertEqual(a, b); self.assertEqual(a["provenance"]["config_sha256"], b["provenance"]["config_sha256"])
        self.assertEqual(a["provenance"]["evidence"], "ESTABLISHED"); self.assertIn("energy eigenbasis", a["basis"])
        g1, g2 = graph.gnp(12, 0.5, seed=3), graph.gnp(12, 0.5, seed=3)
        self.assertEqual(g1.edges(), g2.edges())
        self.assertEqual(graph.evaluate(graph.ring(10), graph.ring(10).remove([(0, 1)])), graph.evaluate(graph.ring(10), graph.ring(10).remove([(0, 1)])))

if __name__ == "__main__": unittest.main()
