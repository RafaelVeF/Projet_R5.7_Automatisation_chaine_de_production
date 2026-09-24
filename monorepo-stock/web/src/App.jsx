import { useState } from 'react';

export default function App() {
  const [status, setStatus] = useState({ loading: false, data: null, error: null });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.fileInput.files[0];
    if (!file) return;

    setStatus({ loading: true, data: null, error: null });
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/scan", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      setStatus({ loading: false, data, error: null });
    } catch (err) {
      setStatus({ loading: false, data: null, error: err.message });
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h2>Gestion de Stocks - Scanner</h2>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input type="file" name="fileInput" accept="image/*" required style={{ display: 'block', marginBottom: '10px' }} />
        <button type="submit" disabled={status.loading}>
          {status.loading ? 'Traitement...' : 'Valider'}
        </button>
      </form>

      {status.error && <p style={{ color: 'red' }}>Échec de connexion : {status.error}</p>}
      {status.data && <pre style={{ background: '#eee', padding: '10px' }}>{JSON.stringify(status.data, null, 2)}</pre>}
    </div>
  );
}