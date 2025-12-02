# Local RAG Application.
A mini RAG Application to query Documents and Database locally.
```
Local RAG Application
├─ backend
│  ├─ api
│  │  ├─ model.py
│  │  ├─ routes.py
│  │  └─ __init__.py
│  ├─ config.py
│  ├─ core
│  │  ├─ graph.py
│  │  ├─ rag_system.py
│  │  ├─ state.py
│  │  └─ __init__.py
│  ├─ data
│  │  ├─ chroma_db
│  │  ├─ database.db
│  │  └─ documents
│  │     ├─ FastAPI For AI.pdf
│  │     └─ Moaaz_Soliman_CV.pdf
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ services
│  │  ├─ document_services.py
│  │  ├─ llm_service.py
│  │  ├─ sql_services.py
│  │  ├─ vectorstore_service.py
│  │  └─ __init__.py
│  ├─ tests
│  │  ├─ test_model.py
│  │  ├─ test_rag.py
│  │  └─ test_services.py
│  ├─ utils
│  │  ├─ helpers.py
│  │  ├─ logger.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ data
│  ├─ chroma_db
│  └─ documents
│     └─ Moaaz_Soliman_CV.pdf
├─ docker
│  └─ docker-compose.yaml
├─ frontend
│  ├─ eslint.config.js
│  ├─ index.html
│  ├─ package.json
│  ├─ public
│  │  └─ vite.svg
│  ├─ README.md
│  ├─ src
│  │  ├─ App.jsx
│  │  ├─ assets
│  │  │  └─ react.svg
│  │  ├─ components
│  │  ├─ index.css
│  │  ├─ main.jsx
│  │  ├─ services
│  │  └─ utils
│  └─ vite.config.js
├─ LICENSE
└─ README.md

```