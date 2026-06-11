# Gym Membership Management System

Command-line Python application for creating and pricing gym memberships.

## Run the Program

```bash
uv run python main.py
```

The program shows a menu repeatedly until the user exits. Membership data is kept in memory and hardcoded in `data.py`.

## Run Tests

```bash
uv run python -m unittest
```

## Assumptions

- No database is used; all plans and features are hardcoded in memory.
- Group membership totals are calculated for the whole group, not per person.
- A 10% group discount applies when two or more members sign up for the same plan together.
- Premium plans and premium features apply a 15% surcharge.
- Special offer discounts are applied after the premium surcharge and group discount.
- If the discounted total is greater than `$400`, the special offer discount is `$50`.
- If the discounted total is greater than `$200` and not greater than `$400`, the special offer discount is `$20`.
- Final confirmed totals are rounded to the nearest dollar and returned as a positive integer.
- Invalid final data or canceled plans return `-1`.
