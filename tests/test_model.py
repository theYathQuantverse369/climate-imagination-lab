import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from server import CITIES, scenario

class ScenarioModelTests(unittest.TestCase):
    def test_all_cities_return_five_bounded_signals(self):
        for city in CITIES:
            result = scenario(city=city)
            self.assertEqual(len(result["risks"]), 5)
            self.assertTrue(all(0 <= score <= 100 for score in result["risks"].values()))

    def test_more_warming_does_not_lower_heat_signal(self):
        low = scenario(city="Delhi", warming=1)["risks"]["Heat stress"]
        high = scenario(city="Delhi", warming=3)["risks"]["Heat stress"]
        self.assertGreater(high, low)

    def test_adaptation_reduces_its_named_pressure(self):
        baseline = scenario(city="Chennai", adaptation="none")
        shade = scenario(city="Chennai", adaptation="shade")
        self.assertLess(shade["risks"]["Heat stress"], baseline["risks"]["Heat stress"])

    def test_expanded_rainfall_and_time_choices_are_accepted(self):
        for rainfall in (70, 85, 100, 115, 130):
            for year in (2030, 2040, 2050, 2070, 2090):
                result = scenario(rainfall=rainfall, year=year)
                self.assertEqual(result["rainfall"], rainfall)
                self.assertEqual(result["year"], year)

    def test_all_adaptation_ideas_are_accepted(self):
        for action in ("shade", "cool_roofs", "drainage", "wetlands", "permeable",
                       "cooling_centres", "early_warning", "transit", "water_saving"):
            with self.subTest(action=action):
                self.assertEqual(scenario(adaptation=action)["adaptation"], action)

    def test_reference_curve_matches_chennai_investment_example(self):
        result = scenario(city="Chennai", warming=3, rainfall=100, year=2050, investment=65)
        self.assertEqual(result["risks"]["Flood exposure"], 46)
        at_three = {key: next(p["risk"] for p in series if p["warming"] == 3)
                    for key, series in result["curve"].items()}
        self.assertGreaterEqual(at_three["temperature"], 60)
        self.assertGreaterEqual(at_three["flood_unmitigated"], 60)
        self.assertEqual(at_three["flood_invested"], 46)
        self.assertTrue(55 <= at_three["people_affected"] <= 60)

    def test_investment_slider_changes_flood_score(self):
        no_investment = scenario(city="Chennai", warming=3, investment=0)
        invested = scenario(city="Chennai", warming=3, investment=65)
        self.assertGreater(no_investment["risks"]["Flood exposure"], invested["risks"]["Flood exposure"])

    def test_rejects_unknown_scenario_values(self):
        for args in ({"city": "Atlantis"}, {"warming": 4}, {"rainfall": 145},
                     {"year": 2045}, {"adaptation": "magic"}, {"investment": 101}):
            with self.subTest(args=args), self.assertRaises(ValueError):
                scenario(**args)

if __name__ == "__main__":
    unittest.main()

