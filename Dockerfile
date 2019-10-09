FROM python:3.7
COPY . /app
WORKDIR /app
ENV SLACK_SIGNING_SECRET <UPDATE THIS WITH YOUR SECRET FROM SLACK>
ENV LOGLEVEL DEBUG
ENV FLASK_ENV development
ENV FLASK_APP src/app.py
RUN pip install -r requirements.txt
RUN flask db init && flask db migrate && flask db upgrade
EXPOSE 80
ENTRYPOINT ["flask", "run"]
CMD ["--host", "0.0.0.0", "--port", "80"]