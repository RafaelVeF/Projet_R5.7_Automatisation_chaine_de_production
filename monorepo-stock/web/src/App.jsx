import { useState } from 'react';

export default function App() {
  const [status, setStatus] = useState({ loading: false, data: null, error: null });
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
      setStatus({ loading: false, data: null, error: null });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.fileInput.files[0];
    if (!file) return;

    setStatus({ loading: true, data: null, error: null });
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch('/api/scan', {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Erreur serveur (HTTP ${response.status})`);
      
      const data = await response.json();
      setStatus({ loading: false, data, error: null });
    } catch (err) {
      setStatus({ loading: false, data: null, error: err.message });
    }
  };

  return (
    <div style={{ maxWidth: '560px', margin: '40px auto', fontFamily: 'system-ui, -apple-system, sans-serif', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)', background: '#fff' }}>
      <h2 style={{ marginTop: 0, color: '#1e293b' }}>📦 Gestion de Stocks - Scanner QR</h2>
      <p style={{ color: '#64748b', fontSize: '14px' }}>
        Acheminement : Interface Web &rarr; Ambassadeur &rarr; Post-Traitement &rarr; Ambassadeur &rarr; Resultat.
      </p>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input 
          type="file" 
          name="fileInput" 
          accept="image/*" 
          onChange={handleFileChange}
          required 
          style={{ display: 'block', marginBottom: '16px', width: '100%', padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1' }} 
        />
        
        {preview && (
          <div style={{ marginBottom: '16px', textAlign: 'center' }}>
            <img src={preview} alt="Aperçu" style={{ maxHeight: '180px', borderRadius: '8px', border: '1px solid #e2e8f0' }} />
          </div>
        )}

        <button 
          type="submit" 
          disabled={status.loading}
          style={{ 
            width: '100%', 
            padding: '12px', 
            borderRadius: '6px', 
            border: 'none', 
            background: status.loading ? '#94a3b8' : '#2563eb', 
            color: '#fff', 
            fontWeight: '600',
            cursor: status.loading ? 'not-allowed' : 'pointer',
            transition: 'background 0.2s'
          }}
        >
          {status.loading ? 'Traitement en cours...' : 'Envoyer pour décodage'}
        </button>
      </form>

      {status.error && (
        <div style={{ padding: '12px 16px', borderRadius: '8px', background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', marginBottom: '16px' }}>
          <strong>Échec :</strong> {status.error}
        </div>
      )}

      {status.data && (
        <div style={{ 
          padding: '16px', 
          borderRadius: '8px', 
          background: status.data.status === 'ok' ? '#f0fdf4' : '#fffbeb', 
          border: `1px solid ${status.data.status === 'ok' ? '#bbf7d0' : '#fef08a'}`
        }}>
          <h4 style={{ margin: '0 0 8px 0', color: status.data.status === 'ok' ? '#166534' : '#854d0e' }}>
            {status.data.status === 'ok' ? '✅ QR Code Détecté !' : '⚠️ Attention'}
          </h4>
          {status.data.message && <p style={{ margin: '0 0 8px 0', fontSize: '14px' }}>{status.data.message}</p>}
          {status.data.data && (
            <div style={{ background: '#fff', padding: '10px', borderRadius: '6px', border: '1px solid #e2e8f0', fontFamily: 'monospace' }}>
              <strong>Données lues :</strong> {status.data.data}
            </div>
          )}
          <details style={{ marginTop: '12px', fontSize: '12px', color: '#64748b' }}>
            <summary style={{ cursor: 'pointer' }}>Voir la réponse brute JSON</summary>
            <pre style={{ background: '#f8fafc', padding: '10px', borderRadius: '6px', overflowX: 'auto' }}>
              {JSON.stringify(status.data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}