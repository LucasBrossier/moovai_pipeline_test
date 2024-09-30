# Utilise une image officielle Python comme image de base
FROM python:3.9-slim

# Définit des variables d'environnement pour Airflow
ENV AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW_VERSION=2.7.2
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.9.txt"


# Installe les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && apt-get clean

# Crée le répertoire Airflow
RUN mkdir -p $AIRFLOW_HOME
RUN mkdir -p $AIRFLOW_HOME/dags/
# Installe Airflow
RUN pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Copie les fichiers locaux de configuration (optionnel si vous avez des fichiers de config)
# COPY ./airflow.cfg $AIRFLOW_HOME/airflow.cfg

# Définit le répertoire de travail
WORKDIR $AIRFLOW_HOME

# Expose le port du serveur web Airflow
EXPOSE 8080

COPY *.py ${AIRFLOW_HOME}/dags/.
COPY requirements.txt ${AIRFLOW_HOME}/dags/.
COPY /modeling/. ${AIRFLOW_HOME}/modeling/.
#COPY 0* /${AIRFLOW_HOME}/.


RUN cd dags/ && pip install -r requirements.txt
# Initialise la base de données d'Airflow
RUN airflow db init

# Crée un utilisateur administrateur (remplacer par vos informations)
RUN airflow users create \
    --username admin \
    --firstname Admin \
    --lastname Admin \
    --role Admin \
    --email admin@example.com \
    --password admin


# Commande d'entrée pour démarrer Airflow (Scheduler et Webserver)
CMD ["bash", "-c", "airflow scheduler & airflow webserver --port 8080"]