# CheapNut

CheapNut is a comprehensive grocery price comparison and nutrition analysis tool. It allows users to search for products, compare prices across different grocery stores (starting with Trader Joe's), and view detailed nutritional information sourced from OpenFoodFacts.

## Features

- **Store Price Comparison:** Real-time web scraping to get current prices from major grocery chains.
- **Nutritional Info:** Automatic integration with OpenFoodFacts to provide calories, macronutrients (protein, carbs, fat), and vitamins for searched items.
- **Real-time Scraping:** Built using Selenium to handle dynamic store websites effectively.
- **Modern Frontend:** Fast and responsive user interface built with React and Vite.

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python
- **Scraping:** Selenium, Beautiful Soup (planned)
- **Data Source:** OpenFoodFacts API

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Chrome/Chromium (for Selenium scraping)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/JonasComlita/CheapNut.git
    cd CheapNut
    ```

2.  **Frontend Setup:**
    Navigate to the frontend directory and install dependencies:
    ```bash
    cd frontend
    npm install
    ```

3.  **Backend Setup:**
    Navigate to the backend directory and ensure you have the necessary Python packages installed:
    ```bash
    cd backend
    # It allows you to create a virtual environment first
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt # If requirements.txt exists, otherwise install manually:
    pip install selenium requests
    ```

## Usage

1.  **Start the Frontend:**
    ```bash
    cd frontend
    npm run dev
    ```

2.  **Start the Backend:**
    (Instructions for running the backend service - assuming a main entry point exists or will be created)
    ```bash
    cd backend
    python main.py # (or appropriate entry file)
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
