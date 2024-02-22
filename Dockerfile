FROM python:3.8.10-slim
WORKDIR /facebook_scraping
COPY . /facebook_scraping

RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y wget gnupg



RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


RUN chmod +x chromedriver.exe
RUN pip install -r requirements.txt
CMD ["uvicorn", "scrap_data:app", "--host", "0.0.0.0", "--port", "8000"]


