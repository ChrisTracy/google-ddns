# google-ddns
A simple Docker container to update Dynamic DNS in Google Domains

## Example ##
docker run -d --name google-ddns -e URL="example.domain.com" -e USER="ABcDEF12345" -e PASS="ZyxWVUT54321" -e WAIT="300" christracy/google-ddns

## Logs ##
docker exec -it google-ddns /bin/bash\
tail -f googledyndns.log
