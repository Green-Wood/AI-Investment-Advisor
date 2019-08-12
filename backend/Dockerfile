#FROM python:3.7.4
#
#COPY ./requirements.txt ./
#RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
FROM greenw00d/investment-advisor-env:latest
WORKDIR /usr/app
COPY ./requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY ./ ./

CMD ["gunicorn", "-c", "gunicorn.py", "wsgi:app"]