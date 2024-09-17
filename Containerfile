FROM python:3.12-slim-bullseye
RUN pip install --no-cache-dir --upgrade pip
# installing torch CPU manually
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# the rest of dependencies

RUN mkdir -p /home/app

COPY requirements.txt /home/app/.
WORKDIR "/home/app/"
RUN pip install --no-cache-dir -r requirements.txt

COPY apiserver.py .
COPY model model

ENV HF_HOME="/home/app/model"
EXPOSE 5000  
CMD ["fastapi", "run", "apiserver.py", "--port", "5000"]
