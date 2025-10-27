import React, { useState, useCallback } from 'react';
import { Bot, Zap, Loader2, BarChart2, AlertTriangle, Code, Play } from 'lucide-react';

// --- Configuration ---
const BACKEND_URL = "http://localhost:8000/query";

const App = () => {
    const [query, setQuery] = useState("Analyze the production trend of Wheat in Maharashtra and Karnataka over the period available in the database, correlate this trend with the rainfall data, and summarize the apparent impact.");
    const [response, setResponse] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dbStatus, setDbStatus] = useState("Initializing...");

    // Check DB status on load (basic health check)
    React.useEffect(() => {
        const checkStatus = async () => {
            try {
                // Check root endpoint for status
                const res = await fetch("http://localhost:8000/"); 
                if (res.ok) {
                    setDbStatus("API Ready (Backend Online)");
                } else {
                    setDbStatus("API Running, DB Status Unknown");
                }
            } catch (e) {
                setDbStatus("Backend Offline (Did you run the FastAPI server?)");
            }
        };
        checkStatus();
    }, []);

    const handleQuery = useCallback(async () => {
        if (!query.trim()) return;

        setIsLoading(true);
        setError(null);
        setResponse("");

        try {
            const fetchResponse = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            const data = await fetchResponse.json();

            if (!fetchResponse.ok) {
                setError(data.detail || `Error: Failed to fetch response (${fetchResponse.status})`);
                setResponse("");
                return;
            }

            setResponse(data.answer);

        } catch (err) {
            console.error("Fetch Error:", err);
            setError("Could not connect to the backend API. Please ensure the FastAPI server is running.");
        } finally {
            setIsLoading(false);
        }
    }, [query]);

    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8 font-sans">
            <script src="https://cdn.tailwindcss.com"></script>
            <style>{`
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
                body { font-family: 'Inter', sans-serif; }
                .fade-in { animation: fadeIn 0.5s ease-out; }
                @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            `}</style>
            
            <div className="max-w-5xl mx-auto">
                <header className="text-center mb-10 p-6 bg-white rounded-xl shadow-lg border-b-4 border-indigo-500">
                    <h1 className="text-4xl font-extrabold text-indigo-700 flex items-center justify-center">
                        <Bot className="h-8 w-8 mr-3 text-green-500" />
                        Project Samarth Analyst MVP
                    </h1>
                    <p className="mt-2 text-lg text-gray-600">Cross-Domain Data Synthesis Engine (FastAPI + React)</p>
                    <div className="mt-4 flex justify-center items-center text-sm">
                        <BarChart2 className="w-4 h-4 mr-2 text-blue-500" />
                        <span className={`font-semibold ${dbStatus.includes('Ready') ? 'text-green-600' : dbStatus.includes('Offline') ? 'text-red-600' : 'text-yellow-600'}`}>
                            Backend Status: {dbStatus}
                        </span>
                    </div>
                </header>

                {/* Input Area */}
                <div className="bg-white p-6 rounded-xl shadow-lg mb-8 border-t-4 border-green-500 fade-in">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4">Ask a Cross-Domain Question</h2>
                    <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g., Compare the production and average rainfall trends between State X and State Y."
                        rows="4"
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 resize-none text-gray-700 shadow-inner"
                    ></textarea>
                    <button
                        onClick={handleQuery}
                        disabled={isLoading}
                        className={`mt-4 w-full px-6 py-3 rounded-lg text-white font-semibold transition duration-150 ease-in-out flex items-center justify-center ${
                            isLoading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-md hover:shadow-lg'
                        }`}
                    >
                        {isLoading ? (
                            <Loader2 className="animate-spin h-5 w-5 mr-3 text-white" />
                        ) : (
                            <Zap className="h-5 w-5 mr-2" />
                        )}
                        {isLoading ? 'Agent Reasoning...' : 'Execute Analysis'}
                    </button>
                    {error && (
                        <div className="mt-4 flex items-center p-3 bg-red-100 rounded-lg text-red-600 font-medium">
                            <AlertTriangle className="h-5 w-5 mr-2" />
                            {error}
                        </div>
                    )}
                </div>

                {/* Output Area */}
                <div className="bg-white p-6 rounded-xl shadow-2xl border-t-8 border-green-600 fade-in">
                    <h2 className="text-xl font-extrabold text-green-700 mb-4">
                        <Bot className="h-5 w-5 mr-2 inline-block" />
                        Samarth Insight: Data-Backed Conclusion
                    </h2>
                    <div className="min-h-40 bg-gray-50 p-4 rounded-lg border border-gray-200 whitespace-pre-wrap text-gray-800 leading-relaxed shadow-inner">
                        {isLoading ? (
                            <p className="text-gray-500 italic flex items-center">
                                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                                Waiting for the LLM Analyst to execute SQL and synthesize the results...
                            </p>
                        ) : response ? (
                            <p className="fade-in">{response}</p>
                        ) : (
                            <p className="text-gray-500 italic">
                                Your synthesized, cross-domain insights will appear here after the agent executes the query against the database.
                            </p>
                        )}
                    </div>
                </div>

                {/* Instructions */}
                <div className="mt-8 p-4 bg-blue-100 border-l-4 border-blue-500 rounded-lg text-sm text-blue-800">
                    <p className="font-bold mb-2 flex items-center"><Play className="h-4 w-4 mr-2" />Setup Instructions:</p>
                    <ol className="list-decimal list-inside space-y-1">
                        <li>**Update Keys:** Replace placeholder IDs/keys in `backend/data/data_connector.py` with your actual **data.gov.in** API Key and Resource IDs.</li>
                        <li>**Set LLM Key:** Set the **`GEMINI_API_KEY`** environment variable.</li>
                        <li>**Start Backend:** Run the FastAPI server: <Code className="h-4 w-4 inline-block mx-1" />`python -m uvicorn backend.app:app --reload`</li>
                        <li>**Run Frontend:** The React interface will automatically attempt to connect to the backend.</li>
                    </ol>
                </div>

            </div>
        </div>
    );
};

export default App;
