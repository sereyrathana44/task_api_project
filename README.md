# Task API — Web APIs & Cloud Deployment (ក្រុមទី ៦)

គម្រោងគំរូនេះបង្ហាញពីការបង្កើត REST API ជាមួយ **Django REST Framework (DRF)**
និងការត្រៀមរៀបចំវាឱ្យដំណើរការជាសាធារណៈលើ **Cloud (Render)** ដោយប្រើ
**PostgreSQL** និង **Gunicorn**។

---

## 1. Server-Rendered HTML vs. API-Centric Backend

| | Server-Rendered HTML (Django Templates) | API-Centric Backend (DRF) |
|---|---|---|
| លទ្ធផលចេញពី Server | ឯកសារ HTML ពេញលេញ ត្រៀមបង្ហាញ | ទិន្នន័យសុទ្ធ ជាទម្រង់ **JSON** |
| អ្នកប្រើប្រាស់ | Browser ទាញ HTML រួចបង្ហាញភ្លាម | Frontend ណាមួយក៏បាន (React, Vue, Mobile App, Postman...) ទាញ JSON ទៅដំណើរការ និង render ដោយខ្លួនឯង |
| ភាពបត់បែន | ភ្ជាប់ជាមួយ Django templates តែប៉ុណ្ណោះ | Frontend/Backend ដាច់ពីគ្នាទាំងស្រុង (decoupled) — client ណាមួយក៏ហៅប្រើបាន |
| ឧទាហរណ៍ក្នុងគម្រោងនេះ | `render(request, 'template.html', context)` | `TaskSerializer` + `TaskViewSet` → `JsonResponse` |

នៅក្នុងគម្រោងនេះ យើងបង្កើតជា **API-Centric Backend**៖ រាល់ endpoint សុទ្ធតែឆ្លើយតបជា JSON
ដើម្បីឱ្យ Client ណាមួយ (Postman, mobile app, React frontend ។ល។) អាចហៅប្រើបាន។

---

## 2. រចនាសម្ព័ន្ធគម្រោង (Project Structure)

```
task_api_project/
├── manage.py
├── requirements.txt          # Python dependencies
├── Procfile                  # command ដែល Heroku/Render ប្រើដើម្បីចាប់ផ្តើម app
├── build.sh                  # script ដំណើរការនៅពេល Render build app
├── render.yaml                # Infrastructure-as-code សម្រាប់ deploy លើ Render ស្វ័យប្រវត្តិ
├── .env.example               # គំរូ Environment Variables (កុំដាក់ .env ពិតចូល Git)
├── postman_collection.json    # Import ចូល Postman ដើម្បីតេស្ត API ភ្លាមៗ
├── task_api/                  # Django project settings
│   ├── settings.py            # DEBUG, ALLOWED_HOSTS, WhiteNoise, DATABASE_URL ។ល។
│   ├── urls.py
│   └── wsgi.py                # ចំណុចចូលសម្រាប់ Gunicorn
└── tasks/                     # Django app មួយ (Task management)
    ├── models.py               # Task model
    ├── serializers.py          # Model -> JSON (និងច្រាសមកវិញ)
    ├── views.py                # ModelViewSet -> CRUD endpoints ស្វ័យប្រវត្តិ
    ├── urls.py                 # DRF Router
    ├── admin.py
    ├── tests.py                 # Sample automated tests
    └── migrations/0001_initial.py
```

---

## 3. ការដំណើរការនៅលើ Local Machine (VS Code)

```bash
# 1) បង្កើត virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 2) ដំឡើង dependencies
pip install -r requirements.txt

# 3) ចម្លងឯកសារ environment variables
cp .env.example .env           # Windows: copy .env.example .env

# 4) បង្កើត database tables
python manage.py migrate

# 5) បង្កើត admin user (ស្រេចចិត្ត តែចាំបាច់សម្រាប់ការ Create/Update/Delete តាមរយៈ API)
python manage.py createsuperuser

# 6) ដំណើរការ server
python manage.py runserver
```

Server នឹងដំណើរការនៅ **http://127.0.0.1:8000/**

