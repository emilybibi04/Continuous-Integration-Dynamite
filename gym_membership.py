from dataclasses import dataclass


GROUP_DISCOUNT_RATE = 0.10
PREMIUM_SURCHARGE_RATE = 0.15


@dataclass(frozen=True)
class MembershipPlan:
    key: str
    name: str
    base_cost: int
    benefits: list[str]
    available_feature_keys: tuple[str, ...]
    includes_premium_features: bool = False


@dataclass(frozen=True)
class Feature:
    key: str
    name: str
    cost: int
    description: str
    is_premium: bool = False


@dataclass(frozen=True)
class MembershipSelection:
    plan_key: str
    feature_keys: tuple[str, ...]
    member_count: int = 1


@dataclass(frozen=True)
class CostBreakdown:
    base_cost: int
    features_cost: int
    subtotal: int
    premium_surcharge: float
    group_discount: float
    special_offer_discount: int
    total_before_rounding: float
    final_total: int


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    message: str = ""


def validate_selection(selection: MembershipSelection, plans: dict, features: dict) -> ValidationResult:
    if selection.plan_key not in plans:
        return ValidationResult(False, f"Membership plan '{selection.plan_key}' is not available.")

    if selection.member_count < 1:
        return ValidationResult(False, "Member count must be at least 1.")

    plan = plans[selection.plan_key]
    unavailable_features = []

    for feature_key in selection.feature_keys:
        if feature_key not in features:
            unavailable_features.append(feature_key)
        elif feature_key not in plan.available_feature_keys:
            unavailable_features.append(features[feature_key].name)

    if unavailable_features:
        joined_features = ", ".join(unavailable_features)
        return ValidationResult(False, f"Selected feature is not available for this plan: {joined_features}.")

    return ValidationResult(True)


def has_premium_features(selection: MembershipSelection, plans: dict, features: dict) -> bool:
    plan = plans[selection.plan_key]
    return plan.includes_premium_features or any(features[key].is_premium for key in selection.feature_keys)


def calculate_cost(selection: MembershipSelection, plans: dict, features: dict) -> CostBreakdown:
    validation = validate_selection(selection, plans, features)
    if not validation.is_valid:
        raise ValueError(validation.message)

    plan = plans[selection.plan_key]
    base_cost = plan.base_cost * selection.member_count
    features_cost = sum(features[key].cost for key in selection.feature_keys) * selection.member_count
    subtotal = base_cost + features_cost

    premium_surcharge = 0.0
    if has_premium_features(selection, plans, features):
        premium_surcharge = subtotal * PREMIUM_SURCHARGE_RATE

    total_after_surcharge = subtotal + premium_surcharge

    group_discount = 0.0
    if selection.member_count >= 2:
        group_discount = total_after_surcharge * GROUP_DISCOUNT_RATE

    total_after_group_discount = total_after_surcharge - group_discount
    special_offer_discount = get_special_offer_discount(total_after_group_discount)
    total_before_rounding = total_after_group_discount - special_offer_discount

    return CostBreakdown(
        base_cost=base_cost,
        features_cost=features_cost,
        subtotal=subtotal,
        premium_surcharge=premium_surcharge,
        group_discount=group_discount,
        special_offer_discount=special_offer_discount,
        total_before_rounding=total_before_rounding,
        final_total=round(total_before_rounding),
    )


def get_special_offer_discount(total: float) -> int:
    if total > 400:
        return 50
    if total > 200:
        return 20
    return 0


def finalize_membership(selection: MembershipSelection, plans: dict, features: dict, confirmed: bool) -> int:
    if not confirmed:
        return -1

    validation = validate_selection(selection, plans, features)
    if not validation.is_valid:
        return -1

    try:
        return calculate_cost(selection, plans, features).final_total
    except ValueError:
        return -1
