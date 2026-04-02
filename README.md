# Celestia Codex – Uputstvo za pokretanje

## Preduslovi

- **Docker** (za pokretanje MySQL baze)
- **Node.js** (v20 ili noviji)
- **Python** (v3.8+)
- **Git** (opciono)

---

## 1. Pokretanje MySQL baze podataka

Baza se pokreće unutar Docker kontejnera komandom:

```bash
docker run --name mysql-celestia -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=celestia_codex -p 3306:3306 -v mysql-data:/var/lib/mysql -d mysql:latest
```

**Objašnjenje:**  
- `--name mysql-celestia` – ime kontejnera  
- `-e MYSQL_ROOT_PASSWORD=1234` – lozinka za root korisnika  
- `-e MYSQL_DATABASE=celestia_codex` – inicijalna baza  
- `-p 3306:3306` – mapiranje porta  
- `-v mysql-data:/var/lib/mysql` – trajno skladištenje podataka  
- `-d mysql:latest` – pokretanje u pozadini

> ⚠️ Ako već postoji kontejner sa istim imenom, on se mora prvo ukloniti: `docker rm -f mysql-celestia`

Kada je baza pokrenuta, potrebno je kreirati tabele. Kreiranje izvršiti pomoću SQL skripte (`celestia_codex.sql`) koja se nalazi u repozitorijumu:

```bash
docker exec -i mysql-celestia mysql -uroot -p1234 celestia_codex < celestia_codex.sql
```

---

## 2. Pokretanje backend servera (Node.js)

### 2.1 Instalacija zavisnosti

U glavnom folderu backend aplikacije (gde se nalazi `package.json`):

```bash
npm install
```

### 2.2 Konfiguracija (`.env` fajl)

Primer `.env` fajla:

```env
# DB DEV
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=1234
DB_NAME=celestia_codex

# EXPRESS CONFIG
PORT=4000

# JWT TOKEN
JWT_SECRET=neki_tajni_kljuc_za_jwt

# SALT FOR PASSWORD
SALT_ROUNDS=10
```

### 2.3 Pokretanje servera

```bash
npm run dev   # razvojni režim (nodemon)
# ili
npm start     # produkcijski režim
```

Server će se pokrenuti na `http://localhost:4000`.  
Endpoint-i su dostupni na `http://localhost:4000/api/v1/...`

---

## 3. API tester (Python alat)

Alat omogućava interaktivno testiranje svih API ruta.

### 3.1 Postavljanje virtuelnog okruženja

U folderu gde se nalazi `api-tester.py`:

```bash
python3 -m venv venv
```

**Aktivacija:**  
- Windows (PowerShell): `.\venv\Scripts\Activate.ps1`  
- Linux/macOS: `source venv/bin/activate`

### 3.2 Instalacija paketa

```bash
pip install flask requests
```

### 3.3 Pokretanje testera

```bash
python api-tester.py
```

U URL adresi u browser-u otići na `http://localhost:5000`.  
Na ovoj stranici možete:
- postaviti JWT token (ili se prijaviti preko built‑in forme)
- odabrati bilo koji API endpoint
- popuniti parametre (path, query, body)
- poslati zahtev i videti odgovor
---

## 4. Dodatne informacije

- **Podrazumevani test korisnik** – nakon prvog pokretanja, preporučuje se registracija korisnika preko testera ili `POST /api/v1/auth/register`.  
- **Admin nalog** – potrebno je ručno postaviti ulogu `admin` u bazi (npr. `UPDATE users SET role='admin' WHERE id=1;`).  
- **Logovi** – sve akcije se beleže u tabeli `audits`.  
- **Validacija** – svi ulazi se validiraju i na serveru i na klijentu.

---

## Česta pitanja

**1. Kako resetovati bazu?**  
`docker rm -f mysql-celestia` zatim ponovo pokrenuti kontejner i SQL skriptu.

**2. Gde se nalaze slike heroja?**  
Čuvaju se kao base64 string u koloni `image` tabele `characters`.

**3. Koje su podrazumevane uloge?**  
`player` i `admin`. Admin ima pristup svim rutama za upravljanje.

---
