import React, { useState } from 'react';

function App() {
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
            <h1>CheapNut</h1>
            <p>Compare cost and nutrition of home cooking vs fast food.</p>

            <form className="search-box" onSubmit={handleSearch}>
                <input
                    type="text"
                    placeholder="Enter food item (e.g. chicken, beans)"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </form>

            {results && (
                <div className="results-container">
                    <div className="column">
                        <h2>Grocery Alternatives</h2>
                        {results.grocery.length === 0 ? <p>No results found.</p> :
                            results.grocery.map((item, index) => (
                                <div key={index} className="card">
                                    <h3>{item.name}</h3>
                                    <div className="price">${item.price.toFixed(2)} / {item.unit}</div>
                                    <p>Store: {item.store}</p>
                                    <div className="nutrition">
                                        <strong>Nutrition (per serving):</strong>
                                        <pre>{JSON.stringify(item.nutrition, null, 2)}</pre>
                                    </div>
                                </div>
                            ))
                        }
                    </div>

                    <div className="column">
                        <h2>Fast Food / Restaurant</h2>
                        {results.fastfood.length === 0 ? <p>No results found.</p> :
                            results.fastfood.map((item, index) => (
                                <div key={index} className="card">
                                    <h3>{item.name}</h3>
                                    <div className="price">${item.price.toFixed(2)} / {item.unit}</div>
                                    <p>Store: {item.store}</p>
                                    <div className="nutrition">
                                        <strong>Nutrition (per serving):</strong>
                                        <pre>{JSON.stringify(item.nutrition, null, 2)}</pre>
                                    </div>
                                </div>
                            ))
                        }
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
