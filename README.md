name: Actualizar VERING Mundial 2026

on:
  schedule:
    # Cada dia a las 10:00 AM hora Paraguay (UTC-4 = 14:00 UTC)
    - cron: '0 14 * * *'
  workflow_dispatch: # También permite ejecutar manualmente

jobs:
  update-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repositorio
        uses: actions/checkout@v3

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Generar HTML actualizado
        run: python3 build.py

      - name: Desplegar a Netlify
        env:
          NETLIFY_TOKEN: ${{ secrets.NETLIFY_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        run: |
          npm install -g netlify-cli
          netlify deploy --prod --dir=./dist --auth=$NETLIFY_TOKEN --site=$NETLIFY_SITE_ID
