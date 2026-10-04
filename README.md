# Prisma AI

Generate beautiful AI images from natural language prompts. Built with a React frontend, a Django API, PostgreSQL, and seamless integrations with **Pollinations AI** and **Hugging Face Inference Providers**.

Built to the specification in `prisma_ai_prd.pdf`.

---

## What it does

Write a prompt, pick a size and quality, and generate. Your image is saved to your private history, and can be downloaded with a meaningful filename or regenerated later.

- Prompt input with live validation and a built-in prompt-writing guide
- Three sizes (1024×1024, 1024×1536, 1536×1024) and two quality tiers
- Paginated private history with preview, download, regenerate, and delete
- Account sign-up and sign-in; every image is scoped to its owner
- Dark and light themes, full keyboard access, reduced-motion support

---

## Stack

| Layer | Choice |
|---|---|
| Frontend | React 19, JavaScript, Vite, Tailwind CSS v4, React Router |
| Backend | Django 6, Django REST Framework, SimpleJWT |
| Database | PostgreSQL |
| AI Providers | Pollinations AI (Free/Default), Hugging Face, Stub (Offline Fallback) |
| Storage | Filesystem behind a swappable interface |

---

## Local Setup

**Requires** Python 3.12+, Node 20+, PostgreSQL 14+.

### 1. Database

```bash
createdb prisma_ai
```

### 2. Backend

```bash
cd backend
python3 -m venv .venv
# Activate the virtual environment
.venv/bin/pip install -r requirements-dev.txt

cp .env.example .env
```

Edit your new `backend/.env` file:

```ini
DJANGO_SECRET_KEY=<your_random_secret_string>
DATABASE_URL=postgres://YOUR_POSTGRES_USER:YOUR_PASSWORD@localhost:5432/prisma_ai
# Choose your provider: pollinations, huggingface, or stub
IMAGE_PROVIDER=pollinations
```

Run the backend:
```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```
The API is now running on `http://localhost:8000`.

### 3. Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`.

---

## AI Image Providers

Prisma AI was designed with a highly modular architecture that lets you hot-swap image providers instantly.

1. **Pollinations AI (`pollinations`)**: The default provider. Fully free, no API keys or accounts required, instantly generates FLUX model images.
2. **Hugging Face (`huggingface`)**: Requires an account. You must add `HF_TOKEN=hf_your_token` to your `.env` file.
3. **Stub (`stub`)**: An offline fallback that generates static gradients. Perfect for UI testing on airplanes!

To change providers, simply edit `IMAGE_PROVIDER=` in your `backend/.env` file and restart the Django server.

---

## Security

- `HF_TOKEN` (if used) is read from the environment, used only server-side, and never leaks.
- CORS is explicitly allowlisted, never wildcarded.
- JWT Refresh cookies are `httpOnly`, `Secure`, path-scoped, and aggressively rotated.
- `Origin` headers are validated on every cookie-authenticated endpoint.
- All image queries are strictly scoped to the requesting `request.user`.

---

## Design System

See `docs/DESIGN_SYSTEM.md` for tokens, components, the nine interaction states, layout, responsive behaviour, and accessibility guidelines.
