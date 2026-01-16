# core/scorer.py

class Scorer:
    def __init__(self):
        # Foco: Exposição de dados, infraestrutura crítica e painéis de controle
        self.high_value_keywords = {
            # Ambientes e Versões (Onde o erro humano é maior)
            "dev": 25, "staging": 20, "stg": 20, "test": 15, "sandbox": 20, 
            "beta": 10, "lab": 15, "v1": 5, "v2": 5, "old": 15, "legacy": 20,
            
            # Infraestrutura e Cloud
            "aws": 20, "s3": 25, "bucket": 30, "azure": 20, "cloud": 15, 
            "storage": 20, "minio": 25, "kubernetes": 25, "k8s": 25, "docker": 15,
            "vault": 35, "consul": 25, "etcd": 30, "terraform": 25,

            # Acesso e Identidade (Alvos de Ouro)
            "vpn": 30, "okta": 25, "auth": 20, "login": 15, "sso": 20,
            "admin": 25, "portal": 20, "dashboard": 20, "manager": 15,
            "root": 30, "secure": 10, "identity": 15,

            # Desenvolvimento e Código
            "git": 25, "gitlab": 25, "bitbucket": 20, "svn": 20, "repo": 20,
            "ci": 20, "cd": 20, "build": 15, "jenkins": 35, "confluence": 25,
            "jira": 20, "sonar": 25, "artifact": 20,

            # Dados e Monitoramento
            "db": 25, "database": 30, "sql": 25, "redis": 20, "mongodb": 25,
            "elastic": 20, "kibana": 20, "grafana": 25, "prometheus": 20,
            "splunk": 20, "log": 20, "logging": 20, "metabase": 25,

            # Redes e Arquivos
            "internal": 25, "intranet": 25, "private": 25, "corp": 20,
            "backup": 35, "archive": 25, "conf": 25, "config": 30, "ftp": 25,
            "smtp": 15, "api-docs": 20, "swagger": 25
        }
        
        # Foco: Tecnologias com histórico de RCE (Remote Code Execution) e vulnerabilidades críticas
        self.critical_techs = {
            # CI/CD e Gestão
            "Jenkins": 35, "TeamCity": 30, "GitLab": 25, "Bamboo": 25,
            "GoCD": 30, "Drone": 20,

            # Servidores de Aplicação e Middleware
            "JBoss": 30, "WebLogic": 35, "WebSphere": 35, "Apache NiFi": 35,
            "ColdFusion": 35, "WildFly": 25, "Tomcat": 20,

            # Bancos de Dados e Big Data
            "phpMyAdmin": 35, "Adminer": 30, "Elasticsearch": 25, "Redis": 25,
            "Cassandra": 25, "Hadoop": 30, "Spark": 25, "CouchDB": 25,

            # CMS e E-commerce (Alvos fáceis de exploração)
            "WordPress": 15, "Drupal": 20, "Magento": 25, "Joomla": 20,
            "Ghost": 15, "vBulletin": 30,

            # Monitoramento e Dashboards
            "Grafana": 25, "Kibana": 25, "Zabbix": 30, "Nagios": 25,
            "Airflow": 30, "Jupyter": 35, "RStudio": 30,

            # Dev Frameworks (Interessante para análise de bugs lógicos)
            "Laravel": 15, "Django": 10, "Ruby on Rails": 15, "Spring Boot": 20,
            "Express": 10, "Flask": 10,

            # Diversos
            "Fortinet": 30, "Citrix": 35, "F5 Big-IP": 35, "Pulse Secure": 35,
            "Roundcube": 25, "Microsoft Exchange": 35
        }

        
    def calculate_score(self, asset):
        """Calcula o Attack Interest Score e armazena os motivos."""
        score = 10.0  # Pontuação base para qualquer ativo encontrado
        reasons = []

        # 1. Análise de Keywords no Domínio
        for word, points in self.high_value_keywords.items():
            if word in asset.domain.lower():
                score += points
                reasons.append(f"Keyword '{word}' detected in domain")

        # 2. Análise de Tecnologias
        for tech in asset.technologies:
            for crit_tech, points in self.critical_techs.items():
                if crit_tech.lower() in tech.lower():
                    score += points
                    reasons.append(f"Critical technology '{crit_tech}' detected")

        # 3. Análise de Status Code
        if asset.status_code == 403:
            score += 15
            reasons.append("Forbidden (403) may indicate protected interesting content")
        elif asset.status_code == 401:
            score += 20
            reasons.append("Unauthorized (401) indicates an authentication barrier")

        # Limitar o score a 100
        asset.attack_interest_score = min(score, 100)
        asset.score_reasons = reasons
        return asset