# AI Feast on the Table (simple)

An AI-powered personalized dining recommendation system that combines real restaurant menus with OpenAI GPT.

After the user enters their gender, age, height, weight, and weekly exercise days, the system:

1. Calculates BMI, Basal Metabolic Rate (BMR), and Total Daily Energy Expenditure (TDEE)
2. Filters the restaurant menu database by BMI range and randomly recommends 3 dishes
3. Calls GPT-3.5-turbo to generate a personalized nutrition analysis and dietary advice in the voice of a nutritionist

## Project Structure

```
ai-feast-on-the-table/
├── api/
│   └── index.py            # Flask backend (Vercel Serverless Function)
├── public/                 # Static frontend
│   ├── index.html          # Welcome page
│   ├── homepage.html       # Main app page
│   └── images/             # Background images
├── data/
│   └── restaurant_information.csv   # Restaurant menus with nutrition facts
├── docs/                   # Project proposal, architecture & flow diagrams
├── showcase/               # Demo results (kept local only, not in version control)
├── vercel.json             # Vercel routing config
├── requirements.txt
├── .env.example
└── LICENSE
```

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment variables
copy .env.example .env
# Edit .env and fill in your OPENAI_API_KEY

# 3. Start the app (Flask serves both the public/ static pages and the API)
python api/index.py
```

Then open <http://localhost:5000> in your browser.

## Deploying to Vercel

1. Sign in to [vercel.com](https://vercel.com) with your GitHub account and import this repository
2. Choose **Other** as the Framework Preset; no build command is needed
3. Add `OPENAI_API_KEY` under **Settings → Environment Variables**
4. Deploy — `public/` is served as static files by the CDN, and `/api/*` is automatically routed to `api/index.py`

## API

### `POST /api/recommend_food`

Example request:

```json
{
  "gender": "男性",
  "height": 175,
  "weight": 70,
  "age": 22,
  "exercise": 3
}
```

`gender` accepts `男性` (male) or `女性` (female); `exercise` is the number of exercise days per week (0–7).

The response includes the BMI, daily caloric need, recommended macronutrient intake, 3 recommended dishes, and a GPT-generated nutrition analysis.

## Data Source

Menus and prices of 12 restaurants were collected via the QuickClick LINE store API.
Nutrition facts (calories, protein, fat, carbohydrates) were compiled manually and merged into `data/restaurant_information.csv`.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
