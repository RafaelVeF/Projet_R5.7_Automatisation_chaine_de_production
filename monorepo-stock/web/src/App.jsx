import { useState } from 'react';
import './App.css';

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
    <div className="scan-card">
      <h2 className="scan-title">Gestion de Stocks</h2>
      <p className="scan-subtitle">
        Chaîne : IHM Web &rarr; Ambassadeur &rarr; Post-Traitement &rarr; Données lues
      </p>

      <form onSubmit={handleSubmit} className="scan-form">
        <input
          type="file"
          name="fileInput"
          accept="image/*"
          onChange={handleFileChange}
          required
          className="file-input"
        />

        {preview && (
          <div className="preview-container">
            <img src={preview} alt="Aperçu du scan" className="preview-img" />
          </div>
        )}

        <button
          type="submit"
          disabled={status.loading}
          className="btn-submit"
        >
          {status.loading ? 'Traitement en cours...' : 'Envoyer pour décodage'}
        </button>
      </form>

      {status.error && (
        <div className="alert-box alert-error">
          <strong>Échec :</strong> {status.error}
        </div>
      )}

      {status.data && (
        <div className={`alert-box ${status.data.status === 'ok' ? 'alert-success' : 'alert-error'}`}>
          <h4 style={{ margin: '0 0 6px 0' }}>
            {status.data.status === 'ok' ? ' Code Détecté avec succès' : 'Erreur de lecture'}
          </h4>
          <p style={{ margin: '0 0 6px 0' }}>{status.data.message}</p>
          {status.data.data && (
            <div className="result-badge">
              <strong>Valeur décodée :</strong> {status.data.data}
            </div>
          )}
          <details className="json-details">
            <summary>Voir la réponse brute JSON</summary>
            <pre className="json-box">
              {JSON.stringify(status.data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}