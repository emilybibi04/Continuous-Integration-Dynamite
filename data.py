from gym_membership import Feature, MembershipPlan


PLANS = {
    "basic": MembershipPlan(
        key="basic",
        name="Basic",
        base_cost=50,
        benefits=[
            "Gym floor access",
            "Locker room access",
            "Standard equipment access",
        ],
        available_feature_keys=("group_classes", "personal_training"),
    ),
    "premium": MembershipPlan(
        key="premium",
        name="Premium",
        base_cost=120,
        benefits=[
            "All Basic benefits",
            "Pool and sauna access",
            "Priority class booking",
        ],
        available_feature_keys=(
            "group_classes",
            "personal_training",
            "nutrition_coaching",
            "exclusive_facilities",
            "specialized_training",
        ),
        includes_premium_features=True,
    ),
    "family": MembershipPlan(
        key="family",
        name="Family",
        base_cost=180,
        benefits=[
            "Gym access for family members",
            "Family locker access",
            "Weekend family classes",
        ],
        available_feature_keys=("group_classes", "personal_training", "nutrition_coaching"),
    ),
}


FEATURES = {
    "group_classes": Feature(
        key="group_classes",
        name="Group classes",
        cost=25,
        description="Yoga, spinning, and strength classes",
    ),
    "personal_training": Feature(
        key="personal_training",
        name="Personal training sessions",
        cost=80,
        description="Two one-on-one sessions with a trainer",
    ),
    "nutrition_coaching": Feature(
        key="nutrition_coaching",
        name="Nutrition coaching",
        cost=60,
        description="Personalized nutrition consultation",
    ),
    "exclusive_facilities": Feature(
        key="exclusive_facilities",
        name="Exclusive gym facilities",
        cost=100,
        description="Access to premium training rooms and recovery areas",
        is_premium=True,
    ),
    "specialized_training": Feature(
        key="specialized_training",
        name="Specialized training programs",
        cost=140,
        description="Advanced athletic or sport-specific programming",
        is_premium=True,
    ),
}
