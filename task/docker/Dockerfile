FROM arm64v8/python:3.9-alpine
MAINTAINER PIYUSH YADAV "piyush.yadav@live.in"
COPY . /app
WORKDIR /app
EXPOSE 5000
ENV SERVE_PORT=5000
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]