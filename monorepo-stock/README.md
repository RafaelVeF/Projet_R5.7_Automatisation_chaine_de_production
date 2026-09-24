# Monorepo Stock

Architecture d'un monorepo pour une chaîne de production avec interface web, orchestration Python, traitement Python et accès données ASP.NET.

## Services

- Web : React + Nginx, exposé sur le port 8080
- Ambassadeur : orchestrateur FastAPI sur le port 8001
- Post-traitement : FastAPI de validation/décodage sur le port 8002
- Datawarehouse : ASP.NET + Redis + Postgres sur les ports 8081, 6379 et 5432

## Démarrage

```bash
docker compose up --build
```

L'interface est accessible sur http://localhost:8080

# Guide

Pour lancer l'Ambassadeur (Terminal 1) :

cd monorepo-stock/ambassadeur
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --port 8000 --reload

Pour lancer le Web (Terminal 2) :

cd monorepo-stock/web
npm install
npm run dev
