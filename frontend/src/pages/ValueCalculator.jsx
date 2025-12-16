import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

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

    return (
        <div className="container mx-auto p-4 max-w-4xl">
            <h1 className="text-3xl font-bold text-center mb-8 text-slate-800">Value Opportunity Calculator</h1>

            <div className="bg-white p-6 rounded-lg shadow-lg mb-8">
                <form onSubmit={handleCompare} className="flex gap-4">
                    <input
                        type="text"
                        className="flex-1 p-3 border border-slate-300 rounded-lg text-lg focus:ring-2 focus:ring-blue-500 outline-none"
                        placeholder="What did you eat? (e.g. Big Mac, Crunchy Taco)"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg transition-colors"
                    >
                        {loading ? 'Analyzing...' : 'Analyze Value'}
                    </button>
                </form>
                {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
            </div>

            {result && (
                <div className="space-y-6">
                    <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded animate-fade-in">
                        <h3 className="text-2xl font-bold text-red-800 mb-2">The Harsh Truth</h3>
                        <p className="text-lg text-red-700">
                            You spent <span className="font-bold">${result.cost?.toFixed(2)}</span> on a {query}.
                            For that same price, you could have bought <span className="font-bold text-2xl">{result.benchmark_potential?.quantity_lbs?.toFixed(1)} lbs</span> of {result.comparison_item}!
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Text Stats */}
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h4 className="text-lg font-semibold mb-4 text-slate-600">Nutrition Breakdown</h4>
                            <div className="space-y-4">
                                <div className="flex justify-between border-b pb-2">
                                    <span>Calories</span>
                                    <div className="text-right">
                                        <div className="text-slate-500 text-sm">You Got</div>
                                        <div className="font-bold">{result.fast_food_metrics?.calories}</div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-green-600 text-sm">Could Have Gotten</div>
                                        <div className="font-bold text-green-600">{result.benchmark_potential?.calories?.toFixed(0)}</div>
                                    </div>
                                </div>
                                <div className="flex justify-between border-b pb-2">
                                    <span>Protein</span>
                                    <div className="text-right">
                                        <div className="text-slate-500 text-sm">You Got</div>
                                        <div className="font-bold">{result.fast_food_metrics?.protein}g</div>
                                    </div>
                                    <div className="text-right">
                                        <div className="text-green-600 text-sm">Could Have Gotten</div>
                                        <div className="font-bold text-green-600">{result.benchmark_potential?.protein?.toFixed(0)}g</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Chart */}
                        <div className="bg-white p-6 rounded-lg shadow h-80">
                            <h4 className="text-lg font-semibold mb-4 text-slate-600">Protein Multiplier</h4>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart
                                    data={[
                                        { name: 'Your Meal', protein: result.fast_food_metrics?.protein },
                                        { name: 'Smart Choice', protein: result.benchmark_potential?.protein }
                                    ]}
                                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                                >
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="protein" fill="#3b82f6" radius={[4, 4, 0, 0]}>
                                        {
                                            [{ name: 'Your Meal' }, { name: 'Smart Choice' }].map((entry, index) => (
                                                <cell key={`cell-${index}`} fill={index === 0 ? '#ef4444' : '#22c55e'} />
                                            ))
                                        }
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ValueCalculator;
