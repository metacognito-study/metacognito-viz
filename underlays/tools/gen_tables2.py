import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from viz_lib import *

TABLES = [
    (
        "u_econ_national_income_table",
        "National Income Accounts",
        ["Measure", "$ (bn)"],
        [
            ["GDP", "1000"],
            ["− Depreciation", "100"],
            ["= Net Domestic Product", "900"],
            ["− Indirect business taxes", "80"],
            ["= National Income", "820"],
        ],
        [(2, 1), (4, 1)],
    ),
    (
        "u_econ_bank_t_account",
        "Bank T-Account",
        ["Assets", "Liabilities"],
        [
            ["Reserves  $200", "Deposits  $1000"],
            ["Loans  $800", ""],
        ],
        [(0, 0)],
    ),
    (
        "u_econ_money_supply_components_table",
        "Money Supply (M1 & M2)",
        ["Component", "$ (bn)"],
        [
            ["Currency", "400"],
            ["Demand deposits", "600"],
            ["= M1", "1000"],
            ["+ Savings & small time", "3000"],
            ["= M2", "4000"],
        ],
        [(2, 1), (4, 1)],
    ),
    (
        "u_econ_balance_of_payments_table",
        "Balance of Payments",
        ["Account", "Balance ($bn)"],
        [
            ["Current account", "−500"],
            ["Financial account", "+500"],
            ["= Overall balance", "0"],
        ],
        [(2, 1)],
    ),
    (
        "u_econ_exchange_rate_table",
        "Exchange Rates (per $1)",
        ["Currency", "per $1"],
        [
            ["Euro (€)", "0.90"],
            ["Pound (£)", "0.80"],
            ["Yen (¥)", "150"],
        ],
        [],
    ),
    (
        "u_econ_value_added_table",
        "Value Added by Stage",
        ["Stage", "Sale $", "Value added"],
        [
            ["Wheat", "20", "20"],
            ["Flour", "50", "30"],
            ["Bread", "90", "40"],
        ],
        [(1, 2), (2, 2)],
    ),
    (
        "u_econ_labor_stats_table",
        "Labour Market Statistics",
        ["Category", "Millions"],
        [
            ["Employed", "150"],
            ["Unemployed", "10"],
            ["= Labour force", "160"],
            ["Not in labour force", "90"],
        ],
        [(2, 1)],
    ),
    (
        "u_econ_spending_multiplier_table",
        "Spending Multiplier",
        ["MPC", "Multiplier = 1/(1−MPC)"],
        [
            ["0.50", "2"],
            ["0.75", "4"],
            ["0.80", "5"],
            ["0.90", "10"],
        ],
        [(1, 1), (2, 1), (3, 1)],
    ),
    (
        "u_econ_individual_demand_table",
        "Individual & Market Demand",
        ["Price", "Qd A", "Qd B", "Market Qd"],
        [
            ["$8", "2", "3", "5"],
            ["$6", "4", "5", "9"],
            ["$4", "6", "7", "13"],
        ],
        [(1, 3), (2, 3)],
    ),
    (
        "u_econ_real_gdp_per_capita_table",
        "Real GDP per Capita",
        ["Country", "Real GDP ($bn)", "Pop (m)", "Per capita ($)"],
        [
            ["Country X", "1000", "50", "20000"],
            ["Country Y", "800", "20", "40000"],
        ],
        [(0, 3), (1, 3)],
    ),
]

saved_count = 0
for name, title, heads, rows, blanks in TABLES:
    save(f"{name}__labeled.svg", table(title, heads, rows))
    saved_count += 1
    save(f"{name}__plain.svg", table(title, heads, rows, blanks=blanks))
    saved_count += 1

print(f"Saved {saved_count} SVG files")