- `GET /` → ទំព័រដើម HTML ស្អាតៗ បង្ហាញ links ទៅកាន់ endpoints ទាំងអស់ (សម្រាប់មនុស្សមើល)
- `GET /health/` → JSON health check សុទ្ធ (សម្រាប់ Postman ឬ script)
- `GET /api/tasks/` → មើលបញ្ជី tasks (មិនចាំបាច់ login)
- `POST/PUT/PATCH/DELETE /api/tasks/` → ត្រូវការ login (session auth តាមរយៈ `/api-auth/login/`)
- `GET /admin/` → Django Admin panel

> **ចំណាំ**៖ ទំព័រដើម (`/`) គ្រាន់តែជា landing page ស្អាតៗសម្រាប់មនុស្សមើលប៉ុណ្ណោះ — API ពិតប្រាកដ
> (ដែលឆ្លើយតបជា JSON) នៅតែស្ថិតនៅ `/api/tasks/`, `/health/` ។ល។ នេះមិនផ្លាស់ប្តូរលក្ខណៈ
> API-Centric Backend របស់គម្រោងនេះទេ — គ្រាន់តែបន្ថែមផ្ទាំងស្វាគមន៍ស្អាតៗម្តងប៉ុណ្ណោះ។

### ដំណើរការ Sample Tests

```bash
python manage.py test
```

---

## 4. ត្រៀមរៀបចំសម្រាប់ Production (Checklist)

ចំណុចទាំងនេះត្រូវបានរៀបចំរួចរាល់ក្នុង `task_api/settings.py`៖

- ✅ **`DEBUG=False`** នៅ production (កំណត់តាមរយៈ Environment Variable `DEBUG`)
- ✅ **`SECRET_KEY`** ទាញពី Environment Variable មិនតម្កល់ក្នុង source code ទេ
- ✅ **`ALLOWED_HOSTS`** កំណត់ច្បាស់លាស់ តាមរយៈ Environment Variable
- ✅ **Static files** គ្រប់គ្រងដោយ **WhiteNoise** (`whitenoise.middleware.WhiteNoiseMiddleware` +
  `CompressedManifestStaticFilesStorage`) — មិនចាំបាច់ dependency លើ Nginx ដើម្បីបម្រើ static files
- ✅ **Database**: local ប្រើ SQLite ស្វ័យប្រវត្តិ, production ប្រើ **PostgreSQL** តាមរយៈ `DATABASE_URL`
  (`dj_database_url`)
