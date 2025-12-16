import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import LeaderboardPage from './pages/LeaderboardPage';
import ValueCalculator from './pages/ValueCalculator';

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
            <h1 className="text-4xl font-bold text-center mb-4 text-slate-800">CheapNut</h1>
            <p className="text-center text-slate-600 mb-8">Compare cost and nutrition of home cooking vs fast food.</p>

            <form className="search-box max-w-xl mx-auto flex gap-2 mb-8" onSubmit={handleSearch}>
                <input
                    type="text"
                    className="flex-1 p-3 border rounded shadow-sm"
                    placeholder="Enter food item (e.g. chicken, beans)"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" disabled={loading} className="bg-blue-600 text-white px-6 rounded font-bold">
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>

            {results && (
                <div className="results-container opacity-100 transition-opacity duration-500">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="column">
                            <h2 className="text-2xl font-bold mb-4 text-green-700">Grocery Alternatives</h2>
                            {results.grocery.length === 0 ? <p>No results found.</p> :
                                results.grocery.map((item, index) => (
                                    <div key={index} className="bg-white p-4 rounded shadow mb-4">
                                        <h3 className="font-bold text-lg">{item.name}</h3>
                                        <div className="text-green-600 font-bold">${item.price.toFixed(2)} / {item.unit}</div>
                                        <p className="text-sm text-slate-500">Store: {item.store}</p>
                                        <div className="mt-2 text-xs bg-slate-100 p-2 rounded">
                                            <strong>Nutrition:</strong>
                                            <pre>{JSON.stringify(item.nutrition, null, 2)}</pre>
                                        </div>
                                    </div>
                                ))
                            }
                        </div>

                        <div className="column">
                            <h2 className="text-2xl font-bold mb-4 text-red-700">Fast Food / Restaurant</h2>
                            {results.fastfood.length === 0 ? <p>No results found.</p> :
                                results.fastfood.map((item, index) => (
                                    <div key={index} className="bg-white p-4 rounded shadow mb-4">
                                        <h3 className="font-bold text-lg">{item.name}</h3>
                                        <div className="text-red-600 font-bold">${item.price.toFixed(2)} / {item.unit}</div>
                                        <p className="text-sm text-slate-500">Store: {item.store}</p>
                                        <div className="mt-2 text-xs bg-slate-100 p-2 rounded">
                                            <strong>Nutrition:</strong>
                                            <pre>{JSON.stringify(item.nutrition, null, 2)}</pre>
                                        </div>
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
                <nav className="bg-white shadow p-4 mb-8">
                    <div className="container mx-auto flex justify-between items-center">
                        <Link to="/" className="text-xl font-bold text-blue-600 flex items-center gap-2">
                            <img src="/logo.png" alt="CheapNut Logo" className="h-8 w-8 object-contain" onError={(e) => e.target.style.display = 'none'} />
                            CheapNut
                        </Link>
                        <div className="space-x-6">
                            <Link to="/" className="hover:text-blue-600 font-medium">Search</Link>
                            <Link to="/leaderboard" className="hover:text-blue-600 font-medium">Leaderboard</Link>
                            <Link to="/calculator" className="hover:text-blue-600 font-medium">Value Calculator</Link>
                        </div>
                    </div>
                </nav>

                <div className="container mx-auto px-4 pb-12">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/leaderboard" element={<LeaderboardPage />} />
                        <Route path="/calculator" element={<ValueCalculator />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
