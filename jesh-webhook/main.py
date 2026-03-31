"""
JESH NAS M15 — TradingView Webhook → Telegram Alert Server
Receives alerts from TradingView and forwards them to your Telegram DM.
Deploy on Railway. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as env vars.
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]
SECRET    = os.environ.get("WEBHOOK_SECRET", "")   # optional security token

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram(text: str):
    payload = {
        "chat_id":    CHAT_ID,
        "text":       text,
        "parse_mode": "HTML",
    }
    r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
    r.raise_for_status()
    log.info("Telegram message sent: %s", text[:60])


def format_signal(data: dict) -> str:
    """Build a clean Telegram message from TradingView alert payload."""
    alert = data.get("alert", "").upper()
    price = data.get("price", "")
    entry = data.get("entry", "")
    sl    = data.get("sl", "")
    tp1   = data.get("tp1", "")
    tp2   = data.get("tp2", "")
    tp3   = data.get("tp3", "")
    risk  = data.get("risk", "")
    qty   = data.get("qty", "")

    # ── LONG ──────────────────────────────────────────────────────────────────
    if "LONG" in alert:
        return (
            "🟢 <b>JESH LONG SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry or price}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R Target</b>    <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )

    # ── SHORT ─────────────────────────────────────────────────────────────────
    if "SHORT" in alert:
        return (
            "🔴 <b>JESH SHORT SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry or price}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R Target</b>    <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )

    # ── SESSION OPEN ──────────────────────────────────────────────────────────
    if "SESSION" in alert or "OPEN" in alert:
        return (
            "🔔 <b>JESH Session Open — 9:30 AM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Opening Range is now set.\n"
            "Watch for breakout signal until 11:30 AM NY.\n"
            "⏰ Lagos: 2:30 PM WAT (summer) · 3:30 PM WAT (winter)"
        )

    # ── FORCE CLOSE ───────────────────────────────────────────────────────────
    if "FORCE" in alert or "CLOSE" in alert:
        return (
            "⚠️ <b>JESH Force Close — 4:55 PM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Close any open NAS100 position NOW.\n"
            "No overnight positions allowed.\n"
            "⏰ Lagos: 10:55 PM WAT"
        )

    # ── FALLBACK — raw alert ──────────────────────────────────────────────────
    return f"📡 <b>JESH Alert</b>\n{json.dumps(data, indent=2)}"


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "JESH webhook server running ✅"}), 200


@app.route("/jesh", methods=["POST"])
def webhook():
    # Optional secret check
    if SECRET:
        token = request.headers.get("X-Secret", "") or request.args.get("secret", "")
        if token != SECRET:
            log.warning("Unauthorized webhook attempt")
            return jsonify({"error": "unauthorized"}), 401

    # Parse body — TradingView sends JSON
    try:
        data = request.get_json(force=True) or {}
    except Exception:
        data = {}

    if not data:
        # TradingView sometimes sends plain text — wrap it
        data = {"alert": request.get_data(as_text=True)}

    log.info("Received alert: %s", str(data)[:200])

    try:
        message = format_signal(data)
        send_telegram(message)
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        log.error("Failed to send Telegram message: %s", e)
        return jsonify({"error": str(e)}), 500
