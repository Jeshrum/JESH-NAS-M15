"""
JESH NAS M15 — Webhook + Live Signal Server
- Receives TradingView webhooks (for future Pro use)
- Runs live signal engine every 15 minutes (no TV Pro needed)
- Sends all alerts to Telegram DM
"""

import os
import json
import logging
import threading
import time as time_module
import requests
from flask import Flask, request, jsonify
from live_signal import check_signals

app = Flask(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN    = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID      = os.environ["TELEGRAM_CHAT_ID"]
SECRET       = os.environ.get("WEBHOOK_SECRET", "")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram(text: str):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(TELEGRAM_URL, json=payload, timeout=10)
    r.raise_for_status()


def format_signal(data: dict) -> str:
    alert = data.get("alert", "").upper()
    entry = data.get("entry", "")
    sl    = data.get("sl", "")
    tp1   = data.get("tp1", "")
    tp2   = data.get("tp2", "")
    tp3   = data.get("tp3", "")
    risk  = data.get("risk", "")
    qty   = data.get("qty", "")

    if "LONG" in alert:
        return (
            "🟢 <b>JESH LONG SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R TP</b>        <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
    if "SHORT" in alert:
        return (
            "🔴 <b>JESH SHORT SIGNAL · NAS100</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 <b>Limit Entry</b>  <code>{entry}</code>\n"
            f"🛑 <b>Stop Loss</b>    <code>{sl}</code>\n"
            f"🎯 <b>1R Target</b>    <code>{tp1}</code>\n"
            f"🎯 <b>2R Target</b>    <code>{tp2}</code>\n"
            f"🎯 <b>3R TP</b>        <code>{tp3}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 Risk: <b>${risk}</b>  |  Qty: <b>{qty}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Lagos: 2:30–4:30 PM WAT (summer) · 3:30–5:30 PM (winter)\n"
            "📋 Place LIMIT order · Set SL &amp; TP · Walk away"
        )
    if "SESSION" in alert or "OPEN" in alert:
        return (
            "🔔 <b>JESH Session Open — 9:30 AM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Opening Range is now set.\n"
            "Watch for breakout signal until 11:30 AM NY.\n"
            "⏰ Lagos: 2:30 PM WAT (summer) · 3:30 PM WAT (winter)"
        )
    if "FORCE" in alert or "CLOSE" in alert:
        return (
            "⚠️ <b>JESH Force Close — 4:55 PM NY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Close any open NAS100 position NOW.\n"
            "No overnight positions allowed.\n"
            "⏰ Lagos: 10:55 PM WAT"
        )
    return f"📡 <b>JESH Alert</b>\n{json.dumps(data, indent=2)}"


# ── Scheduler — runs check_signals() every 15 minutes ────────────────────────

def scheduler_loop():
    log.info("Live signal scheduler started — checking every 15 minutes")
    # Run once immediately on startup
    try:
        check_signals()
    except Exception as e:
        log.error("Signal check error: %s", e)

    while True:
        time_module.sleep(15 * 60)  # wait 15 minutes
        try:
            check_signals()
        except Exception as e:
            log.error("Signal check error: %s", e)


# Start scheduler in background thread
scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
scheduler_thread.start()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "JESH signal server running ✅",
                    "mode":   "live polling + webhook ready"}), 200


@app.route("/jesh", methods=["POST"])
def webhook():
    if SECRET:
        token = request.headers.get("X-Secret", "") or request.args.get("secret", "")
        if token != SECRET:
            return jsonify({"error": "unauthorized"}), 401

    try:
        data = request.get_json(force=True) or {}
    except Exception:
        data = {}

    if not data:
        data = {"alert": request.get_data(as_text=True)}

    log.info("Webhook received: %s", str(data)[:200])

    try:
        message = format_signal(data)
        send_telegram(message)
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        log.error("Webhook send error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/check", methods=["GET"])
def manual_check():
    """Manually trigger a signal check — for testing."""
    try:
        check_signals()
        return jsonify({"status": "check complete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
