import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

function LeaderboardPage() {
    const [data, setData] = useState([]);
    const [metric, setMetric] = useState('protein');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchLeaderboard();
    }, [metric]);

    const fetchLeaderboard = async () => {
        setLoading(true);
        try {
            const response = await fetch(`http://localhost:8000/api/benchmarks/leaderboard?metric=${metric}`);
            const jsonData = await response.json();
            setData(jsonData);
        } catch (error) {
            console.error("Error fetching leaderboard:", error);
        }
        setLoading(false);
    };

    const handleRefresh = async () => {
        try {
            await fetch('http://localhost:8000/api/benchmarks/refresh', { method: 'POST' });
            alert('Scrapers started! This will take a few minutes. Check back soon for updated prices.');
        } catch (e) {
            alert('Failed to start refresh');
        }
    };

    const getRankBadge = (index) => {
        if (index === 0) return <span className="rank-badge gold">🥇</span>;
        if (index === 1) return <span className="rank-badge silver">🥈</span>;
        if (index === 2) return <span className="rank-badge bronze">🥉</span>;
        return <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            background: 'var(--slate-100)',
            fontSize: '0.75rem',
            fontWeight: '600',
            color: 'var(--slate-600)'
        }}>{index + 1}</span>;
    };

    const getMetricValue = (item) => {
        if (metric === 'protein') return `${item.protein_per_dollar?.toFixed(1)}g/$`;
        if (metric === 'calories') return `${item.calories_per_dollar?.toFixed(0)} kcal/$`;
        return `$${item.price_per_100g?.toFixed(2)}/100g`;
    };

    const getBarDataKey = () => {
        if (metric === 'protein') return 'protein_per_dollar';
        if (metric === 'calories') return 'calories_per_dollar';
        return 'lowest_price';
    };

    const getGradientColors = () => {
        if (metric === 'protein') return ['#10b981', '#059669'];
        if (metric === 'calories') return ['#f59e0b', '#d97706'];
        return ['#3b82f6', '#1d4ed8'];
    };

    const colors = getGradientColors();

    return (
        <div className="page-container">
            <div className="container">
                {/* Header */}
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '2rem',
                    flexWrap: 'wrap',
                    gap: '1rem'
                }}>
                    <div>
                        <h1 style={{ marginBottom: '0.5rem' }}>🏆 Best Value Leaderboard</h1>
                        <p>Find the most nutritious foods for your dollar</p>
                    </div>
                    <button onClick={handleRefresh} className="btn btn-primary">
                        🔄 Refresh Prices
                    </button>
                </div>

                {/* Metric Toggle */}
                <div className="toggle-group" style={{ marginBottom: '2rem' }}>
                    <button
                        onClick={() => setMetric('protein')}
                        className={`toggle-btn ${metric === 'protein' ? 'active' : ''}`}
                    >
                        💪 Protein Per $
                    </button>
                    <button
                        onClick={() => setMetric('calories')}
                        className={`toggle-btn ${metric === 'calories' ? 'active' : ''}`}
                    >
                        🔥 Calories Per $
                    </button>
                    <button
                        onClick={() => setMetric('price')}
                        className={`toggle-btn ${metric === 'price' ? 'active' : ''}`}
                    >
                        💰 Lowest Price
                    </button>
                </div>

                {loading ? (
                    <div className="grid grid-2">
                        <div className="card">
                            <div className="skeleton skeleton-heading"></div>
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="skeleton skeleton-card"></div>
                            ))}
                        </div>
                        <div className="card">
                            <div className="skeleton skeleton-heading"></div>
                            <div className="skeleton" style={{ height: '300px' }}></div>
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-2">
                        {/* Table */}
                        <div className="card card-elevated animate-fade-in-up">
                            <div className="card-header">
                                <h2 className="card-title">Top 10 Rankings</h2>
                                <span className="badge badge-primary">{data.length} items</span>
                            </div>
                            <div className="table-container">
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th style={{ width: '50px' }}>Rank</th>
                                            <th>Item</th>
                                            <th>Store</th>
                                            <th style={{ textAlign: 'right' }}>Price</th>
                                            <th style={{ textAlign: 'right' }}>Value</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {data.map((item, index) => (
                                            <tr key={item.id} className="animate-fade-in-up" style={{ animationDelay: `${index * 0.05}s` }}>
                                                <td>{getRankBadge(index)}</td>
                                                <td style={{ fontWeight: '500' }}>{item.name}</td>
                                                <td>
                                                    <span className="badge badge-info">{item.store}</span>
                                                </td>
                                                <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>
                                                    ${item.lowest_price?.toFixed(2)}
                                                </td>
                                                <td style={{
                                                    textAlign: 'right',
                                                    fontWeight: '700',
                                                    color: metric === 'price' ? 'var(--info)' : 'var(--success)'
                                                }}>
                                                    {getMetricValue(item)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Chart */}
                        <div className="card card-elevated animate-fade-in-up stagger-1" style={{ height: '500px' }}>
                            <div className="card-header">
                                <h2 className="card-title">Visual Comparison</h2>
                            </div>
                            <ResponsiveContainer width="100%" height="90%">
                                <BarChart
                                    data={data.slice(0, 10)}
                                    layout="vertical"
                                    margin={{ left: 20, right: 30, top: 10, bottom: 10 }}
                                >
                                    <defs>
                                        <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor={colors[0]} />
                                            <stop offset="100%" stopColor={colors[1]} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="var(--slate-200)" />
                                    <XAxis type="number" tick={{ fontSize: 12, fill: 'var(--slate-600)' }} />
                                    <YAxis
                                        dataKey="name"
                                        type="category"
                                        width={120}
                                        tick={{ fontSize: 11, fill: 'var(--slate-700)' }}
                                    />
                                    <Tooltip
                                        contentStyle={{
                                            background: 'white',
                                            border: '1px solid var(--slate-200)',
                                            borderRadius: 'var(--radius-md)',
                                            boxShadow: 'var(--shadow-lg)',
                                            fontSize: '0.875rem'
                                        }}
                                    />
                                    <Bar
                                        dataKey={getBarDataKey()}
                                        fill="url(#barGradient)"
                                        radius={[0, 6, 6, 0]}
                                    >
                                        {data.slice(0, 10).map((entry, index) => (
                                            <Cell
                                                key={`cell-${index}`}
                                                fillOpacity={1 - (index * 0.06)}
                                            />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default LeaderboardPage;
