---
name: Project Development Guidelines
description: Skills, technologies, and guidelines needed to develop the Cinema Invite App
---

# Project Development Guidelines

This skill provides a **project summary**, **technologies**, and **practices** used in the Cinema Invite App. Use it when developing or modifying features so that choices stay consistent with the codebase.

---

## Project Summary

**Cinema Invite App** is a full-stack web application that lets users create and manage **movie invitations**—e.g. inviting friends to see a specific movie. Main capabilities:

- **Authentication**: Email/password login and **Google SSO** (OAuth2), JWT-based sessions.
- **Users**: Profiles; current user is available via React context and backend `get_current_user`.
- **Movies**: Movie catalog (title, description, release date, genre, director, actors); used when creating invitations.
- **Invitations**: User-created posts linking a **user**, a **movie**, optional text, image URLs, cinema IDs, status, and “amount of reach.”
- **Feed**: Home feed of content; sidebar; post-creation popup.
- **Search**: Search page (protected route).
- **Deployment**: Backend can serve the built frontend (SPA fallback for `/`, `/search`, `/login`, `/profile`).

**Repository layout**: Backend lives in `backend/`, frontend in `frontend-2/` (the previous `frontend` folder was removed). Docker Compose runs MySQL and the FastAPI backend; the frontend is typically run with `npm start` in development.

---

## Tech Stack Overview

### 1. Backend
- **Language**: Python 3.x
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database Migrations**: Alembic
- **Database**: MySQL (PyMySQL driver; optional aiosqlite in requirements)
- **Auth**: JWT (python-jose), password hashing (passlib/bcrypt), **Google SSO** (fastapi-sso)
- **Notable patterns**:
  - Pydantic schemas for request/response validation.
  - Dependency injection `get_db()` for DB sessions.
  - `get_current_user` for protected routes.
  - Use **Alembic** for all schema changes: `alembic revision --autogenerate` and `alembic upgrade head`. Do **not** rely on `Base.metadata.create_all` for schema updates.

### 2. Frontend
- **Library**: React 18
- **UI**: React Bootstrap, custom CSS
- **Routing**: React Router DOM v6
- **HTTP**: Axios (wrapped in `context/api.js` and invitation API module)
- **Auth**: AuthContext (login, logout, token and user in localStorage), ProtectedRoute for private pages
- **Build**: Create React App (`react-scripts`)

### 3. Infrastructure
- **Containers**: Docker and Docker Compose
- **Services**: `mysql` (port 3306), `backend` (port 8000), backend depends on MySQL health.
- **Static frontend**: Backend mounts and serves the built frontend from a path such as `../frontend/build/` (update to `../frontend-2/build/` if building from `frontend-2`).

---

## Skills Needed to Develop the Project

When working on this codebase, you should be comfortable with (or learn) the following:

### Backend
- **Python 3**: Type hints, async/await where used, module layout.
- **FastAPI**: Routers, dependencies, CORS, static files, `FileResponse` for SPA fallback.
- **SQLAlchemy**: Models, relationships, sessions, MySQL-specific considerations (e.g. no native ARRAY; use TEXT and parse).
- **Alembic**: Writing and applying migrations; never changing schema only via `create_all`.
- **Pydantic**: Request/response schemas, validation.
- **Auth**: JWT creation/validation, OAuth2 (e.g. Google SSO), password hashing, secure token storage and refresh flows.
- **API design**: REST-like endpoints under `/api/v1`, consistent error handling and status codes.

### Frontend
- **React 18**: Hooks (useState, useEffect, useContext), function components.
- **React Router v6**: `Routes`, `Route`, nested routes, `ProtectedRoute` pattern.
- **React Bootstrap**: Layout and form components; custom CSS where needed.
- **State**: Context (e.g. AuthContext, API client), localStorage for token/user cache.
- **HTTP**: Axios instances with base URL and auth headers; handling 401 and redirect to login.

### Data & DB
- **MySQL**: Basic administration, connection strings, PyMySQL.
- **Modeling**: Users, movies, invitations; foreign keys and relationships; parsing stored strings (e.g. semicolon-separated) into arrays in app code.

### DevOps & Tooling
- **Docker**: Dockerfile for backend, Docker Compose for multi-service setup.
- **Environment**: `.env` for secrets (e.g. `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `REDIRECT_URI`, DB credentials); not committing secrets.

### Conventions
- **Backend**: Routers in `app/api/`, models in `app/models/`, CRUD in `app/crud/`, schemas in `app/schemas/`, utilities in `app/utils/`.
- **Frontend**: Pages in `pages/`, reusable UI in `components/`, popups in `popups/`, API and auth in `context/` and `api/`.
- **Styling**: Prefer React Bootstrap; add custom CSS files next to components when needed.

---

## Development Rules

1. **Database schema**: Always use Alembic migrations. Do not use `Base.metadata.create_all` for ongoing schema changes.
2. **Frontend styling**: Use React Bootstrap first; add custom CSS only when necessary.
3. **Running the app**:
   - **Backend + MySQL**: `docker-compose up` from repo root.
   - **Frontend**: `cd frontend-2 && npm start` (dev server; proxy to backend if configured).
   - **Production build**: Build frontend (`npm run build` in `frontend-2`); ensure backend serves from the correct build path (e.g. `../frontend-2/build` if applicable).

---

## Quick Reference

| Area        | Choice / Location                                      |
|------------|---------------------------------------------------------|
| API prefix | `/api/v1`                                               |
| Auth       | JWT + Google SSO; `get_current_user`, AuthContext       |
| DB         | MySQL; Alembic for migrations                           |
| Frontend   | `frontend-2/` (React 18, React Bootstrap, React Router) |
| Backend    | `backend/` (FastAPI, SQLAlchemy, Pydantic)              |
