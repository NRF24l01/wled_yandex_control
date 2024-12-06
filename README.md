# Connect wled to yandex alice

## Requirements
- Docker
- board with wled
- Account on alexstar.ru
- System with static ip

## Deployment
### 1. Git clone
```bash
git clone https://github.com/NRF24l01/wled_yandex_control
cd wled_yandex_control
```

### 2. Create .env
You should include wled ip into .env file
```bash
echo "WLED_HOST=<ip>" >> .env
```

### 3. Run app
*Requires docker compose*
1. Build
```bash
docker compose build
```
2. Run for check
```bash
docker compose up
```
When you saw that unicorn started, press ctrl+c
3. Run container
```bash
docker compose run lights-controler
```
### 4. Chill
