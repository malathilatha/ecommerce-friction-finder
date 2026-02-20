# Complete Tool Creation Guide

This document contains all 8 custom ES|QL tools for the E-commerce Friction Finder agent.

---

## How to Create Tools

1. Navigate to **Agent Builder** → **Tools** in Kibana
2. Click **"Create tool"**
3. Select **"ES|QL"** as tool type
4. Copy the configuration below for each tool
5. Click **"Save"**

---

## Tool #1: detect_cart_abandonment

**Tool ID:**
```
detect_cart_abandonment
```

**Description:**
```
Detects cart abandonment patterns by analyzing checkout flows. Identifies which checkout steps have highest drop-off rates and calculates abandonment percentages. Use this when user asks about cart abandonment, checkout issues, or conversion problems.
```

**ES|QL Query:**
```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    total_checkouts = COUNT(*),
    abandoned_count = SUM(CASE(abandoned == true, 1, 0)),
    completed_count = SUM(CASE(completed == true, 1, 0))
  BY step
| EVAL abandonment_rate = ROUND((abandoned_count / total_checkouts) * 100, 2)
| EVAL completion_rate = ROUND((completed_count / total_checkouts) * 100, 2)
| SORT abandonment_rate DESC
```

---

## Tool #2: find_search_failures

**Tool ID:**
```
find_search_failures
```

**Description:**
```
Identifies search queries that returned zero results. Shows which search terms users are looking for but cannot find. Use this when user asks about search problems, missing products, or search optimization.
```

**ES|QL Query:**
```esql
FROM "search-queries"
| WHERE results_count == 0 AND timestamp > NOW() - 7 days
| STATS 
    failure_count = COUNT(*),
    unique_users = COUNT_DISTINCT(user_id)
  BY search_term
| WHERE failure_count > 2
| EVAL impact_score = failure_count * unique_users
| SORT failure_count DESC
| LIMIT 20
```

---

## Tool #3: identify_slow_pages

**Tool ID:**
```
identify_slow_pages
```

**Description:**
```
Detects pages with slow load times that cause user frustration and bounces. Calculates average load time and bounce rate per page. Use this when user asks about performance, page speed, or bounce rates.
```

**ES|QL Query:**
```esql
FROM "user-sessions"
| WHERE timestamp > NOW() - 7 days
| STATS 
    avg_load_time = ROUND(AVG(page_load_time), 2),
    max_load_time = ROUND(MAX(page_load_time), 2),
    page_views = COUNT(*),
    bounces = SUM(CASE(bounce == true, 1, 0))
  BY page_url
| WHERE page_views > 10
| EVAL bounce_rate = ROUND((bounces / page_views) * 100, 2)
| SORT avg_load_time DESC
| LIMIT 15
```

---

## Tool #4: analyze_checkout_steps

**Tool ID:**
```
analyze_checkout_steps
```

**Description:**
```
Analyzes time spent at each checkout step and identifies bottlenecks. Shows which steps take too long and may be causing user frustration. Use this when user asks about checkout process, slow steps, or user experience issues.
```

**ES|QL Query:**
```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    avg_time = ROUND(AVG(time_spent), 1),
    max_time = MAX(time_spent),
    total_sessions = COUNT(*),
    completion_rate = ROUND((SUM(CASE(completed == true, 1, 0)) / COUNT(*)) * 100, 2)
  BY step
| EVAL status = CASE(
    avg_time > 60, "CRITICAL - Too slow",
    avg_time > 30, "WARNING - Slow",
    "OK"
  )
| SORT avg_time DESC
```

---

## Tool #5: track_error_patterns

**Tool ID:**
```
track_error_patterns
```

**Description:**
```
Tracks 404 errors and other HTTP errors on the site. Identifies broken links and pages causing frustration. Use this when user asks about errors, broken pages, or 404 issues.
```

**ES|QL Query:**
```esql
FROM "error-logs"
| WHERE timestamp > NOW() - 7 days
| STATS 
    error_count = COUNT(*),
    unique_users_affected = COUNT_DISTINCT(user_id)
  BY url
| WHERE error_count > 3
| EVAL severity = CASE(
    error_count > 20, "HIGH",
    error_count > 10, "MEDIUM",
    "LOW"
  )
| SORT error_count DESC
| LIMIT 15
```

---

## Tool #6: friction_summary_dashboard

**Tool ID:**
```
friction_summary_dashboard
```

**Description:**
```
Provides comprehensive overview of all friction metrics in one view. Shows cart abandonment rate, total revenue at risk, and overall health score. Use this when user asks for overview, summary, dashboard, or health check.
```

**ES|QL Query:**
```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    cart_abandonment_rate = ROUND((SUM(CASE(abandoned == true, 1, 0)) / COUNT(*)) * 100, 2),
    total_checkouts = COUNT(*),
    total_revenue_at_risk = ROUND(SUM(CASE(abandoned == true, cart_value, 0)), 0)
| EVAL health_score = CASE(
    cart_abandonment_rate < 15, "EXCELLENT",
    cart_abandonment_rate < 25, "GOOD", 
    cart_abandonment_rate < 35, "NEEDS ATTENTION",
    "CRITICAL"
  )
```

---

## Tool #7: calculate_revenue_impact

**Tool ID:**
```
calculate_revenue_impact
```

**Description:**
```
Calculates estimated revenue loss from friction points and potential revenue gain from fixes. Translates technical metrics into business outcomes. Use when user asks about business impact, ROI, revenue, or financial implications.
```

**ES|QL Query:**
```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    total_carts = COUNT_DISTINCT(checkout_id),
    abandoned_carts = SUM(CASE(abandoned == true, 1, 0)),
    avg_cart_value = ROUND(AVG(cart_value), 2)
| EVAL 
    monthly_abandoned_carts = abandoned_carts * 4,
    estimated_monthly_revenue_loss = ROUND(monthly_abandoned_carts * avg_cart_value, 0),
    potential_recovery_30_percent = ROUND(estimated_monthly_revenue_loss * 0.30, 0)
```

---

## Tool #8: compare_weekly_trends

**Tool ID:**
```
compare_weekly_trends
```

**Description:**
```
Compares current week metrics vs previous week to identify trends. Shows if friction is increasing or decreasing over time. Use when user asks about trends, changes, improvements, or whether things are getting better or worse.
```

**ES|QL Query:**
```esql
FROM "checkout-flows"
| EVAL week = CASE(
    timestamp > NOW() - 7 days, "current_week",
    timestamp > NOW() - 14 days, "previous_week",
    "older"
  )
| WHERE week IN ("current_week", "previous_week")
| STATS 
    abandonment_rate = ROUND((SUM(CASE(abandoned == true, 1, 0)) / COUNT(*)) * 100, 2),
    total_sessions = COUNT(*),
    avg_cart_value = ROUND(AVG(cart_value), 2)
  BY week
| SORT week DESC
```

---

## Verification

After creating all 8 tools, verify in Agent Builder → Tools that you see:

- ✅ detect_cart_abandonment
- ✅ find_search_failures
- ✅ identify_slow_pages
- ✅ analyze_checkout_steps
- ✅ track_error_patterns
- ✅ friction_summary_dashboard
- ✅ calculate_revenue_impact
- ✅ compare_weekly_trends

**Total: 8 tools**

---

## Testing Individual Tools (Optional)

You can test each tool in Kibana Dev Tools:

1. Go to **Management** → **Dev Tools**
2. Paste any ES|QL query above
3. Click the ▶️ play button
4. Verify results match expected output



After creating all tools, proceed to create the agent using `AGENT_CONFIG.md`.
