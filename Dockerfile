# Usa uma imagem oficial e enxuta do Python como base.
FROM python:3.13-slim

# Define /app como diretório de trabalho dentro da imagem.
WORKDIR /app

# Copia primeiro o arquivo que contém as dependências Python.
COPY requirements.txt .

# Instala as dependências declaradas em requirements.txt.
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copia a pasta app para o diretório /app da imagem.
COPY app/ .

# Documenta que a aplicação Flask utiliza a porta 5000.
EXPOSE 5000

# Define o comando executado quando o container web iniciar.
CMD ["python", "app.py"]
