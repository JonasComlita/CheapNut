import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

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
        // Trigger background refresh
        try {
            await fetch('http://localhost:8000/api/benchmarks/refresh', { method: 'POST' });
            alert('Scrapers started! This will take a few minutes. Check back soon for updated prices.');
        } catch (e) {
            alert('Failed to start refresh');
        }
    }

    return (
        <div className="container mx-auto p-4">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Best Value Leaderboard</h1>
                <button
                    onClick={handleRefresh}
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                    Refresh Prices
                </button>
            </div>

            <div className="mb-6 flex space-x-4">
                <button
                    onClick={() => setMetric('protein')}
                    className={`py-2 px-4 rounded ${metric === 'protein' ? 'bg-blue-600 text-white' : 'bg-slate-200'}`}
                >
                    Protein Per Dollar
                </button>
                <button
                    onClick={() => setMetric('calories')}
                    className={`py-2 px-4 rounded ${metric === 'calories' ? 'bg-blue-600 text-white' : 'bg-slate-200'}`}
                >
                    Calories Per Dollar
                </button>
                <button
                    onClick={() => setMetric('price')}
                    className={`py-2 px-4 rounded ${metric === 'price' ? 'bg-blue-600 text-white' : 'bg-slate-200'}`}
                >
                    Lowest Price
                </button>
            </div>

            {loading ? (
                <div>Loading top contenders...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <h2 className="text-xl font-semibold mb-4">Top 10 Rankings</h2>
                        <div className="overflow-x-auto">
                            <table className="min-w-full text-left">
                                <thead>
                                    <tr className="border-b">
                                        <th className="py-2">Item</th>
                                        <th className="py-2">Store</th>
                                        <th className="py-2">Price</th>
                                        <th className="py-2">Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.map((item) => (
                                        <tr key={item.id} className="border-b hover:bg-slate-50">
                                            <td className="py-2">{item.name}</td>
                                            <td className="py-2 text-sm text-slate-500">{item.store}</td>
                                            <td className="py-2 font-mono">${item.lowest_price?.toFixed(2)}</td>
                                            <td className="py-2 font-bold text-green-600">
                                                {metric === 'protein' && `${item.protein_per_dollar?.toFixed(1)}g/$`}
                                                {metric === 'calories' && `${item.calories_per_dollar?.toFixed(0)} kcal/$`}
                                                {metric === 'price' && `$${item.price_per_100g?.toFixed(2)}/100g`}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow h-96">
                        <h2 className="text-xl font-semibold mb-4">Visual Comparison</h2>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data} layout="vertical" margin={{ left: 50 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis type="number" />
                                <YAxis dataKey="name" type="category" width={150} tick={{ fontSize: 12 }} />
                                <Tooltip />
                                <Bar
                                    dataKey={metric === 'protein' ? 'protein_per_dollar' : metric === 'calories' ? 'calories_per_dollar' : 'lowest_price'}
                                    fill="#3b82f6"
                                    name={metric === 'protein' ? 'Protein (g/$)' : 'Value'}
                                />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            )}
        </div>
    );
}

export default LeaderboardPage;
