import { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIdea('');
    const words = input.trim().split(/\s+/);
    if (words.length < 2 || words.length > 3) {
      setError('Please enter 2 or 3 words.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5000/generate-idea', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ words }),
      });
      const data = await res.json();
      setIdea(data.idea || 'No idea returned.');
    } catch (err) {
      setError('Failed to fetch idea.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Moodyartist Test Form</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Enter 2 or 3 words"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>Generate Idea</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading...</p>}
      {idea && <div style={{ marginTop: '1em', fontWeight: 'bold' }}>{idea}</div>}
    </div>
  );
}

export default App;
