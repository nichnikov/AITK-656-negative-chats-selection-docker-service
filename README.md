# AITK-656-negative-chats-selection
Обернуть в Докер сервис по анализу чатов на негатив

Docker RUN:
sudo docker run --env HTTP_PROXY=http://proxy.dev.aservices.tech:8080 --env HTTPS_PROXY=http://proxy.dev.aservices.tech:8080 -v /home/nichnikov/my-repo/negative-chats-selection-docker-service/data:/app/data  negative-chats-selection
