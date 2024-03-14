# 使用官方的 Python 运行时作为基础镜像
FROM python:3.8
LABEL authors="chenyin"

# 设置工作目录
WORKDIR /app

# 将项目中的 requirements.txt 复制到镜像中，并安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install djangorestframework==3.14.0
# 将整个项目复制到镜像中
COPY . /app/

# 暴露 Django 项目运行的端口
EXPOSE 8000

# 启动 Django 项目
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh","-c","scripts/run"]