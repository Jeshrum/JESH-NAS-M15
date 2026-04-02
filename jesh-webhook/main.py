"""
JESH Signal Server — NAS100 + XAUUSD (Doctor Praise)
- Runs live signal engines every 15 minutes (no TradingView Pro needed)
- NAS100  : JESH NAS M15 strategy  (9:30 AM–4:55 PM NY)
- XAUUSD  : DOCTOR PRAISE strategy (10:00 AM–1:00 PM NY)
- Sends all alerts to Telegram
"""

import os
import json
import logging
import threading
import time as time_module
import requests
from flask import Flask, request, jsonify
from live_signal import check_signals
from dp_live_signal import dp_check_signals

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


def format_nas_signal(data: dict) -> str:
    """Format inbound TradingView webhook payload for NAS100."""
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
            "Opening Range is now being set.\n"
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


# ── Scheduler — runs both signal engines every 15 minutes ────────────────────

def scheduler_loop():
    log.info("Signal scheduler started — NAS100 + XAUUSD, every 15 minutes")

    # Run both immediately on startup
    for fn, name in [(check_signals, "NAS"), (dp_check_signals, "DP")]:
        try:
            fn()
        except Exception as e:
            log.error("[%s] Startup check error: %s", name, e)

    while True:
        time_module.sleep(15 * 60)
        for fn, name in [(check_signals, "NAS"), (dp_check_signals, "DP")]:
            try:
                fn()
            except Exception as e:
                log.error("[%s] Signal check error: %s", name, e)


scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
scheduler_thread.start()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status":     "JESH signal server running ✅",
        "strategies": ["NAS100 (JESH M15)", "XAUUSD (Doctor Praise)"],
        "mode":       "live polling every 15 minutes"
    }), 200


@app.route("/jesh", methods=["POST"])
def webhook():
    """TradingView webhook receiver for NAS100 (for future TV Pro use)."""
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

    log.info("NAS webhook received: %s", str(data)[:200])

    try:
        message = format_nas_signal(data)
        send_telegram(message)
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        log.error("Webhook send error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/check", methods=["GET"])
def manual_check():
    """Manually trigger both signal checks — for testing."""
    results = {}
    for fn, name in [(check_signals, "nas"), (dp_check_signals, "dp")]:
        try:
            fn()
            results[name] = "ok"
        except Exception as e:
            results[name] = str(e)
    return jsonify({"status": "check complete", "results": results}), 200


@app.route("/check/dp", methods=["GET"])
def manual_check_dp():
    """Manually trigger Doctor Praise signal check only."""
    try:
        dp_check_signals()
        return jsonify({"status": "Doctor Praise check complete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
