import unittest

from data import FEATURES, PLANS
from gym_membership import (
    MembershipSelection,
    calculate_cost,
    finalize_membership,
    get_special_offer_discount,
    validate_selection,
)


class GymMembershipTests(unittest.TestCase):
    def test_valid_selection_passes_validation(self):
        selection = MembershipSelection(
            plan_key="basic",
            feature_keys=("group_classes",),
            member_count=1,
        )

        result = validate_selection(selection, PLANS, FEATURES)

        self.assertTrue(result.is_valid)

    def test_invalid_plan_fails_validation(self):
        selection = MembershipSelection(plan_key="vip", feature_keys=(), member_count=1)

        result = validate_selection(selection, PLANS, FEATURES)

        self.assertFalse(result.is_valid)
        self.assertIn("not available", result.message)

    def test_invalid_feature_fails_validation(self):
        selection = MembershipSelection(
            plan_key="basic",
            feature_keys=("exclusive_facilities",),
            member_count=1,
        )

        result = validate_selection(selection, PLANS, FEATURES)

        self.assertFalse(result.is_valid)
        self.assertIn("not available", result.message)

    def test_single_member_base_and_feature_cost(self):
        selection = MembershipSelection(
            plan_key="basic",
            feature_keys=("group_classes", "personal_training"),
            member_count=1,
        )

        breakdown = calculate_cost(selection, PLANS, FEATURES)

        self.assertEqual(50, breakdown.base_cost)
        self.assertEqual(105, breakdown.features_cost)
        self.assertEqual(155, breakdown.final_total)

    def test_group_discount_applies_for_two_or_more_members(self):
        selection = MembershipSelection(
            plan_key="basic",
            feature_keys=("personal_training",),
            member_count=2,
        )

        breakdown = calculate_cost(selection, PLANS, FEATURES)

        self.assertEqual(260, breakdown.subtotal)
        self.assertEqual(26, breakdown.group_discount)
        self.assertEqual(214, breakdown.final_total)

    def test_group_discount_does_not_apply_for_one_member(self):
        selection = MembershipSelection(
            plan_key="basic",
            feature_keys=("personal_training",),
            member_count=1,
        )

        breakdown = calculate_cost(selection, PLANS, FEATURES)

        self.assertEqual(0, breakdown.group_discount)

    def test_special_offer_discount_thresholds(self):
        self.assertEqual(0, get_special_offer_discount(200))
        self.assertEqual(20, get_special_offer_discount(201))
        self.assertEqual(20, get_special_offer_discount(400))
        self.assertEqual(50, get_special_offer_discount(401))

    def test_premium_plan_applies_surcharge_and_rounds(self):
        selection = MembershipSelection(
            plan_key="premium",
            feature_keys=("specialized_training",),
            member_count=1,
        )

        breakdown = calculate_cost(selection, PLANS, FEATURES)

        self.assertEqual(260, breakdown.subtotal)
        self.assertEqual(39, breakdown.premium_surcharge)
        self.assertEqual(20, breakdown.special_offer_discount)
        self.assertEqual(279, breakdown.final_total)

    def test_special_offer_can_apply_after_group_discount_and_surcharge(self):
        selection = MembershipSelection(
            plan_key="premium",
            feature_keys=("exclusive_facilities", "specialized_training"),
            member_count=2,
        )

        breakdown = calculate_cost(selection, PLANS, FEATURES)

        self.assertEqual(720, breakdown.subtotal)
        self.assertEqual(108, breakdown.premium_surcharge)
        self.assertAlmostEqual(82.8, breakdown.group_discount)
        self.assertEqual(50, breakdown.special_offer_discount)
        self.assertEqual(695, breakdown.final_total)

    def test_finalize_returns_negative_one_when_canceled(self):
        selection = MembershipSelection(plan_key="basic", feature_keys=(), member_count=1)

        result = finalize_membership(selection, PLANS, FEATURES, confirmed=False)

        self.assertEqual(-1, result)

    def test_finalize_returns_negative_one_for_invalid_data(self):
        selection = MembershipSelection(plan_key="missing", feature_keys=(), member_count=1)

        result = finalize_membership(selection, PLANS, FEATURES, confirmed=True)

        self.assertEqual(-1, result)


if __name__ == "__main__":
    unittest.main()