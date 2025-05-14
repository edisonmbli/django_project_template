# Pull base image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
# 确保 pip 是最新的
RUN pip install --upgrade pip
# 安装项目依赖
RUN pip uninstall -y marshmallow environs || true && \
    pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Copy project
COPY . .

# 安全性提升：添加非 root 用户
RUN adduser --disabled-password --no-create-home appuser
USER appuser