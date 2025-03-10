# Alap image
FROM python:3.9

# Munka könyvtár
WORKDIR /app

# Másoljuk a kódot
COPY . .

# Függőségek telepítése
RUN pip install -r requirements.txt

# Alkalmazás indítása
CMD ["python", "main.py"]
