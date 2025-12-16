import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import LeaderboardPage from './pages/LeaderboardPage';
import ValueCalculator from './pages/ValueCalculator';

function NavLink({ to, children }) {
    const location = useLocation();
    const isActive = location.pathname === to;

    return (
        <Link
            to={to}
            className={`nav-link ${isActive ? 'active' : ''}`}
        >
            {children}
        </Link>
    );
}

function Navigation() {
    return (
        <nav className="nav-container">
            <div className="nav-inner">
                <Link to="/" className="nav-logo">
                    <img src="/logo.png" alt="CheapNut Logo" style={{ width: '36px', height: '36px', borderRadius: 'var(--radius-md)' }} />
                    CheapNut
                </Link>
                <div className="nav-links">
                    <NavLink to="/">Search</NavLink>
                    <NavLink to="/leaderboard">Leaderboard</NavLink>
                    <NavLink to="/calculator">Calculator</NavLink>
                </div>
            </div>
        </nav>
    );
}

function Home() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/api/search?q=${query}`);
            const data = await response.json();
            setResults(data);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            {/* Hero Section */}
            <div className="hero">
                <div className="hero-content">
                    <h1 className="animate-fade-in-up">🥜 CheapNut</h1>
                    <p className="animate-fade-in-up stagger-1">
                        Discover the true cost of your food choices. Compare grocery prices with fast food and make smarter decisions for your wallet and health.
                    </p>

                    <form className="search-box animate-fade-in-up stagger-2" onSubmit={handleSearch}>
                        <input
                            type="text"
                            className="input input-lg"
                            placeholder="Search for any food (e.g. chicken, beans, rice)..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <button type="submit" disabled={loading} className="btn btn-primary">
                            {loading ? (
                                <>
                                    <span className="animate-pulse">⏳</span>
                                    Searching...
                                </>
                            ) : (
                                <>
                                    🔍 Search
                                </>
                            )}
                        </button>
                    </form>
                </div>
            </div>

            {/* Results */}
            {results && (
                <div className="results-container animate-fade-in-up">
                    <div className="column">
                        <h2 className="grocery-title">
                            <span>🥬</span>
                            Grocery Alternatives
                        </h2>
                        {results.grocery.length === 0 ? (
                            <div className="card">
                                <p style={{ textAlign: 'center', color: 'var(--slate-500)' }}>
                                    No grocery items found matching your search.
                                </p>
                            </div>
                        ) : (
                            results.grocery.map((item, index) => (
                                <div
                                    key={index}
                                    className="result-card animate-fade-in-up"
                                    style={{ animationDelay: `${index * 0.1}s` }}
                                >
                                    <div className="result-card-header">
                                        <h3 className="result-card-title">{item.name}</h3>
                                        <div className="result-card-price grocery">
                                            ${item.price.toFixed(2)}
                                            <span style={{ fontSize: '0.875rem', fontWeight: '400', color: 'var(--slate-500)' }}>
                                                /{item.unit}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="result-card-store">
                                        <span className="badge badge-success">{item.store}</span>
                                    </div>
                                    <div className="nutrition-grid">
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Calories</span>
                                            <span className="nutrition-value">{item.nutrition?.calories || '—'}</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Protein</span>
                                            <span className="nutrition-value">{item.nutrition?.protein || '—'}g</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Carbs</span>
                                            <span className="nutrition-value">{item.nutrition?.carbs || '—'}g</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Fat</span>
                                            <span className="nutrition-value">{item.nutrition?.fat || '—'}g</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>

                    <div className="column">
                        <h2 className="fastfood-title">
                            <span>🍔</span>
                            Fast Food / Restaurant
                        </h2>
                        {results.fastfood.length === 0 ? (
                            <div className="card">
                                <p style={{ textAlign: 'center', color: 'var(--slate-500)' }}>
                                    No fast food items found matching your search.
                                </p>
                            </div>
                        ) : (
                            results.fastfood.map((item, index) => (
                                <div
                                    key={index}
                                    className="result-card animate-fade-in-up"
                                    style={{ animationDelay: `${index * 0.1}s` }}
                                >
                                    <div className="result-card-header">
                                        <h3 className="result-card-title">{item.name}</h3>
                                        <div className="result-card-price fastfood">
                                            ${item.price.toFixed(2)}
                                            <span style={{ fontSize: '0.875rem', fontWeight: '400', color: 'var(--slate-500)' }}>
                                                /{item.unit}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="result-card-store">
                                        <span className="badge badge-danger">{item.store}</span>
                                    </div>
                                    <div className="nutrition-grid">
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Calories</span>
                                            <span className="nutrition-value">{item.nutrition?.calories || '—'}</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Protein</span>
                                            <span className="nutrition-value">{item.nutrition?.protein || '—'}g</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Carbs</span>
                                            <span className="nutrition-value">{item.nutrition?.carbs || '—'}g</span>
                                        </div>
                                        <div className="nutrition-item">
                                            <span className="nutrition-label">Fat</span>
                                            <span className="nutrition-value">{item.nutrition?.fat || '—'}g</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

function App() {
    return (
        <Router>
            <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
                <Navigation />

                <main style={{ flex: 1 }}>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/leaderboard" element={<LeaderboardPage />} />
                        <Route path="/calculator" element={<ValueCalculator />} />
                    </Routes>
                </main>

                <footer className="footer">
                    <p>
                        🥜 <strong>CheapNut</strong> — Making smart food choices easier, one comparison at a time.
                    </p>
                </footer>
            </div>
        </Router>
    );
}

export default App;
