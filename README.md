# 🍪 Cookie Clicker Bot (Selenium + undetected\_chromedriver)

This project automates the popular [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/) game using **Selenium** and **undetected\_chromedriver**. The bot clicks the cookie, checks for upgrades, and buys them when enough cookies are available.

-----

## 🚀 Features

  * Automatically clicks the big cookie
  * Buys upgrades/products when affordable
  * Bypasses Cloudflare challenge using `undetected_chromedriver`
  * Simulates human-like random sleep and scrolling
  * Logs key steps and warnings

-----

## 🧰 Requirements

  * Python 3.7+
  * Google Chrome installed
  * ChromeDriver (managed automatically by `undetected_chromedriver`)

-----

## 📦 Installation

1.  **Clone the repo**:

    ```bash
    git clone https://github.com/aakk23/cookieclicker-selenium.git
    cd cookieclicker-selenium
    ```

2.  **Install dependencies**:

    ```bash
    pip install undetected-chromedriver selenium
    ```

-----

## ▶️ Run the Bot

```bash
python cookie_clicker.py
```

The bot will open Chrome in non-headless mode, auto-select English, and start clicking + buying.

-----

## 📝 How It Works

  * Uses `undetected_chromedriver` to load the game page and bypass bot detection.
  * Waits for the language selection screen and picks English.
  * If a Cloudflare CAPTCHA appears, it waits until it's gone.
  * Starts clicking the cookie in a loop.
  * Checks prices of upgrades and buys the most affordable one available.

-----

## 📂 File Structure

```
cookieclicker-bot/
├── cookie_clicker.py       # Main automation script
└── README.md               # This file
```

-----

## 📋 Notes

  * The game takes a few seconds to load; the script includes proper wait conditions.
  * You can tweak product IDs or logic to prioritize better upgrades.
  * Be mindful of CPU usage if running the click loop for a long time.

-----

## 📄 License

MIT License – do whatever you want, but don't blame me if the cookie takes over your CPU. 🍪

-----

## 🙌 Acknowledgements

  * Selenium
  * `undetected_chromedriver`
  * Cookie Clicker