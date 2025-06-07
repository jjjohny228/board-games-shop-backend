FROM python:3.11
# declare ports which container exposess
EXPOSE 8000

# create app directory to work in
WORKDIR /app

# copy project requirements
COPY requirements.txt ./

# install project requirements
RUN pip install -r requirements.txt

COPY . ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
