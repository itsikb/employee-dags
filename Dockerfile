FROM 668139184987.dkr.ecr.us-east-1.amazonaws.com/microcosm-airflow-1-onbuild


#add more packages on base image
COPY requirements.txt .
RUN pip install --no-cache-dir -q -r requirements.txt 
