FROM python:3.7
COPY . /app
WORKDIR /app
ENV FLASK_ENV production
ENV FLASK_APP devopshero.py
RUN pip install -r requirements.txt
RUN flask db init && flask db migrate && flask db upgrade
EXPOSE 80
ENTRYPOINT ["flask", "run"]
CMD ["--host", "0.0.0.0", "--port", "80"]