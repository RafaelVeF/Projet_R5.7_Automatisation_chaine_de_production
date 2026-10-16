-- 1. Table des articles / stocks
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    code VARCHAR(64) UNIQUE NOT NULL,      -- Valeur scannée (ex: 'ART-001' ou EAN-13 '5901234123457')
    designation VARCHAR(150) NOT NULL,
    description TEXT,
    quantite INT NOT NULL DEFAULT 0 CHECK (quantite >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Historique des mouvements (traçabilité chaîne de prod)
CREATE TABLE IF NOT EXISTS mouvements_stock (
    id SERIAL PRIMARY KEY,
    article_id INT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    type_mouvement VARCHAR(10) NOT NULL CHECK (type_mouvement IN ('ENTREE', 'SORTIE')),
    quantite INT NOT NULL CHECK (quantite > 0),
    date_mouvement TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    remarque VARCHAR(255)
);

-- 3. Données de test initiales
INSERT INTO articles (code, designation, description, quantite) VALUES
    ('ART-001', 'Capteur de proximité inductif', 'Composant pour ligne d''assemblage', 25),
    ('ART-002', 'Vérin pneumatique double effet', 'Actionneur standard 50mm', 10),
    ('5901234123457', 'Moteur pas-à-pas NEMA 17', 'Moteur pour convoyeur motorisé', 8)
ON CONFLICT (code) DO NOTHING;