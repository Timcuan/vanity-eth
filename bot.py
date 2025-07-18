import os
import re
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from eth_account import Account
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables from a .env file (if present)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Please set the BOT_TOKEN environment variable in a .env file or system environment.")

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ThreadPoolExecutor for CPU-bound vanity generation tasks
executor = ThreadPoolExecutor(max_workers=os.cpu_count() or 4)

HEX_PATTERN = re.compile(r"^[0-9a-fA-F]+$")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and brief instruction."""
    await update.message.reply_text(
        "👋 Halo! Kirim /generate <prefiks_heksadesimal> untuk membuat dompet Ethereum 
vanity.\n\n"
        "Contoh: /generate abc\n"
        "Catatan: Prefiks tidak termasuk '0x' dan sebaiknya maksimal 6 karakter untuk proses cepat."
    )


def generate_wallet(prefix: str) -> tuple[str, str]:
    """Brute force search for an Ethereum address that starts with the given hex prefix.

    Returns tuple (address, private_key_hex).
    """
    prefix = prefix.lower()
    target = "0x" + prefix
    attempts = 0
    while True:
        acct = Account.create()
        address = acct.address.lower()
        attempts += 1
        if address.startswith(target):
            return address, acct.key.hex()
        # Optionally log progress every million attempts.
        if attempts % 1_000_000 == 0:
            logger.info("Tried %d keys for prefix %s", attempts, prefix)


async def _async_generate(prefix: str) -> tuple[str, str]:
    """Run the CPU bound generate_wallet in a thread pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, generate_wallet, prefix)


async def generate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /generate command."""

    if not context.args:
        await update.message.reply_text("Silakan sertakan prefiks hex. Contoh: /generate abc")
        return

    prefix = context.args[0]

    # Validate prefix
    if not HEX_PATTERN.fullmatch(prefix):
        await update.message.reply_text("Prefiks harus berupa karakter heksadesimal (0-9, a-f).")
        return

    if len(prefix) > 6:
        await update.message.reply_text("Prefiks terlalu panjang (maks 6 karakter disarankan).")
        return

    await update.message.reply_text(
        f"⏳ Sedang mencari alamat yang dimulai dengan 0x{prefix} ... Mohon tunggu."
    )

    try:
        address, priv_key = await _async_generate(prefix)
    except Exception as exc:
        logger.exception("Error generating wallet: %s", exc)
        await update.message.reply_text("Terjadi kesalahan saat membuat dompet. Coba lagi nanti.")
        return

    # Send result (beware of privacy)
    await update.message.reply_text(
        f"✅ Ditemukan!\n\n"
        f"Address: `{address}`\n"
        f"Private Key: `{priv_key}`\n\n"
        "SIMPAN private key ini dengan aman. Siapapun yang memiliki kunci ini dapat mengakses dana Anda.",
        parse_mode="Markdown",
    )


async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to unknown commands."""
    await update.message.reply_text("Perintah tidak dikenali. Gunakan /generate untuk membuat dompet baru.")


def main() -> None:
    """Run the Telegram bot."""

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_handler))

    # Unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

    # Start the bot
    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()