# CheapNut

CheapNut is a comprehensive "Best Nutrition Per Dollar" analysis engine. It goes beyond simple price comparison by calculating the nutritional density of foods per dollar spent, helping users identify the most efficient ways to fuel their bodies. It also features a "Value Opportunity" calculator that compares fast food purchases against high-efficiency staples.

## Key Features

- **🏆 Best Value Leaderboard:**
    - continuously updated ranking of foods with the highest Protein Per Dollar and Calories Per Dollar.
    - Powered by a "Smart Pantry" engine that scrapes real-time prices for high-efficiency staples (Lentils, Frozen Veggies, Eggs, etc.).
  
- **🍔 Value Opportunity Calculator:**
    - Input a fast food item (e.g. "Big Mac") and see the "Opportunity Cost".
    - Visualizes how much *more* nutrition (protein, volume, calories) you could have purchased for the same price using Smart Pantry staples.

- **🛒 Multi-Store Scraping:**
    - Real-time Selenium scrapers for Walmart, Safeway, Trader Joe's, and major fast food chains.
    - Automatic integration with OpenFoodFacts for nutritional data.

- **📊 Data Visualization:**
    - Interactive charts powered by `Recharts` to visualize value density and comparisons.

## Tech Stack

- **Frontend:** React, Vite, TailwindCSS, Recharts
- **Backend:** Python (FastAPI), SQLAlchemy, Selenium
- **Data Source:** OpenFoodFacts API, Direct Store Scraping

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.10+)
- Chrome/Chromium (for Selenium scraping)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/JonasComlita/CheapNut.git
    cd CheapNut
    ```

2.  **Frontend Setup:**
    ```bash
    cd frontend
    npm install
    ```

3.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Backend:**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    *The API will start at http://localhost:8000*

2.  **Start the Frontend:**
    ```bash
    cd frontend
    npm run dev
    ```
    *The App will start at http://localhost:5173*

3.  **Update Benchmarks:**
    - Go to the **Leaderboard** page.
    - Click **Refresh Prices** to trigger the background scraping routine for staple items.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
