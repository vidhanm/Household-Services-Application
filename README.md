# Household Services Platform 🚀

Hey! 👋 This is a full-stack web app for booking household services, built by a 21-year-old who loves code, coffee, and making life easier. You can be a customer, a pro, or an admin—everyone gets their own dashboard. It's got cool features, a modern UI, and is super easy to run locally. Read on!

---

## What Can You Do Here?
- Sign up as a customer or professional (pros upload docs, get admin approval)
- Book services, see your history, give feedback
- Admins can approve pros, manage users/services, and see analytics
- OTP password reset (email + Redis magic)
- Real-time slot holding so no double-booking
- All with JWT auth and a Vue + Vuetify frontend

---

## Tech Stack (aka, what makes this tick)
- **Backend:** Flask, Flask-RESTful, JWT, SQLAlchemy, Redis, Celery
- **Frontend:** Vue 3, Vuetify, Vue Router, Axios, Chart.js
- **DB:** SQLite (easy mode, swap if you want)

---

## Project Structure
```
Project/
  Backend/
    app.py, config.py, models.py, ...
    resources/   # All the API stuff
    utils/       # OTP, Redis, etc
    uploads/     # Pro docs
  frontend/
    src/
      App.vue, components/, router/
    package.json, vite.config.mjs
```

---

## Getting Started (dev mode)
### Backend
```bash
cd Backend
pip install -r requirements.txt
python init_db.py  # sets up DB + admin user
python app.py      # runs on http://localhost:5000/
```
- Edit `config.py` and `config/mail_config.py` for your secrets, DB, email, Redis, etc.

### Frontend
```bash
cd frontend
npm install  # or yarn
npm run dev  # runs on http://localhost:3000/
```

---

## Database & Migrations
- Uses SQLite by default (file: `Backend/instance/MAD2.sqlite3`)
- Alembic migrations in `Backend/migrations/`
- Run `python init_db.py` to set up tables and admin

---

## Main Features (TL;DR)
- **Customers:** Book services, see history, leave feedback
- **Pros:** Register, upload docs, get approved, accept/reject jobs
- **Admins:** Approve pros, manage everything, see stats, export data
- **Auth:** JWT, role-based, OTP reset
- **Booking:** Real-time slot holding (Redis)
- **UI:** Modern, responsive, and not ugly 😎

---

## API Endpoints (Quick Peek)
- `/register`, `/login`, `/logout`, `/refresh`, `/reset-password`, `/forgot-password`
- `/api/customer/service-requests`, `/customer/services/search`, `/api/customer/ongoing-services`, `/api/customer/completed-services`
- `/professional/dashboard`
- `/admin/dashboard`, `/admin/users`, `/admin/services`, `/admin/professionals/pending`, etc.

---

## Pro Tips
- For production, use Gunicorn (backend) and build the frontend (`npm run build`)
- Set your secrets/env vars for JWT, DB, Redis, and mail
- Want to swap DB? Change the URI in `config.py`


