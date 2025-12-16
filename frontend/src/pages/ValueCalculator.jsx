import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

function ValueCalculator() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleCompare = async (e) => {
        e.preventDefault();
        if (!query) return;

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch(`http://localhost:8000/api/compare/opportunity-cost?query=${query}`);
            const data = await response.json();

            if (data.error) {
                setError(data.error);
            } else {
                setResult(data);
            }
        } catch (err) {
            setError("Failed to compare items.");
        }
        setLoading(false);
    };

    const proteinMultiplier = result ?
        (result.benchmark_potential?.protein / result.fast_food_metrics?.protein).toFixed(1) : 0;

    const calorieMultiplier = result ?
        (result.benchmark_potential?.calories / result.fast_food_metrics?.calories).toFixed(1) : 0;

    return (
        <div className="page-container">
            <div className="container" style={{ maxWidth: '900px' }}>
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
                    <h1 style={{ marginBottom: '0.75rem' }}>
                        <span style={{ fontSize: '2.5rem' }}>⚖️</span> Value Opportunity Calculator
                    </h1>
                    <p style={{ fontSize: '1.125rem', maxWidth: '600px', margin: '0 auto' }}>
                        See what you're really missing out on when you choose fast food over grocery shopping.
                    </p>
                </div>

                {/* Search Card */}
                <div className="card card-elevated" style={{ marginBottom: '2rem' }}>
                    <form onSubmit={handleCompare} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                        <input
                            type="text"
                            className="input input-lg"
                            style={{ flex: 1, minWidth: '250px' }}
                            placeholder="What did you eat? (e.g. Big Mac, Crunchy Taco)"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="btn btn-primary"
                            style={{ padding: '1rem 2rem' }}
                        >
                            {loading ? (
                                <>
                                    <span className="animate-pulse">⏳</span>
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    🔍 Analyze Value
                                </>
                            )}
                        </button>
                    </form>
                    {error && (
                        <div className="callout callout-danger animate-fade-in-up" style={{ marginTop: '1rem' }}>
                            <p style={{ color: '#b91c1c', margin: 0 }}>❌ {error}</p>
                        </div>
                    )}
                </div>

                {/* Results */}
                {result && (
                    <div className="animate-fade-in-up" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

                        {/* Impact Callout */}
                        <div className="callout callout-danger animate-scale-in">
                            <h3 className="callout-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <span style={{ fontSize: '1.5rem' }}>💸</span>
                                The Harsh Truth
                            </h3>
                            <p style={{ fontSize: '1.125rem', color: '#991b1b', lineHeight: 1.7 }}>
                                You spent <strong style={{ fontSize: '1.25rem' }}>${result.cost?.toFixed(2)}</strong> on a {query}.
                                For that same price, you could have bought{' '}
                                <strong style={{
                                    fontSize: '1.75rem',
                                    background: 'linear-gradient(135deg, #dc2626, #991b1b)',
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent'
                                }}>
                                    {result.benchmark_potential?.quantity_lbs?.toFixed(1)} lbs
                                </strong>{' '}
                                of <strong>{result.comparison_item}</strong>!
                            </p>
                        </div>

                        {/* Stats Grid */}
                        <div className="grid grid-2">
                            {/* Nutrition Comparison */}
                            <div className="card card-elevated">
                                <div className="card-header">
                                    <h3 className="card-title">📊 Nutrition Breakdown</h3>
                                </div>

                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                                    {/* Calories Row */}
                                    <div>
                                        <div style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            marginBottom: '0.5rem',
                                            fontSize: '0.875rem'
                                        }}>
                                            <span style={{ fontWeight: '600' }}>🔥 Calories</span>
                                            <div style={{ display: 'flex', gap: '1.5rem' }}>
                                                <span style={{ color: 'var(--slate-500)' }}>
                                                    You: <strong style={{ color: 'var(--danger)' }}>{result.fast_food_metrics?.calories}</strong>
                                                </span>
                                                <span style={{ color: 'var(--slate-500)' }}>
                                                    Better: <strong style={{ color: 'var(--success)' }}>{result.benchmark_potential?.calories?.toFixed(0)}</strong>
                                                </span>
                                            </div>
                                        </div>
                                        <div className="comparison-bar">
                                            <div
                                                className="comparison-bar-fill danger"
                                                style={{
                                                    width: `${Math.min(100, (result.fast_food_metrics?.calories / result.benchmark_potential?.calories) * 100)}%`
                                                }}
                                            />
                                        </div>
                                    </div>

                                    {/* Protein Row */}
                                    <div>
                                        <div style={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            marginBottom: '0.5rem',
                                            fontSize: '0.875rem'
                                        }}>
                                            <span style={{ fontWeight: '600' }}>💪 Protein</span>
                                            <div style={{ display: 'flex', gap: '1.5rem' }}>
                                                <span style={{ color: 'var(--slate-500)' }}>
                                                    You: <strong style={{ color: 'var(--danger)' }}>{result.fast_food_metrics?.protein}g</strong>
                                                </span>
                                                <span style={{ color: 'var(--slate-500)' }}>
                                                    Better: <strong style={{ color: 'var(--success)' }}>{result.benchmark_potential?.protein?.toFixed(0)}g</strong>
                                                </span>
                                            </div>
                                        </div>
                                        <div className="comparison-bar">
                                            <div
                                                className="comparison-bar-fill danger"
                                                style={{
                                                    width: `${Math.min(100, (result.fast_food_metrics?.protein / result.benchmark_potential?.protein) * 100)}%`
                                                }}
                                            />
                                        </div>
                                    </div>

                                    {/* Multiplier Badges */}
                                    <div style={{
                                        display: 'flex',
                                        gap: '1rem',
                                        paddingTop: '0.75rem',
                                        borderTop: '1px solid var(--slate-200)',
                                        justifyContent: 'center'
                                    }}>
                                        <div className="stat-card" style={{ padding: '0.75rem 1.5rem' }}>
                                            <div className="stat-value" style={{ fontSize: '1.75rem' }}>{proteinMultiplier}x</div>
                                            <div className="stat-label">more protein</div>
                                        </div>
                                        <div className="stat-card" style={{ padding: '0.75rem 1.5rem' }}>
                                            <div className="stat-value" style={{ fontSize: '1.75rem' }}>{calorieMultiplier}x</div>
                                            <div className="stat-label">more calories</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Chart */}
                            <div className="card card-elevated" style={{ height: '350px' }}>
                                <div className="card-header">
                                    <h3 className="card-title">📈 Protein Comparison</h3>
                                </div>
                                <ResponsiveContainer width="100%" height="85%">
                                    <BarChart
                                        data={[
                                            { name: 'Your Meal', protein: result.fast_food_metrics?.protein, fill: '#ef4444' },
                                            { name: 'Smart Choice', protein: result.benchmark_potential?.protein, fill: '#22c55e' }
                                        ]}
                                        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                                    >
                                        <defs>
                                            <linearGradient id="redGradient" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="0%" stopColor="#f87171" />
                                                <stop offset="100%" stopColor="#ef4444" />
                                            </linearGradient>
                                            <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="0%" stopColor="#4ade80" />
                                                <stop offset="100%" stopColor="#22c55e" />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" stroke="var(--slate-200)" />
                                        <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'var(--slate-600)' }} />
                                        <YAxis tick={{ fontSize: 12, fill: 'var(--slate-600)' }} />
                                        <Tooltip
                                            contentStyle={{
                                                background: 'white',
                                                border: '1px solid var(--slate-200)',
                                                borderRadius: 'var(--radius-md)',
                                                boxShadow: 'var(--shadow-lg)'
                                            }}
                                            formatter={(value) => [`${value}g`, 'Protein']}
                                        />
                                        <Bar dataKey="protein" radius={[8, 8, 0, 0]}>
                                            <Cell fill="url(#redGradient)" />
                                            <Cell fill="url(#greenGradient)" />
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Call to Action */}
                        <div className="callout callout-success animate-fade-in-up stagger-2">
                            <h3 className="callout-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <span style={{ fontSize: '1.5rem' }}>💡</span>
                                The Smart Choice
                            </h3>
                            <p style={{ color: '#166534', fontSize: '1rem', margin: 0 }}>
                                Next time, consider grabbing <strong>{result.comparison_item}</strong> from your local grocery store.
                                You'll get more nutrition for your dollar and build better eating habits!
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default ValueCalculator;
