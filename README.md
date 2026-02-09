# 🏭 WILD ERP v3 — Gamybos valdymo sistema

Kubilų ir pirčių gamybos valdymo sistema su interaktyvia skaičiuokle, daugiakalbiu interfeisu ir PDF generavimu.

![Version](https://img.shields.io/badge/version-3.0-blue)
![Languages](https://img.shields.io/badge/languages-LT%20EN%20DE%20RU%20FR%20IT-green)

## ✨ Funkcionalumas

| Modulis | Aprašymas |
|---------|-----------|
| **Pagrindinis** | Dashboard su statistika ir greiti veiksmai |
| **Žaliavos** | Pilnas CRUD, paieška, filtravimas pagal kategorijas |
| **Kubilai** | 22 modeliai (ST/AK/PP) su kainomis ir maržomis |
| **Pirtys** | 7 modeliai × 9 ilgiai (2-6m) su savikainomis |
| **Skaičiuoklė** | Interaktyvus konfigūratorius su realaus laiko kainomis |
| **Užsakymai** | Užsakymų valdymas su statusais |
| **Gamyba** | Gamybos eigos stebėjimas |
| **PDF** | Komercinis pasiūlymas + Gamybos lapas |
| **Kalbos** | LT, EN, DE, RU, FR, IT |

## 🚀 Greitas startas

### Variantas 1: Tik frontend (GitHub Pages)

1. Forkinkite šį repository
2. Settings → Pages → Source: `main` branch
3. Atidarykite: `https://jusu-username.github.io/wild-erp/`

### Variantas 2: Su backend (Render.com)

```bash
# 1. Klonuokite
git clone https://github.com/jusu-username/wild-erp.git
cd wild-erp

# 2. Sukurkite virtualią aplinką
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instaliuokite
pip install -r requirements.txt

# 4. Paleiskite
python app.py
```

Atsidarykite `http://localhost:5000`

## 📁 Failų struktūra

```
wild-erp/
├── index.html            # Frontend (React + viskas viename faile)
├── app.py                # Flask REST API backend
├── database_schema.sql   # SQLite schema
├── requirements.txt      # Python dependencies
├── render.yaml           # Render.com deploy config
├── .gitignore
└── README.md
```

## 🔧 Technologijos

- **Frontend:** React 18, JSX (Babel), CSS, jsPDF
- **Backend:** Python Flask, SQLite
- **Deploy:** GitHub Pages / Render.com
- **Duomenys:** localStorage (offline) + REST API (online)

## 📊 Produktų modeliai

### Kubilai (22 modeliai)
- **ST** — Stiklo pluošto (7 modeliai: apvalūs, kvadratiniai, Ofuro, šaltas)
- **AK** — Akriliniai (6 modeliai: apvalūs, kvadratiniai, Ofuro)
- **PP** — Polipropileno (9 modeliai: apvalūs, kvadratiniai, šaltas)

### Pirtys (7 modeliai × 9 ilgių)
- Apvali eglė / termo
- Igloo eglė / termo
- Kvadratinė eglė / termo
- Moderni

## 🌍 Deploy į Render.com

1. Push'inkite į GitHub
2. [render.com](https://render.com) → New Web Service → Connect repo
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`
5. Deploy! ✅

## 📋 API Endpoints

```
GET    /api/materials          # Visos žaliavos
POST   /api/materials          # Nauja žaliava
PUT    /api/materials/:id      # Atnaujinti
DELETE /api/materials/:id      # Ištrinti
GET    /api/orders             # Visi užsakymai
POST   /api/orders             # Naujas užsakymas
GET    /api/stats              # Statistika
GET    /api/health             # Health check
```

## 📄 Licencija

Private — WILD Production
