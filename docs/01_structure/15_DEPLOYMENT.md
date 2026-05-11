# DEPLOYMENT.md

# Estrategia de despliegue

Documento de referencia para ejecutar Aula Robótica Platform en distintos entornos.

---

# Entornos previstos

## Local Development

Uso diario durante desarrollo.

## Staging

Pruebas previas a producción.

## Production

Entorno real para usuarios finales.

---

# Requisitos mínimos

- Python 3.12+
- uv o pip
- MariaDB
- Git

---

# Instalación local

## Clonar repositorio

```bash
git clone https://github.com/fran-eliot/aula-robotica-platform
cd aula-robotica-platform
```

## Crear entorno

```bash
uv sync
```

## Variables de entono

Crear .env
```text
SECRET_KEY=change_me
DATABASE_URL=mysql+pymysql://user:pass@localhost/db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```
## Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

---

# Producción recomendada

## Arquitectura

```text
Internet
   │
   ▼
Nginx
   │
   ▼
Uvicorn / FastAPI
   │
   ▼
MariaDB
```

---

## Nginx Recomendado
### Funciones
* **Reverse proxy**
* **HTTPS**
* **Static files**
* **Security headers**
* **Gzip**

### HTTPS

Usar: 
* **Let's Encrypt**
* **Certbot**

---

## Ejecución y Despliegue
### Ejecución con Gunicorn/Uvicorn
```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4
```

### Docker futuro
`docker-compose.yml` previsto.
**Servicios:**
* `app`
* `db`
* `nginx`

---

## Variables sensibles
**Nunca subir:**
* `SECRET_KEY`
* `DATABASE_URL` real
* Tokens
* Credenciales admin

*Nota: Usar siempre archivo `.env`.*

---

## Seguridad en producción
### Recomendado
* **Secure cookies**: HttpOnly, SameSite
* **HTTPS obligatorio**
* **Firewall**: Fail2ban
* **Logs monitorizados**

---

## Backups
### Base de datos
**Backup diario:**
```bash
mysqldump db > backup.sql
```

### Estrategia
* Diarios
* Semanales
* Rotación
* Almacenamiento externo

---

## Logging
### Recomendado
* Access logs
* Error logs
* Audit logs
* Alertas

---

## Monitorización futura
* Uptime checks
* CPU / RAM
* Errores 500
* Tiempos respuesta

---

## CI/CD futuro
**Pipeline ideal (GitHub Actions):**
1. **Tests**
2. **Lint**
3. **Build**
4. **Deploy staging**
5. **Deploy production**

---

## Escalabilidad futura
Si aumenta uso:
* **Redis cache**
* **Workers background**
* **PostgreSQL**
* **Contenedores**
* **Kubernetes**

---

## Checklist producción
- [ ] `DEBUG=False`
- [ ] HTTPS activo
- [ ] Secret key segura
- [ ] Backups activos
- [ ] Logs revisados
- [ ] Cookies seguras
- [ ] Firewall
- [ ] Monitoring






