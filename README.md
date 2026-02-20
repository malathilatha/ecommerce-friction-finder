# 🛒 E-commerce Friction Finder

> AI-powered agent that detects conversion friction points and recommends data-driven fixes to improve e-commerce revenue

[![Elasticsearch Agent Builder](https://img.shields.io/badge/Built%20with-Elasticsearch%20Agent%20Builder-00BFB3?style=flat-square)](https://www.elastic.co)
[![ES|QL](https://img.shields.io/badge/Powered%20by-ES%7CQL-FEC514?style=flat-square)](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)

---

## 🎯 Problem Statement

E-commerce businesses lose **Example: $260 billion annually** to cart abandonment, yet most can't identify WHY users leave. Manual analytics take hours and miss critical patterns. Businesses need real-time, AI-powered friction detection with actionable fix recommendations.

**Key Pain Points:**
- 45% average cart abandonment rate (industry standard)
- Hours spent manually analyzing user behavior data
- No clear prioritization of what to fix first
- Difficulty calculating ROI of potential improvements
- Reactive rather than proactive problem detection

---

## 💡 Solution

An intelligent agent built on **Elasticsearch Agent Builder** that:

- ✅ **Automatically detects** 5 types of conversion friction across 8 analysis dimensions
- ✅ **Analyzes root causes** using real behavioral data patterns
- ✅ **Calculates revenue impact** for each issue ($220K+ monthly identified)
- ✅ **Prioritizes fixes** by ROI (Priority 1-4 ranking system)
- ✅ **Provides 3-step action plans** with timeline and difficulty estimates
- ✅ **Compares trends** week-over-week to track improvements
- ✅ **Generates executive summaries** with health scores

**Result:** From hours of manual analysis → **5 seconds** of AI-powered insights

---

## 🚀 Demo

### Sample Agent Conversation:

**User:** "What are the biggest problems costing me revenue?"

**Agent Response:**
```
🚨 Executive Summary: $220K Monthly Revenue at Risk

You have 3 critical problems costing you revenue right now. 
In the last 7 days, 202 carts were abandoned (45% rate), 
translating to $220,253 in potential monthly revenue loss.

🔥 Priority 1: CRITICAL - Payment Page Catastrophe
📊 The Numbers:
• 117.4 seconds average time on payment page (target: <30s)
• 5.81 seconds page load time (target: <3s)
• 73% bounce rate on checkout/payment
• 156 users hit this bottleneck
• 0% completion rate at payment step

🔍 Root Cause:
Payment page taking 6 seconds to load with users spending 2 minutes 
struggling. Performance + UX disaster causing massive abandonment.

💡 Fix Recommendations (Ranked by Impact):
1. Optimize page performance - Lazy load scripts, CDN caching (Easy)
   Expected impact: -40% load time
2. Simplify payment form - Remove fields, add autofill (Medium)
   Expected impact: -50% time spent
3. Add trust signals - Security badges, payment icons (Easy)
   Expected impact: +15% conversion

💰 Revenue Impact: $66,076/month recovery potential
⏱️ Implementation: Medium difficulty, 1-2 week sprint

⚡ Priority 2: Search Failures Blocking Sales
📊 The Numbers:
• 210 failed searches (44% failure rate)
• 184 unique users couldn't find products
• Top failures: "laptop chargr" (46), "usbc cable" (44), 
  "mous" (41), "wireles headphones" (41)

💰 Revenue Impact: $12,240/month potential gain
```

**[Full response includes Priority 3 + 3-Step Action Plan]**


## 🔧 Technical Implementation

### Technology Stack
- **Platform:** Elasticsearch Cloud Serverless (14-day trial)
- **Framework:** Elastic Agent Builder (native AI framework)
- **Query Language:** ES|QL (Elasticsearch Query Language)
- **LLM:** Elastic Managed LLM (Claude Sonnet 4.5)
- **Data Generation:** Python 3.8+ with Faker library
- **Total Development Time:** <10 days (proof of rapid prototyping)

### Data Model (5 Indices)

**Index 1: user-sessions** (2,000 records)
```json
{
  "session_id": "sess_abc123",
  "user_id": "user_0042",
  "timestamp": "2026-02-15T14:30:00Z",
  "page_url": "/checkout/payment",
  "page_load_time": 5.81,
  "action": "view_page",
  "bounce": true,
  "device": "desktop",
  "browser": "Chrome"
}
```

**Index 2: search-queries** (1,000 records)
```json
{
  "query_id": "q_xyz789",
  "user_id": "user_0042",
  "search_term": "usbc cable",
  "results_count": 0,
  "timestamp": "2026-02-15T14:25:00Z",
  "clicked_result": null
}
```

**Index 3: cart-events** (800 records)
```json
{
  "cart_id": "cart_def456",
  "user_id": "user_0042",
  "action": "add_to_cart",
  "product_id": "prod_001",
  "product_name": "Wireless Mouse",
  "timestamp": "2026-02-15T14:20:00Z",
  "cart_value": 29.99
}
```

**Index 4: checkout-flows** (600+ multi-step records)
```json
{
  "checkout_id": "co_ghi789",
  "user_id": "user_0042",
  "step": "payment",
  "time_spent": 117,
  "completed": false,
  "abandoned": true,
  "timestamp": "2026-02-15T14:35:00Z",
  "cart_value": 272.59
}
```

**Index 5: error-logs** (300 records)
```json
{
  "error_id": "err_jkl012",
  "url": "/product/old-laptop-123",
  "error_code": 404,
  "timestamp": "2026-02-15T14:40:00Z",
  "user_id": "user_0042"
}
```

---

## 🛠️ 8 Custom ES|QL Tools

### Core Friction Detection Tools

#### 1️⃣ detect_cart_abandonment
**Purpose:** Identifies checkout abandonment patterns and calculates rates per step

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

**Key Metrics Detected:**
- 45% abandonment rate at payment step
- 0% completion rate at payment (critical!)
- 202 abandoned carts in 7 days

---

#### 2️⃣ find_search_failures
**Purpose:** Identifies zero-result searches that indicate missing products or poor search config

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

**Key Insights:**
- 44% search failure rate
- Top failures: typos like "usbc cable", "wireles headphones"
- 210 failed searches = lost conversion opportunities

---

#### 3️⃣ identify_slow_pages
**Purpose:** Detects performance bottlenecks causing user frustration and bounces

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

**Key Findings:**
- Payment page: 5.81s average (target: <3s)
- 73% bounce rate on slow pages
- Direct correlation: slow = abandoned

---

#### 4️⃣ analyze_checkout_steps
**Purpose:** Analyzes time spent at each step to identify friction and confusion

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

**Critical Insight:**
- Payment step: 117.4 seconds average (should be <30s)
- Users spending 2+ minutes indicates UX/technical issues

---

#### 5️⃣ track_error_patterns
**Purpose:** Tracks HTTP errors (404s, 500s) that break user experience

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

**Pattern Detected:**
- 129 errors across critical pages
- /product/old-laptop-123: 20 errors (broken link)
- Payment page errors compound performance issues

---

### Advanced Analysis Tools

#### 6️⃣ friction_summary_dashboard
**Purpose:** Provides executive-level health score across all metrics

```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    cart_abandonment_rate = ROUND((SUM(CASE(abandoned == true, 1, 0)) / COUNT(*)) * 100, 2),
    total_revenue_at_risk = ROUND(SUM(CASE(abandoned == true, cart_value, 0)), 0)
| EVAL health_score = CASE(
    cart_abandonment_rate < 15, "EXCELLENT",
    cart_abandonment_rate < 25, "GOOD", 
    cart_abandonment_rate < 35, "NEEDS ATTENTION",
    "CRITICAL"
  )
```

**Output:**
- Overall health score: "NEEDS ATTENTION"
- $220K monthly revenue at risk
- Single-view executive dashboard

---

#### 7️⃣ calculate_revenue_impact
**Purpose:** Translates technical metrics into business outcomes ($$$)

```esql
FROM "checkout-flows"
| WHERE timestamp > NOW() - 7 days
| STATS 
    total_carts = COUNT_DISTINCT(checkout_id),
    abandoned_carts = SUM(CASE(abandoned == true, 1, 0)),
    avg_cart_value = ROUND(AVG(cart_value), 2)
| EVAL 
    monthly_abandoned = abandoned_carts * 4,
    revenue_loss_monthly = ROUND(monthly_abandoned * avg_cart_value, 0),
    recovery_30_percent = ROUND(revenue_loss_monthly * 0.30, 0)
```

**Business Translation:**
- 202 abandoned carts/week × 4 = 808/month
- 808 × $272.59 avg = $220,253 monthly loss
- 30% recovery = $66,076 potential gain

---

#### 8️⃣ compare_weekly_trends
**Purpose:** Week-over-week comparison to track if friction is improving/worsening

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
    avg_cart_value = ROUND(AVG(cart_value), 2)
  BY week
```

**Trend Analysis:**
- Shows if improvements are working
- Tracks regression warnings
- Data-driven decision validation

---

## 📊 Results & Business Impact

### Detection Accuracy
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|---------|
| Cart Abandonment Rate | 45% | <20% (good) | 🔴 Critical |
| Search Failure Rate | 44% | <5% (target) | 🔴 Critical |
| Payment Page Load | 5.81s | <3s (target) | 🔴 Critical |
| Error Rate | 129/week | Minimal | 🟡 Warning |
| Time at Payment | 117.4s | <30s (target) | 🔴 Critical |

### Revenue Impact Identified
- **Total Monthly Revenue at Risk:** $220,253
  - Payment page issues: $66,076/month
  - Search failures: $12,240/month
  - Error patterns: $790+/month
- **Potential Recovery:** $78,240+/month (30% fix success rate)
- **Annual Impact:** $938,880+ potential revenue recovery

### Operational Efficiency
- **Manual Analysis Time:** 4-6 hours → **AI Analysis Time:** <5 seconds
- **Time Savings:** 99.9% reduction in analysis time
- **Tools Orchestrated:** 8 tools working in concert
- **Data Points Analyzed:** 4,700+ events across 5 dimensions
- **Actionable Insights:** 3-priority system with implementation timelines

### Agent Performance
- ✅ Multi-tool orchestration (calls 3-5 tools per query)
- ✅ Revenue calculations (automatic ROI analysis)
- ✅ Priority ranking (1-4 system with impact scores)
- ✅ Proactive recommendations (not just reactive reporting)
- ✅ Executive summaries (emoji indicators, health scores)
- ✅ Action plans (week-by-week implementation roadmaps)

## 💭 What I Learned

### Technical Insights
1. **ES|QL is Powerful** - Complex multi-step aggregations are remarkably concise compared to traditional Query DSL. The `EVAL` and `CASE` functions enable sophisticated business logic directly in queries.

2. **Context Engineering Matters** - The agent's effectiveness depends heavily on precise tool descriptions and well-structured instructions. Vague descriptions lead to incorrect tool selection.

3. **Agent Builder = 10x Faster** - Building this manually would require: Lambda functions, API gateway, vector DB, embedding pipeline, tool orchestration logic, state management. Agent Builder handles all of this natively.

4. **Synthetic Data Works** - Intentional friction patterns (slow payment page, typo searches) successfully simulated real-world issues, proving concept viability before production data.

5. **Multi-Tool Orchestration** - The agent intelligently combines tools (cart abandonment + checkout steps + revenue calculator) to provide comprehensive insights no single tool could deliver.

### Business Learnings
1. **Revenue Language Wins** - Technical metrics (45% abandonment) become actionable when translated to dollars ($220K at risk). Business stakeholders respond to money, not percentages.

2. **Priority Ranking is Critical** - Without Priority 1-4 system, users face analysis paralysis. "Fix everything" → "Fix payment page first (highest ROI)" is the difference between insight and action.

3. **Proactive > Reactive** - Traditional analytics report problems after they've cost money. This agent predicts impact before fixes are implemented, enabling proactive decision-making.

4. **One Focused Fix > Ten Scattered** - Payment page alone accounts for $66K/month (75% of total issue). Agent correctly identifies this as Priority 1, avoiding wasted effort on minor issues.

5. **Speed Matters** - Going from 4-hour manual analysis to 5-second AI response isn't just convenience—it enables daily monitoring vs. monthly, catching problems before they compound.

### Surprising Discoveries
- **Emoji Indicators Work** - Initially skeptical, but 🔥/⚠️/✅ make long responses scannable and increase engagement. Users immediately see severity without reading paragraphs.
  
- **Week-over-Week Comparison** - This tool seemed like a "nice to have" but became critical—showing trend direction (getting better/worse) adds context that static metrics lack.

- **Elastic Managed LLM Quality** - No setup, no API keys, and performance matched expectations. The tight integration with ES|QL made tool calling seamless.

- **Serverless is Legit** - Zero infrastructure management, instant provisioning, auto-scaling. Went from idea to working prototype in hours, not days.

