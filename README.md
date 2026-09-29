# Scrappy
This is a simple demo application for scrapping data from telegraph channels and storing it in a database. It uses the Ollama framework for model serving and can be run in a Conda environment.

## Example of .env file

```bash
API_ID='your_api_id'
API_HASH='your_api_hash'
MY_SENDER_ID='your_sender_id'
PHONE_NUMBER='your_phone_number'
```

## Conda Environment

```bash
conda activate [your_env_name]
```

## Use Model GPU

Run in terminal:

```bash
sudo systemctl edit ollama.service
```

Add this line under `[Service]` section:

```ini
[Service]
Environment="CUDA_VISIBLE_DEVICES=0"
```

Save changes:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Check:

```bash
ollama ps
```