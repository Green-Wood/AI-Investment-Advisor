FROM python:alpine
WORKDIR /usr/app

COPY ./requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
COPY ./ ./

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]