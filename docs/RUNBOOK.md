# LABBAIK AI v6.0 - Operations Runbook

## 📋 Table of Contents

1. [Quick Reference](#quick-reference)
2. [Deployment Procedures](#deployment-procedures)
3. [Monitoring & Alerts](#monitoring--alerts)
4. [Incident Response](#incident-response)
5. [Database Operations](#database-operations)
6. [Scaling Procedures](#scaling-procedures)
7. [Backup & Recovery](#backup--recovery)
8. [Security Procedures](#security-procedures)

---

## 🚀 Quick Reference

### Important URLs

| Environment | URL | Purpose |
|-------------|-----|---------|
| Production | https://labbaik.cloud | Main application |
| Staging | https://staging.labbaik.cloud | Testing |
| Admin | https://labbaik.cloud/admin | Admin panel |
| API Docs | https://labbaik.cloud/docs | API documentation |

### Key Contacts

| Role | Contact |
|------|---------|
| Lead Developer | dev@labbaik.cloud |
| DevOps | ops@labbaik.cloud |
| Support | support@labbaik.cloud |

### Common Commands

```bash
# Check application status
docker-compose ps

# View logs
docker-compose logs -f app

# Restart application
docker-compose restart app

# Deploy new version
git pull && docker-compose up -d --build

# Run database migrations
python scripts/migrate.py migrate

# Check migration status
python scripts/migrate.py status
```

---

## 🚀 Deployment Procedures

### Standard Deployment (Streamlit Cloud)

1. **Merge to main branch**
   ```bash
   git checkout main
   git merge develop
   git push origin main
   ```

2. **Verify deployment**
   - Check Streamlit Cloud dashboard
   - Wait for auto-deploy (2-5 minutes)
   - Verify application at https://labbaik.cloud

3. **Rollback if needed**
   ```bash
   git revert HEAD
   git push origin main
   ```

### Docker Deployment

1. **Build new image**
   ```bash
   docker build -t labbaik-ai:latest .
   ```

2. **Test locally**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   curl http://localhost:8501/health
   ```

3. **Push to registry**
   ```bash
   docker tag labbaik-ai:latest ghcr.io/labbaik/labbaik-ai:latest
   docker push ghcr.io/labbaik/labbaik-ai:latest
   ```

4. **Deploy to production**
   ```bash
   ssh production
   docker-compose pull
   docker-compose up -d
   ```

### Database Migration

1. **Check current status**
   ```bash
   python scripts/migrate.py status
   ```

2. **Backup database**
   ```bash
   pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
   ```

3. **Run migrations**
   ```bash
   python scripts/migrate.py migrate
   ```

4. **Verify**
   ```bash
   python scripts/migrate.py status
   ```

---

## 📊 Monitoring & Alerts

### Health Checks

**Application Health:**
```bash
curl https://labbaik.cloud/health
```

Expected response: `{"status": "healthy", "version": "6.0.0"}`

**Database Health:**
```bash
python -c "from services.database import get_db; print(get_db().is_connected)"
```

### Key Metrics to Monitor

| Metric | Threshold | Action |
|--------|-----------|--------|
| Response Time | > 3s | Scale up / optimize |
| Error Rate | > 1% | Investigate errors |
| CPU Usage | > 80% | Scale horizontally |
| Memory Usage | > 85% | Check for leaks |
| Database Connections | > 80 | Increase pool size |

### Log Locations

| Component | Location |
|-----------|----------|
| Application | `/var/log/labbaik/app.log` |
| Nginx | `/var/log/nginx/access.log` |
| PostgreSQL | `/var/log/postgresql/` |

### Log Analysis Commands

```bash
# Recent errors
grep -i error /var/log/labbaik/app.log | tail -50

# Slow queries
grep "duration:" /var/log/postgresql/*.log | awk '$NF > 1000'

# User activity
grep "user_login" /var/log/labbaik/app.log | wc -l
```

---

## 🚨 Incident Response

### Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P1 | Service down | 15 minutes |
| P2 | Major feature broken | 1 hour |
| P3 | Minor issue | 4 hours |
| P4 | Low priority | Next business day |

### P1 Response Procedure

1. **Acknowledge incident** (within 5 min)
2. **Initial assessment**
   ```bash
   docker-compose ps
   docker-compose logs --tail=100 app
   curl -v https://labbaik.cloud/health
   ```
3. **Notify stakeholders**
4. **Begin mitigation**
5. **Update status page**
6. **Post-incident review**

### Common Issues & Solutions

#### Application Not Responding

```bash
# Check if container is running
docker-compose ps

# Restart application
docker-compose restart app

# Check resources
docker stats

# View detailed logs
docker-compose logs -f --tail=200 app
```

#### Database Connection Issues

```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check connection pool
docker-compose logs app | grep -i connection

# Restart with fresh connections
docker-compose restart app
```

#### High Memory Usage

```bash
# Check memory
docker stats

# Clear caches
docker-compose exec app python -c "import gc; gc.collect()"

# Restart if needed
docker-compose restart app
```

#### SSL Certificate Issues

```bash
# Check certificate
openssl s_client -connect labbaik.cloud:443 -servername labbaik.cloud

# Renew certificate (Let's Encrypt)
certbot renew
systemctl restart nginx
```

---

## 🗄️ Database Operations

### Connection Information

```bash
# Production
DATABASE_URL=postgresql://user:pass@host:5432/labbaik_prod

# Staging
DATABASE_URL=postgresql://user:pass@host:5432/labbaik_staging
```

### Routine Maintenance

**Weekly:**
```bash
# Vacuum analyze
psql $DATABASE_URL -c "VACUUM ANALYZE;"

# Check table sizes
psql $DATABASE_URL -c "SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) 
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;"
```

**Monthly:**
```bash
# Full vacuum
psql $DATABASE_URL -c "VACUUM FULL VERBOSE;"

# Reindex
psql $DATABASE_URL -c "REINDEX DATABASE labbaik_prod;"
```

### Backup Procedures

**Daily Automated Backup:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL | gzip > /backups/labbaik_$DATE.sql.gz

# Keep only last 30 days
find /backups -name "labbaik_*.sql.gz" -mtime +30 -delete
```

**Manual Backup Before Major Changes:**
```bash
pg_dump $DATABASE_URL > backup_before_migration_$(date +%Y%m%d).sql
```

### Restore Procedure

```bash
# Restore from backup
psql $DATABASE_URL < backup_file.sql

# Verify data integrity
python scripts/migrate.py status
```

---

## 📈 Scaling Procedures

### Horizontal Scaling

1. **Increase replica count**
   ```yaml
   # docker-compose.prod.yml
   services:
     app:
       deploy:
         replicas: 3
   ```

2. **Apply changes**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale app=3
   ```

3. **Verify load balancing**
   ```bash
   for i in {1..10}; do curl -s https://labbaik.cloud/health | jq .hostname; done
   ```

### Vertical Scaling

1. **Update resource limits**
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

2. **Apply and restart**
   ```bash
   docker-compose up -d
   ```

### Database Scaling

**Increase connection pool:**
```python
# core/config.py
database:
  pool_size: 20  # Increase from 5
  max_overflow: 40  # Increase from 10
```

**Add read replicas:**
- Configure in Neon dashboard
- Update connection strings

---

## 💾 Backup & Recovery

### Backup Schedule

| Data | Frequency | Retention |
|------|-----------|-----------|
| Database | Daily | 30 days |
| Database | Weekly | 12 weeks |
| Database | Monthly | 12 months |
| Application logs | Daily | 7 days |
| Configuration | On change | Indefinite (Git) |

### Recovery Procedures

**Full System Recovery:**

1. Provision new infrastructure
2. Restore database from backup
3. Deploy latest application version
4. Verify functionality
5. Update DNS if needed

**Database Recovery:**

```bash
# Stop application
docker-compose stop app

# Restore database
psql $DATABASE_URL < latest_backup.sql

# Run migrations (if needed)
python scripts/migrate.py migrate

# Restart application
docker-compose start app
```

---

## 🔒 Security Procedures

### Regular Security Tasks

**Daily:**
- Review access logs for anomalies
- Check failed login attempts

**Weekly:**
- Review user access patterns
- Check for dependency vulnerabilities

**Monthly:**
- Rotate API keys
- Review and update access controls
- Security audit

### Credential Rotation

```bash
# Generate new JWT secret
python -c "import secrets; print(secrets.token_hex(32))"

# Update in environment
export JWT_SECRET_KEY="new_secret_here"

# Restart application
docker-compose restart app
```

### Security Incident Response

1. **Identify scope**
2. **Contain threat**
   - Disable compromised accounts
   - Block suspicious IPs
3. **Eradicate**
   - Rotate affected credentials
   - Patch vulnerabilities
4. **Recover**
   - Restore from clean backup if needed
5. **Document and review**

### Audit Log Review

```bash
# View recent audit logs
psql $DATABASE_URL -c "SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 100;"

# Check for suspicious activity
psql $DATABASE_URL -c "SELECT user_id, action, COUNT(*) FROM audit_logs 
WHERE created_at > NOW() - INTERVAL '24 hours' 
GROUP BY user_id, action 
ORDER BY COUNT(*) DESC;"
```

---

## 📞 Escalation Matrix

| Issue Type | First Contact | Escalation |
|------------|---------------|------------|
| Application | DevOps Team | Lead Developer |
| Database | DevOps Team | Database Admin |
| Security | Security Team | CTO |
| Business | Support Team | Product Manager |

---

## 📝 Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-01-XX | Initial runbook creation | LABBAIK Team |

---

*Last updated: January 2025*
*Version: 6.0.0*
