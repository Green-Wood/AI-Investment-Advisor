FROM python:3.7.4


WORKDIR /usr/app

COPY ./requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY ./ ./

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]