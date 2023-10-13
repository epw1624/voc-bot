# voc-bot
Discord bot for the VOC server

# Instructions for deployment

Ensure that Docker is installed on the target device. You can install docker at: https://docs.docker.com/get-docker/<br>

1. Clone the repository
```
$ git clone git@gitlab.com:voc/voc-bot.git
$ cd voc-bot/src
```

2. Install the project requirements
```
$ cd src
$ pip install -r requirements.txt
```

2. Create a credentials.py file with the following values
```
BASE_URL="http://ubc-voc.com/api/verify.php"
SECRET_KEY=""
API_KEY=""
```
Fill in SECRET_KEY with the secret key for the Discord bot, and API_KEY with the API key for ubc-voc.com

3. Build the docker container
```
docker build -t container-name .
```

4. Run the docker container
```
docker run -d --name container-name voc-bot
```
