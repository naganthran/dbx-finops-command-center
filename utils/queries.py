from .spark_utils import run_query
from .config import TABLES

def executive_scorecard():
    return run_query(f"SELECT * FROM {TABLES['executive']}")

def action_dashboard():
    return run_query(f"SELECT * FROM {TABLES['action_dashboard']}")

def top_actions(limit=200):
    return run_query(f"""
        SELECT *
        FROM {TABLES['top_actions']}
        LIMIT {int(limit)}
    """)

def policy_breakdown():
    return run_query(f"""
        SELECT *
        FROM {TABLES['policy_breakdown']}
        ORDER BY estimated_annual_savings_usd DESC
    """)

def owner_breakdown():
    return run_query(f"""
        SELECT *
        FROM {TABLES['owner_breakdown']}
        ORDER BY estimated_annual_savings_usd DESC
    """)

def governance_queue(limit=500):
    return run_query(f"""
        SELECT *
        FROM {TABLES['governance_queue']}
        ORDER BY bookable_savings_opportunity_90d_usd DESC
        LIMIT {int(limit)}
    """)

def daily_spend_trend():
    return run_query(f"""
        SELECT
            usage_date,
            finops_workload_category,
            ROUND(SUM(cost_usd), 2) AS cost_usd,
            ROUND(SUM(dbus), 2) AS dbus
        FROM {TABLES['billing_fact']}
        WHERE usage_date >= DATEADD(day, -90, CURRENT_DATE())
        GROUP BY usage_date, finops_workload_category
        ORDER BY usage_date
    """)

def workload_spend_31d():
    return run_query(f"""
        SELECT
            finops_workload_category,
            ROUND(SUM(cost_usd), 2) AS cost_usd_31d,
            ROUND(SUM(dbus), 2) AS dbus_31d,
            ROUND((SUM(cost_usd) / 31) * 90, 2) AS forecast_90d_usd,
            ROUND((SUM(cost_usd) / 31) * 365, 2) AS forecast_365d_usd
        FROM {TABLES['billing_fact']}
        WHERE usage_date >= DATEADD(day, -31, CURRENT_DATE())
        GROUP BY finops_workload_category
        ORDER BY cost_usd_31d DESC
    """)

def user_spend():
    return run_query(f"""
        SELECT *
        FROM {TABLES['user_spend']}
        ORDER BY total_cost_usd_31d DESC
        LIMIT 100
    """)

def cluster_opportunities():
    return run_query(f"""
        SELECT *
        FROM {TABLES['cluster_opportunity']}
        ORDER BY bookable_savings_opportunity_90d_usd DESC, cost_usd_31d DESC
        LIMIT 300
    """)

def sql_candidates():
    return run_query(f"""
        SELECT *
        FROM {TABLES['sql_candidates']}
        ORDER BY sql_cost_usd_31d DESC
        LIMIT 200
    """)

def serverless_governance():
    return run_query(f"""
        SELECT *
        FROM {TABLES['serverless']}
        ORDER BY cost_usd_31d DESC
        LIMIT 200
    """)

def jobs_cost():
    return run_query(f"""
        SELECT *
        FROM {TABLES['jobs']}
        ORDER BY cost_usd_31d DESC
        LIMIT 200
    """)
