# Scrappy

## Conda Environment

```bash
conda activate traitor-env
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