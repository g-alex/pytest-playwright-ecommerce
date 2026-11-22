# pytest-playwright-ecommerce

Black-box **API** and **UI** autotests for a Telegram Mini App e-commerce product.

Application source code is **private (NDA)**. This repository contains **tests only** — no shop brand, no production URLs.

## Stack

- Python 3.10+
- pytest
- httpx (API)
- Playwright + Page Object Model (UI)
- jsonschema (API contract checks)
- Allure / pytest-html (reports)
- GitHub Actions (collect + optional smoke)

## Test approach

### Pyramid

1. **API** (majority) — fast, stable contracts and business rules.
2. **UI smoke** — critical user journeys in the Mini App.
3. **Negatives** — validation and error handling (404, empty cart, invalid status).

We do **not** duplicate every API check in UI. UI covers what the user sees; API covers rules and edge cases.

### Risk-based coverage

| Risk | Covered by |
|------|------------|
| App / API is down | `GET /api/status`, catalog UI |
| Catalog / search broken | API + UI search/category |
| Cart corruption | add / qty / remove / clear |
| Checkout fails | API order + UI checkout |
| Bad order status | API status + invalid status |
| Empty cart UX | UI empty-cart popup |

### Explicitly out of scope (v1)

- Telegram admin/shop bots (tokens, unstable for public portfolio)
- Production runs with mutating tests
- Load / performance
- Full i18n matrix — only default locale in UI smoke

### Anti-flaky strategy

- Fresh **browser context** per UI test (no shared cookies/`localStorage` leaks).
- Shared **`TEST_USER_ID`**: UI seeds `localStorage.browserTempUserId`; API `clear_cart` uses the same id.
- Prefer Playwright **`expect` / `expect_response`** over fixed `sleep`.
- Dynamic test data from the stand (no hard-coded product ids/titles).
- Use **`available_stock`** (stock minus reserved), not raw `stock` alone.
- Mutating tests only on **local/staging**, never production.

### UI ↔ API user sync

1. `page` fixture seeds `localStorage.browserTempUserId = TEST_USER_ID`.
2. `TEST_USER_ID` must look like `web_tg_<username>` (see `.env.example`).
3. UI checkout form regenerates the same id from the Telegram field → cart/order stay aligned.

## What is covered

| Layer | Scenarios |
|-------|-----------|
| API smoke | status, categories, products, cart add→get→clear, order from cart |
| API extra | search, category filter, cart qty/remove, order status confirmed |
| API negative | 404s, cart without productId, empty-cart order, invalid status |
| UI smoke | catalog, add to cart → badge, checkout → order created |
| UI extra | search, category filter |
| UI negative | empty cart popup |

## Project layout

```text
tests/api/       # API tests
tests/ui/        # Playwright tests
pages/           # Page Object Model
fixtures/        # helpers (HTTP wrappers)
utils/           # config + JSON schemas
conftest.py      # shared pytest fixtures
```

## Setup

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
copy .env.example .env
```

Set in `.env` (local or staging stand — never production):

```env
BASE_URL=http://localhost:3000
TEST_USER_ID=web_tg_aqa_local_user
```

Point `BASE_URL` at your **local/staging** Mini App stand (separate DB, bots off).

## Run tests

```bash
# all
python -m pytest -v

# smoke only
python -m pytest -m smoke -v

# API only / UI only
python -m pytest -m api -v
python -m pytest -m ui -v

# HTML report
python -m pytest -m smoke --html=reports/report.html --self-contained-html

# Allure results (needs Allure Commandline for `allure serve`)
python -m pytest -m smoke --alluredir=allure-results
allure serve allure-results
```

## CI (GitHub Actions)

On every push/PR the workflow runs `pytest --collect-only` (framework sanity).

Optional job **API smoke** runs only when repository variable `BASE_URL` is set (local/staging stand or future private-app clone). HTML/Allure outputs are uploaded as artifacts — not committed to git.

## Reports

Smoke tests use Allure metadata (`feature` / `story` / `title` / `step`).

| Report | Command | Commit to git? |
|--------|---------|----------------|
| pytest-html | `--html=reports/report.html --self-contained-html` | No (gitignore) |
| Allure | `--alluredir=allure-results` + `allure serve` | No (gitignore) |

Keep reports local or as **CI artifacts**. Do not push raw results.

## Safety

- Do **not** commit `.env`, tokens, production URLs, or shop brand assets.
- Mutating flows (create order) — **local/staging only**.
- Tests use a dedicated `TEST_USER_ID`.

## Resume one-liner

> API + UI autotests for a Telegram Mini App e-commerce product (NDA): pytest, Playwright, Page Object, jsonschema, Allure/HTML. Public tests-only repo; risk-based smoke + negatives; isolated stand; anti-flaky waits and shared test user id.
