from data import FEATURES, PLANS
from gym_membership import MembershipSelection, calculate_cost, finalize_membership, validate_selection


def main():
    while True:
        print("\nGym Membership Management System")
        print("1. Create membership")
        print("2. View plans")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            result = create_membership()
            print(f"Result: {result}")
        elif choice == "2":
            display_plans()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid menu option. Please choose 1, 2, or 3.")


def create_membership() -> int:
    while True:
        display_plans()
        plan_key = input("Enter membership plan key: ").strip().lower()

        if plan_key not in PLANS:
            print(f"Membership plan '{plan_key}' is not available. Please select again.")
            continue

        feature_keys = prompt_for_features(plan_key)
        member_count = prompt_for_member_count()
        selection = MembershipSelection(plan_key=plan_key, feature_keys=feature_keys, member_count=member_count)
        validation = validate_selection(selection, PLANS, FEATURES)

        if not validation.is_valid:
            print(validation.message)
            print("Please make your selections again.")
            continue

        breakdown = calculate_cost(selection, PLANS, FEATURES)
        display_confirmation(selection, breakdown)
        confirmation = input("Confirm this membership plan? (y/n): ").strip().lower()

        if confirmation == "y":
            return finalize_membership(selection, PLANS, FEATURES, confirmed=True)

        print("Membership plan canceled. You can make changes from the menu.")
        return finalize_membership(selection, PLANS, FEATURES, confirmed=False)


def display_plans():
    print("\nAvailable Membership Plans")
    for plan in PLANS.values():
        print(f"\n{plan.key} - {plan.name}: ${plan.base_cost}")
        for benefit in plan.benefits:
            print(f"  - {benefit}")
        print("  Available features:")
        for feature_key in plan.available_feature_keys:
            feature = FEATURES[feature_key]
            premium_label = " (premium)" if feature.is_premium else ""
            print(f"    {feature.key}: {feature.name}{premium_label} - ${feature.cost}")


def prompt_for_features(plan_key: str) -> tuple[str, ...]:
    plan = PLANS[plan_key]
    selected_features = []

    print("\nSelect additional features.")
    print("Enter feature keys one at a time, or press Enter when finished.")

    while True:
        feature_key = input("Feature key: ").strip().lower()
        if feature_key == "":
            return tuple(selected_features)

        if feature_key not in FEATURES:
            print(f"Feature '{feature_key}' is not available. Please select again.")
            continue

        if feature_key not in plan.available_feature_keys:
            print(f"Feature '{FEATURES[feature_key].name}' is not available for {plan.name}.")
            continue

        if feature_key in selected_features:
            print("That feature has already been selected.")
            continue

        selected_features.append(feature_key)
        print(f"Added {FEATURES[feature_key].name}.")


def prompt_for_member_count() -> int:
    while True:
        raw_count = input("How many members are signing up together? ").strip()
        try:
            member_count = int(raw_count)
        except ValueError:
            print("Invalid member count. Please enter a whole number.")
            continue

        if member_count < 1:
            print("Invalid member count. Please enter at least 1.")
            continue

        if member_count >= 2:
            print("Group savings available: 10% discount applied for two or more members.")

        return member_count


def display_confirmation(selection: MembershipSelection, breakdown):
    plan = PLANS[selection.plan_key]
    selected_features = [FEATURES[key] for key in selection.feature_keys]

    print("\nReview Membership")
    print(f"Plan: {plan.name}")
    print(f"Members: {selection.member_count}")

    if selected_features:
        print("Additional features:")
        for feature in selected_features:
            print(f"  - {feature.name}: ${feature.cost} per member")
    else:
        print("Additional features: None")

    print(f"Base membership cost: ${breakdown.base_cost}")
    print(f"Additional features cost: ${breakdown.features_cost}")
    print(f"Subtotal: ${breakdown.subtotal}")

    if breakdown.premium_surcharge > 0:
        print(f"Premium surcharge: ${breakdown.premium_surcharge:.2f}")

    if breakdown.group_discount > 0:
        print(f"Group discount savings: -${breakdown.group_discount:.2f}")

    if breakdown.special_offer_discount > 0:
        print(f"Special offer discount: -${breakdown.special_offer_discount}")

    print(f"Total before rounding: ${breakdown.total_before_rounding:.2f}")
    print(f"Final total: ${breakdown.final_total}")


if __name__ == "__main__":
    main()
