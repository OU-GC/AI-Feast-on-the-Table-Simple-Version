# AI Feast on the Table

Enter your gender, age, height, weight, and weekly exercise days, and the app
recommends real restaurant dishes that fit your daily energy needs — ranked by
your BMI band so the picks actually match your goals, not just generic "healthy"
suggestions. It then calls an LLM to turn the raw numbers into a personalized
nutrition analysis written in the voice of a nutritionist.

## Features

- **Body-metric calculation**: derives BMI, Basal Metabolic Rate (BMR), and Total
  Daily Energy Expenditure (TDEE) from the user's profile.
- **Gender-specific BMR formulas**: separate equations for 男性 (male) and 女性 (female).
- **Activity-level scaling**: weekly exercise days (0–7) map to a TDEE multiplier
  from 1.2 (sedentary) to 1.9 (daily training).
- **BMI-banded menu filtering**: underweight (<18.5) keeps higher-calorie dishes,
  normal (18.5–24) keeps all, overweight (≥24) keeps lower-calorie dishes.
- **Macronutrient targets**: splits TDEE into carbs / protein / fat (55% / 15% / 25%)
  and converts to grams.
- **Random 3-dish pick**: samples up to 3 dishes from the eligible set each request.
- **LLM nutrition analysis**: GPT-3.5-turbo writes a tailored, nutritionist-style
  explanation tying each dish back to the user's BMI and TDEE.
- **Input guarding**: validates required fields, numeric formats, and sane ranges
  (height ≤ 250, weight ≤ 300, age ≤ 120) before any computation.

## Tech Stack

- **Backend**: Python + Flask
- **Data**: restaurant menu CSV loaded with `pandas`
- **External services**: OpenAI (`gpt-3.5-turbo` — nutrition analysis)
- **Frontend**: vanilla HTML / CSS / JS served from `public/`
- **Deployment**: Vercel (`api/index.py` serverless entry, configured in `vercel.json`)

## Project Structure

```
api/index.py                       Flask app, calorie/macro/BMI logic, recommendation route
public/
  index.html                       Welcome page
  homepage.html                    Main app page
  images/                          Background and login imagery
data/restaurant_information.csv    Restaurant menus with nutrition facts
vercel.json                        Vercel routing config (rewrites all paths to api/index)
requirements.txt                   Python dependencies
.gitignore                         Excludes .env, showcase/, caches
LICENSE                            Apache License 2.0
```

## Environment Variables

Create a `.env` file in the project root (loaded automatically at startup):

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Generating the personalized nutrition analysis |
| `CSV_PATH` | No | Override the menu CSV location (defaults to `data/restaurant_information.csv`) |

The app refuses to start without `OPENAI_API_KEY`.

## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env (see Environment Variables above)

# 3. Run (Flask serves both the public/ static pages and the API)
python api/index.py
```

## Deployment

Deployed on Vercel — try it at [ai-feast-on-the-table-simple-versio-chi.vercel.app](https://ai-feast-on-the-table-simple-versio-chi.vercel.app/).

## API

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Frontend welcome page |
| POST | `/api/recommend_food` | Main flow: profile → BMI/TDEE → ranked dishes + analysis |

`POST /api/recommend_food` request example:

```json
{
  "gender": "男性",
  "height": 175,
  "weight": 70,
  "age": 22,
  "exercise": 3
}
```

`gender` accepts `男性` (male) or `女性` (female); `exercise` is exercise days per
week (0–7). The response includes the BMI, daily caloric need (TDEE), recommended
macronutrient grams, 3 recommended dishes, and the GPT-generated analysis.

## Data Source

Menus and prices for 12 restaurants were collected via the QuickClick LINE store
API. Nutrition facts (calories, protein, fat, carbohydrates) were compiled
manually and merged into `data/restaurant_information.csv`
(columns: 商店名稱, 品項, 菜名, 價格, 熱量, 蛋白質(g), 脂肪(g), 碳水化合物(g)).

## Pipeline

1. Input guard: reject missing fields, bad formats, or out-of-range values.
2. Energy calc: compute BMR from gender-specific formula, scale by activity level to TDEE.
3. Body metrics: compute BMI and split TDEE into carb / protein / fat gram targets.
4. Menu filter: keep dishes whose calories fit the user's BMI band.
5. Pick: randomly sample up to 3 eligible dishes.
6. Analysis: send user profile + picks to GPT-3.5-turbo for a nutritionist-style writeup.
7. Return BMI, TDEE, macronutrients, the 3 dishes, and the analysis.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