- ✅ **HTTPS/Security headers** (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`)
  បើកស្វ័យប្រវត្តិនៅពេល `DEBUG=False`

---

## 5. ការ Deploy លើ Render (Step-by-Step)

> Render ត្រូវបានជ្រើសរើសព្រោះមាន Free tier សម្រាប់ទាំង Web Service និង PostgreSQL database។
> ជំហានស្រដៀងគ្នាទាំងស្រុងសម្រាប់ Heroku (ជំនួស `render.yaml` ដោយ `Procfile` ដែលមានស្រាប់ក្នុងគម្រោង)។

### ជំហានទី ១ — ដាក់ Code ឡើង GitHub
```bash
git init
git add .
git commit -m "Initial commit: Task API with DRF"
git branch -M main
git remote add origin https://github.com/<your-username>/task-api.git
git push -u origin main
```

### ជំហានទី ២ — បង្កើត PostgreSQL Database នៅលើ Render
1. ចូល [render.com](https://render.com) → **New +** → **PostgreSQL**
2. ដាក់ឈ្មោះ (ឧ. `task-api-db`) → ជ្រើសរើស Free plan → **Create Database**
3. ចម្លង **Internal Database URL** ទុក (នឹងត្រូវការនៅជំហានបន្ទាប់)

### ជំហានទី ៣ — បង្កើត Web Service
1. **New +** → **Web Service** → ភ្ជាប់ទៅ GitHub repository ខាងលើ
2. កំណត់៖
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn task_api.wsgi:application`
3. បន្ថែម **Environment Variables** (Settings → Environment):

   | Key | Value |
   |---|---|
   | `SECRET_KEY` | (ចុច "Generate" ឬដាក់ string ដោយខ្លួនឯង) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `.onrender.com` |
   | `DATABASE_URL` | (ចម្លងពី PostgreSQL database ខាងលើ) |
   | `PYTHON_VERSION` | `3.12.4` |

4. ចុច **Create Web Service** — Render នឹង `pip install`, `collectstatic`, `migrate` និង
   ចាប់ផ្តើម Gunicorn ស្វ័យប្រវត្តិ (មើល `build.sh` និង `Procfile`)។

> **ជម្រើសរហ័ស**៖ បើ repository មាន `render.yaml` (មានរួចហើយក្នុងគម្រោងនេះ) អ្នកអាចប្រើ
> Render's "Blueprint" feature (**New + → Blueprint**) ដើម្បី provision ទាំង database
> និង web service ក្នុងចលនាតែមួយ ដោយស្វ័យប្រវត្តិ។

### ជំហានទី ៤ — ផ្ទៀងផ្ទាត់
បើកតំណភ្ជាប់ដែល Render ផ្តល់ឱ្យ (ឧទាហរណ៍ `https://task-api-xxxx.onrender.com/`)
គួរឃើញលទ្ធផល health-check JSON ដូចនៅក្នុង `task_api/urls.py`។

Deploy លើ **Heroku** ឬ **AWS Elastic Beanstalk** អនុវត្តតាមគោលការណ៍ដូចគ្នា៖
env vars → PostgreSQL add-on → `Procfile`/`Dockerfile` → `gunicorn task_api.wsgi`។

---

## 6. ការតេស្ត API ជាមួយ Postman

1. បើក Postman → **Import** → ជ្រើសរើសឯកសារ `postman_collection.json` ក្នុងគម្រោងនេះ
2. កែប្រែ Collection Variable `base_url` ទៅជា URL ដែល deploy រួច
   (ឧ. `https://task-api-xxxx.onrender.com`) ឬទុកជា `http://127.0.0.1:8000` សម្រាប់ local
3. Requests ដែលមានស្រាប់ក្នុង collection៖

   | Request | Method | Endpoint | ត្រូវការ Login? |
   |---|---|---|---|
   | Health Check | GET | `/` | ទេ |
   | List Tasks | GET | `/api/tasks/` | ទេ |
   | Filter by Priority | GET | `/api/tasks/?priority=HIGH` | ទេ |
   | Search Tasks | GET | `/api/tasks/?search=deploy` | ទេ |
   | Retrieve Single Task | GET | `/api/tasks/{id}/` | ទេ |
   | Create Task | POST | `/api/tasks/` | បាទ/ចាស |
   | Update Task (Partial) | PATCH | `/api/tasks/{id}/` | បាទ/ចាស |
   | Delete Task | DELETE | `/api/tasks/{id}/` | បាទ/ចាស |

4. សម្រាប់ requests ដែលត្រូវការ login (POST/PATCH/DELETE)៖ Session Authentication ត្រូវការ
   ចូល browser ទៅ `{{base_url}}/api-auth/login/` ជាមុនសិន រួច Postman នឹងទាញយក session cookie
   ស្វ័យប្រវត្តិ (បើកម៉ឺនុយ Postman Interceptor ឬប្រើ Postman Cookie sync)។ ជម្រើសសាមញ្ញជាងសម្រាប់
   Postman សុទ្ធ គឺប្រើ **Basic Auth** tab ក្នុង Postman ដោយដាក់ username/password របស់
   superuser ដែលបានបង្កើតតាមរយៈ `createsuperuser`។

---

## 7. ចំណុចអាចបន្ថែម (Extensions)

- ប្តូរពី Session/Basic Auth ទៅជា **Token Authentication** ឬ **JWT** (`djangorestframework-simplejwt`)
  សម្រាប់ mobile/SPA clients
- បន្ថែម `drf-spectacular` ដើម្បីបង្កើត Swagger/OpenAPI documentation ស្វ័យប្រវត្តិ
- ភ្ជាប់ **Docker** (`Dockerfile` + `docker-compose.yml`) សម្រាប់ deploy លើ AWS ECS/EC2
