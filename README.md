# KupujemProdajem Ad Notifier

A Python script that monitors new classified ads on kupujemprodajem website with custom filters and **sends an email notification** when a new ad appears.

## 🔍 Use Case

Stay on top of new listings without refreshing the page — perfect for finding great deals.

## 📦 Features

- Scrapes filtered search results on KupujemProdajem
- Detects new ads in real-time
- Sends email alerts with the ad title and link
- Avoids duplicate alerts using in-memory cache
- Easy to configure via `.env` file (no hardcoding credentials)
