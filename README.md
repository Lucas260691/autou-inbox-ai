<h1>📧 Classificador e Resposta Automática de Emails</h1>

<h2>🚀 Sobre o Projeto</h2>
<p>
Aplicação web fullstack para <strong>classificação automática de emails</strong> (Produtivo/Improdutivo) e <strong>sugestão de respostas rápidas</strong>.
</p>
<ul>
  <li><strong>Backend:</strong> FastAPI + NLP/ML + integração opcional com LLM (OpenAI).</li>
  <li><strong>Frontend:</strong> React + Vite + TailwindCSS, com interface moderna e responsiva.</li>
  <li><strong>Infra:</strong> Docker e Docker Compose para rodar tudo integrado.</li>
</ul>

<hr />

<h2>🎯 Objetivo</h2>
<p>Auxiliar equipes de suporte e atendimento a:</p>
<ol>
  <li><strong>Filtrar rapidamente emails</strong> que exigem ação.</li>
  <li><strong>Responder automaticamente</strong> mensagens comuns.</li>
</ol>

<hr />

<h2>🖥️ Funcionalidades</h2>

<h3>Frontend</h3>
<ul>
  <li>Área para <strong>colar texto de emails</strong>.</li>
  <li><strong>Upload arrasta-e-solta</strong> de arquivos <code>.txt</code> e <code>.pdf</code>.</li>
  <li>Exemplos rápidos prontos para testar.</li>
  <li>Exibição clara do resultado:
    <ul>
      <li>Categoria atribuída (Produtivo/Improdutivo).</li>
      <li>Grau de confiança.</li>
      <li>Intenções detectadas (status, suporte, cobrança, anexos).</li>
      <li>Resposta sugerida com botão <strong>Copiar texto</strong>.</li>
    </ul>
  </li>
  <li>Interface com <strong>modo claro/escuro</strong>.</li>
  <li>Feedback visual de carregamento.</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Pipeline híbrido: regras heurísticas + modelo baseline (Logistic Regression + TF-IDF).</li>
  <li>Detecção de intenções.</li>
  <li>Geração de respostas em português ou inglês.</li>
  <li>Upload seguro e leitura de PDFs (<code>pypdf</code>).</li>
  <li>Integração com <strong>OpenAI GPT</strong> opcional.</li>
</ul>

<hr />

<h2>🛠️ Tecnologias</h2>
<ul>
  <li><strong>Frontend:</strong> React, Vite, TailwindCSS, React Hook Form, Zod</li>
  <li><strong>Backend:</strong> Python 3.12, FastAPI, Scikit-learn, Joblib, PyPDF</li>
  <li><strong>Infra:</strong> Docker, Docker Compose</li>
  <li><strong>IA avançada (opcional):</strong> OpenAI GPT</li>
</ul>

<hr />

<h2>⚙️ Instalação</h2>

<h3>1. Pré-requisitos</h3>
<ul>
  <li><a href="https://www.docker.com/">Docker</a></li>
  <li><a href="https://docs.docker.com/compose/">Docker Compose</a></li>
</ul>

<h3>2. Clonar o repositório</h3>
<pre><code>git clone https://github.com/seu-usuario/projeto-email-ia.git
cd projeto-email-ia
</code></pre>

<h3>3. Configurar variáveis de ambiente</h3>
<p>Crie um <code>.env</code> baseado em <code>.env.openApi</code>:</p>
<pre><code>AI_PROVIDER=openai      # ou "none" para usar só o baseline
OPENAI_API_KEY=seu_token_aqui
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=*
</code></pre>

<h3>4. Subir os containers</h3>
<pre><code>docker-compose up --build
</code></pre>

<h3>5. Acessar os serviços</h3>
<ul>
  <li><strong>Frontend:</strong> <a href="http://localhost:5173">http://localhost:5173</a></li>
  <li><strong>Backend (Swagger):</strong> <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
</ul>

<hr />

<h2>📂 Estrutura</h2>
<pre><code>📦 projeto-email-ia
├── backend/
│   ├── app/...
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .dockerignore
│   └── .env.openApi
│
├── frontend/
│   ├── src/components/...
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
</code></pre>

<hr />

<h2>📦 docker-compose.yml</h2>
<pre><code>version: "3.9"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: email-backend
    env_file:
      - ./backend/.env.openApi
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: email-frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
</code></pre>

<hr />

<h2>📦 Rodando o Backend Manualmente</h2>
<p>Se preferir rodar sem Docker:</p>
<pre><code>cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
</code></pre>

<hr />

<h2>📌 Melhorias Futuras</h2>
<ul>
  <li>Expandir dataset para treinar o baseline.</li>
  <li>Suporte multilíngue além de PT/EN.</li>
  <li>Persistência em banco de dados (histórico).</li>
  <li>Autenticação de usuários.</li>
  <li>Dashboard estatístico no frontend.</li>
</ul>

<hr />

<h2>👨‍💻 Autor</h2>
<p>Projeto desenvolvido por <strong>Lucas Meinen</strong> ✨</p>
