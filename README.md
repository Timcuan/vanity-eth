# Vanity-ETH

[![Build Status](https://flat.badgen.net/github/checks/bokub/vanity-eth?label=build)](https://github.com/bokub/vanity-eth/actions/workflows/deploy.yml?query=branch%3Amaster)
[![License](https://flat.badgen.net/badge/license/MIT/cyan)](https://raw.githubusercontent.com/bokub/vanity-eth/master/LICENSE)
[![Code style](https://flat.badgen.net/badge/code%20style/prettier/ff69b4)](https://github.com/bokub/prettier-config)
[![Maintainability](https://flat.badgen.net/codeclimate/maintainability/bokub/vanity-eth)](https://codeclimate.com/github/bokub/vanity-eth/maintainability)

Browser-based ETH vanity address generator

Just type [`vanity-eth.tk`](https://vanity-eth.tk) to use it ⚡️

[![Vanity-ETH](https://i.imgur.com/zmSLeBP.png)](https://vanity-eth.tk)

## What's a vanity address?

A vanity address is an address in which you can choose a part of it to make it appear less random.

Examples:

-   `0xc0ffee254729296a45a3885639AC7E10F9d54979`
-   `0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E`

## Usage

First of all, visit [`vanity-eth.tk`](https://vanity-eth.tk)

Enter a short prefix and/or suffix of your choice and click _Generate_ to start. Your browser will
generate lots of random addresses until it finds one that matches your input.

Once an address is found, you can choose to reveal the private key or click the _Save_ button to download a password-encrypted keystore file.

Adjusting the number of working threads can increase or decrease the speed, depending on your computer's capabilities.

## Security

As mentioned earlier, all computations occur solely within your browser. Nothing ever leaves your machine, or even your browser tab.
There is no database, no server-side code. Everything vanishes when you close your browser tab.

**Vanity-ETH cannot and will never store your private key.** If you have concerns about its trustworthiness, you have three options to ensure the privacy of your key:

-   After loading the web page, you can disconnect from the internet and continue using it seamlessly
-   Alternatively, you can download the latest build of Vanity-ETH [here](https://git.io/veth-dl)
    and use it on an offline computer
-   The code is 100% open source and available on GitHub, allowing you to review it thoroughly before usage.

Vanity-ETH uses a cryptographically secure pseudorandom number generator (CSPRNG) to generate Ethereum addresses.

The keystore file is encrypted with an AES-128-CTR cipher using the PBKDF2-SHA256 derivation function with 65536 hashing rounds.

## Other browser-based tools

Be aware that due to its popularity and open-source nature, Vanity-ETH has been widely copied, leading to the existence of websites claiming to provide the same functionality. Sometimes, they are perfect clones hosted on very similar domains.

Most of them do not credit the original code, are not open-source, and may contain malicious code.

Vanity-ETH has always been the **first** browser-based ETH vanity address generator, and remains the most popular and trusted one.

To be sure you're on the real Vanity-ETH website, search for [Vanity-ETH on GitHub](https://github.com/search?o=desc&q=Vanity-ETH&s=stars), find the repository with the most stars (> 600), and click the link in the description. Double check by searching [Vanity-ETH on Google](https://www.google.com/search?q=Vanity-ETH).

## Performance

Vanity-ETH's performance may vary significantly across different browsers. Currently, Chrome provides the best results.

While you can use Vanity-ETH on your phone or tablet, it is unlikely to match the speed of a traditional computer.

**N.B:** Vanity-ETH is designed to be a user-friendly tool that runs directly in your browser, providing easy accessibility without the need to download or install additional software.
However, browser-based tools have inherent limitations that may affect their performance and efficiency. Some dedicated command-line tools are more difficult to use, but may offer better performance.

## Compatibility

Any address generated with Vanity-ETH is ERC-20 compatible, which means you can use it for an ICO, an airdrop, or just
to withdraw your funds from an exchange.

The keystore file is 100% compatible with MyEtherWallet, MetaMask, Mist, and geth.

## Build Vanity-ETH from source

A GitHub Action is in charge of building and deploying Vanity-ETH to GitHub pages automatically 🤖, but you can make
your own build from source if you want (you will need Node.js 16)

```sh
git clone https://github.com/bokub/vanity-eth
cd vanity-eth
npm i
npm run build
```

## Tips

You can support this project by sending tips to `0xAceBabe64807cb045505b268ef253D8fC2FeF5Bc` 💛

# Telegram Vanity ETH Wallet Bot

Bot ini memungkinkan Anda membuat dompet Ethereum (ETH) dengan alamat *vanity* (alamat yang diawali dengan prefiks tertentu) langsung dari Telegram.

## Fitur

1. Perintah `/generate <prefiks>` untuk menghasilkan dompet ETH baru dengan alamat yang dimulai dengan `0x<prefiks>`.
2. Validasi prefiks (karakter heksadesimal, panjang ≤ 6 direkomendasikan).
3. Proses pencarian dilakukan secara paralel di thread pool untuk performa yang lebih baik.
4. Kunci privat dan alamat dikirim kembali dalam obrolan Telegram setelah ditemukan.

> ⚠️ **PERINGATAN**: Kunci privat ditampilkan dalam obrolan Telegram. Pastikan Anda hanya menggunakan obrolan pribadi (bukan grup) dan simpan kunci privat Anda dengan aman.

## Persyaratan

- Python 3.9+
- Token bot Telegram (dapat dibuat via [@BotFather](https://t.me/BotFather))

## Instalasi

1. Clone repositori / salin kode ini ke server Anda.
2. Buat lingkungan virtual (opsional namun disarankan)

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instal dependensi

```bash
pip install -r requirements.txt
```

4. Buat berkas `.env` pada root proyek dan tambahkan token bot Telegram Anda:

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

## Menjalankan Bot

```bash
python bot.py
```

Bot akan mulai melakukan *polling* dan siap menerima perintah di Telegram.

## Cara Penggunaan

1. Mulai bot dengan mengirim `/start`.
2. Buat dompet vanity dengan memanggil:

```text
/generate abc
```

Bot akan mencari alamat yang dimulai dengan `0xabc` dan mengembalikan *address* serta *private key* ketika ditemukan.

Semakin panjang prefiks, semakin lama waktu pencarian; prefiks 6 karakter bisa memakan beberapa menit tergantung performa CPU.

---
### Lisensi

MIT License
