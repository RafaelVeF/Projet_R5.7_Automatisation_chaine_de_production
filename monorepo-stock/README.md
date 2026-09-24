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
