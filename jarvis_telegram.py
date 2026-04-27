import json
import hmac
import queue
import re
import threading
import time
import urllib.error
import urllib.parse


def _tg_fix_mojibake_text(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    # Typical broken UTF-8->CP1251 decoding produces many uppercase
    # Cyrillic "Р"/"С" markers. Recover original UTF-8 text when detected.
    marker_count = sum(1 for ch in text if ch in ("\u0420", "\u0421"))
    if marker_count < 3:
        return text
    for source_encoding in ("cp1251", "latin1"):
        try:
            candidate = text.encode(source_encoding).decode("utf-8").strip()
        except Exception:
            continue
        if not candidate:
            continue
        candidate_marker_count = sum(1 for ch in candidate if ch in ("\u0420", "\u0421"))
        candidate_cyr_count = sum(1 for ch in candidate if "\u0400" <= ch <= "\u04FF")
        if candidate_marker_count + 2 <= marker_count and candidate_cyr_count >= 2:
            return candidate
    return text


def _tg_normalize_text(value: object) -> str:
    fixed = _tg_fix_mojibake_text(value)
    return " ".join(fixed.replace("\n", " ").split()).strip()


def _tg_pick_language_text(language_key: object, ru: str, en: str, uk: str) -> str:
    key = _tg_normalize_text(language_key).casefold()
    if "english" in key or key in {"en", "eng"}:
        return _tg_fix_mojibake_text(en)
    if "\u0443\u043a\u0440\u0430" in key or key in {"uk", "ua"}:
        return _tg_fix_mojibake_text(uk)
    return _tg_fix_mojibake_text(ru)


class JarvisTelegramMixin:
    """Telegram polling/sending helpers for JarvisWindow."""

    def _schedule_telegram_sync(self, delay_ms: int = 320) -> None:
        timer = getattr(self, "_telegram_sync_timer", None)
        if timer is not None and hasattr(timer, "start"):
            timer.start(max(0, int(delay_ms)))
            return
        self._sync_telegram_bot_worker()

    def _set_telegram_runtime_status(self, text: object) -> None:
        raw = _tg_normalize_text(text)
        if raw == str(getattr(self, "_telegram_last_status", "") or ""):
            return
        self._telegram_last_status = raw
        try:
            self._telegram_status_requested.emit(raw)
        except Exception:
            pass

    def _on_telegram_status_requested(self, text: str) -> None:
        self._telegram_last_status = _tg_normalize_text(text)
        page = getattr(self, "settings_page", None)
        if page is not None and hasattr(page, "set_tg_bot_status_text"):
            try:
                page.set_tg_bot_status_text(self._telegram_last_status)
            except Exception:
                pass

    def _on_telegram_phrase_received(self, phrase: str, chat_id: str, message_id: int) -> None:
        text = _tg_normalize_text(phrase)
        if not text:
            return
        chat = str(chat_id or "").strip()
        if chat:
            self._append_runtime_line(f"TG[{chat}]: {text}", "lead", force_home=True)
        else:
            self._append_runtime_line(f"TG: {text}", "lead", force_home=True)
        self._enqueue_command_execution(text, source="telegram", chat_id=chat, message_id=int(message_id or 0))

    def _queue_telegram_outgoing_message(self, chat_id: object, text: object) -> None:
        chat = str(chat_id or "").strip()
        body = _tg_normalize_text(text)
        if not chat or not body:
            return
        if len(body) > 3600:
            body = body[:3590].rstrip() + "..."
        payload = (chat, body)
        queue_obj = getattr(self, "_telegram_outgoing_queue", None)
        if not isinstance(queue_obj, queue.Queue):
            return
        try:
            queue_obj.put_nowait(payload)
            return
        except Exception:
            pass
        try:
            _ = queue_obj.get_nowait()
        except Exception:
            pass
        try:
            queue_obj.put_nowait(payload)
        except Exception:
            pass

    def _telegram_api_get_json(
        self,
        token: str,
        method: str,
        params: dict[str, object] | None = None,
        timeout_sec: float = 6.0,
        max_bytes: int = 420_000,
    ) -> dict[str, object]:
        safe_token = str(token or "").strip()
        api_method = str(method or "").strip()
        if not safe_token or not api_method:
            return {}
        payload_pairs: list[tuple[str, str]] = []
        if isinstance(params, dict):
            for key, value in params.items():
                payload_pairs.append((str(key), str(value)))
        query = urllib.parse.urlencode(payload_pairs)
        url = f"https://api.telegram.org/bot{safe_token}/{api_method}"
        if query:
            url = f"{url}?{query}"
        try:
            payload = self._web_fetch_json(
                url,
                timeout_sec=max(1.2, float(timeout_sec)),
                max_bytes=max(96_000, int(max_bytes)),
            )
            return payload if isinstance(payload, dict) else {}
        except urllib.error.HTTPError as exc:
            code = int(getattr(exc, "code", 0) or 0)
            body_text = ""
            try:
                body_text = bytes(exc.read() or b"").decode("utf-8", errors="ignore").strip()
            except Exception:
                body_text = ""
            if body_text:
                try:
                    parsed = json.loads(body_text)
                    if isinstance(parsed, dict):
                        parsed.setdefault("ok", False)
                        if code > 0 and "error_code" not in parsed:
                            parsed["error_code"] = code
                        return parsed
                except Exception:
                    pass
            return {"ok": False, "error_code": code, "description": body_text or f"http_{code}"}
        except Exception as exc:
            return {"ok": False, "description": str(exc)}

    def _telegram_send_message_api(self, token: str, chat_id: str, text: str) -> bool:
        payload = self._telegram_api_get_json(
            token,
            "sendMessage",
            params={
                "chat_id": str(chat_id or "").strip(),
                "text": str(text or ""),
                "disable_web_page_preview": "true",
            },
            timeout_sec=6.0,
            max_bytes=220_000,
        )
        if not isinstance(payload, dict):
            return False
        return bool(payload.get("ok", False))

    def _telegram_help_text(self) -> str:
        base = _tg_pick_language_text(
            self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
            "Jarvis TG bot: РѕС‚РїСЂР°РІСЊС‚Рµ Р»СЋР±СѓСЋ РєРѕРјР°РЅРґСѓ РєР°Рє РІ РѕСЃРЅРѕРІРЅРѕРј РѕРєРЅРµ. /id - РїРѕРєР°Р·Р°С‚СЊ chat id.",
            "Jarvis TG bot: send any command like in the main window. /id shows chat id.",
            "Jarvis TG bot: РЅР°РґС–С€Р»С–С‚СЊ Р±СѓРґСЊ-СЏРєСѓ РєРѕРјР°РЅРґСѓ СЏРє Сѓ РіРѕР»РѕРІРЅРѕРјСѓ РІС–РєРЅС–. /id РїРѕРєР°Р¶Рµ chat id.",
        )
        if self._telegram_password_required():
            base = f"{base} " + _tg_pick_language_text(
                self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                "Авторизация: /login <пароль>. Выход: /logout.",
                "Authorization: /login <password>. Logout: /logout.",
                "Авторизація: /login <пароль>. Вихід: /logout.",
            )
        return base

    def _telegram_password_value(self) -> str:
        return str(self._settings.get("tg_bot_password", "") or "").strip()

    def _telegram_password_required(self) -> bool:
        return bool(self._telegram_password_value())

    def _telegram_is_chat_authorized(self, chat_id: str) -> bool:
        chat = str(chat_id or "").strip()
        if not chat:
            return False
        sessions = getattr(self, "_telegram_auth_sessions", None)
        if not isinstance(sessions, dict):
            return False
        now_ts = time.monotonic()
        expires_at = float(sessions.get(chat, 0.0) or 0.0)
        if expires_at <= now_ts:
            sessions.pop(chat, None)
            return False
        return True

    def _telegram_authorize_chat(self, chat_id: str) -> None:
        chat = str(chat_id or "").strip()
        if not chat:
            return
        sessions = getattr(self, "_telegram_auth_sessions", None)
        if not isinstance(sessions, dict):
            return
        ttl = int(getattr(self, "_telegram_auth_ttl_sec", 1800) or 1800)
        ttl = max(60, min(24 * 3600, ttl))
        sessions[chat] = time.monotonic() + float(ttl)

    def _telegram_revoke_chat(self, chat_id: str) -> None:
        chat = str(chat_id or "").strip()
        sessions = getattr(self, "_telegram_auth_sessions", None)
        if chat and isinstance(sessions, dict):
            sessions.pop(chat, None)

    def _telegram_check_password(self, supplied_password: str) -> bool:
        expected = self._telegram_password_value()
        actual = str(supplied_password or "").strip()
        if not expected:
            return True
        if not actual:
            return False
        try:
            return bool(hmac.compare_digest(expected, actual))
        except Exception:
            return expected == actual

    @staticmethod
    def _telegram_extract_login_payload(text: str) -> tuple[bool, str, str]:
        source = _tg_normalize_text(text)
        if not source:
            return False, "", ""
        match = re.match(
            r"^(?:/(?:login|pass|password)|login|password|пароль|логин|вход)\s*(.*)$",
            source,
            flags=re.IGNORECASE,
        )
        if match is None:
            return False, "", ""
        tail = _tg_normalize_text(match.group(1))
        if not tail:
            return True, "", ""
        if ";" in tail:
            pwd, cmd_tail = tail.split(";", 1)
            return True, _tg_normalize_text(pwd), _tg_normalize_text(cmd_tail)
        parts = tail.split(maxsplit=1)
        password = _tg_normalize_text(parts[0] if parts else "")
        command_tail = _tg_normalize_text(parts[1] if len(parts) > 1 else "")
        return True, password, command_tail

    def _telegram_poll_loop(self) -> None:
        # This loop intentionally keeps retries simple: fewer moving parts,
        # predictable behavior, and no hidden exponential backoff magic.
        backoff = 0.4
        self._set_telegram_runtime_status(
            _tg_pick_language_text(
                self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                "РўР“ Р±РѕС‚: РїРѕРґРєР»СЋС‡РµРЅРёРµ...",
                "TG bot: connecting...",
                "РўР“ Р±РѕС‚: РїС–РґРєР»СЋС‡РµРЅРЅСЏ...",
            )
        )
        while not self._telegram_stop.is_set():
            if not bool(self._settings.get("tg_bot_enabled", False)):
                break
            token = str(self._settings.get("tg_bot_token", "") or "").strip()
            if not token:
                self._set_telegram_runtime_status(
                    _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: РІРєР»СЋС‡РµРЅ, РЅРѕ С‚РѕРєРµРЅ РЅРµ Р·Р°РґР°РЅ.",
                        "TG bot is enabled but token is missing.",
                        "РўР“ Р±РѕС‚ СѓРІС–РјРєРЅРµРЅРѕ, Р°Р»Рµ С‚РѕРєРµРЅ РЅРµ РІРєР°Р·Р°РЅРёР№.",
                    )
                )
                time.sleep(0.45)
                continue
            self._telegram_active_token = token

            flush_limit = 16
            while flush_limit > 0 and not self._telegram_stop.is_set():
                flush_limit -= 1
                item = None
                try:
                    item = self._telegram_outgoing_queue.get_nowait()
                except queue.Empty:
                    break
                except Exception:
                    item = None
                if item is None:
                    continue
                out_chat_id = str(item[0] if len(item) > 0 else "").strip() if isinstance(item, tuple) else ""
                out_text = str(item[1] if len(item) > 1 else "").strip() if isinstance(item, tuple) else ""
                if not out_chat_id or not out_text:
                    continue
                if not self._telegram_send_message_api(token, out_chat_id, out_text):
                    self._set_telegram_runtime_status(
                        _tg_pick_language_text(
                            self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                            "РўР“ Р±РѕС‚: РѕС€РёР±РєР° РѕС‚РїСЂР°РІРєРё СЃРѕРѕР±С‰РµРЅРёСЏ.",
                            "TG bot: failed to send message.",
                            "РўР“ Р±РѕС‚: РїРѕРјРёР»РєР° РЅР°РґСЃРёР»Р°РЅРЅСЏ РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ.",
                        )
                    )

            payload = self._telegram_api_get_json(
                token,
                "getUpdates",
                params={
                    "offset": str(max(0, int(self._telegram_update_offset))),
                    "timeout": "4",
                    "allowed_updates": '["message"]',
                },
                timeout_sec=6.5,
                max_bytes=900_000,
            )
            if not isinstance(payload, dict) or not payload:
                self._set_telegram_runtime_status(
                    _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: СЃРµС‚СЊ РЅРµРґРѕСЃС‚СѓРїРЅР°.",
                        "TG bot: network unavailable.",
                        "РўР“ Р±РѕС‚: РјРµСЂРµР¶Р° РЅРµРґРѕСЃС‚СѓРїРЅР°.",
                    )
                )
                time.sleep(backoff)
                backoff = min(3.2, backoff + 0.4)
                continue

            if not bool(payload.get("ok", False)):
                description = _tg_normalize_text(payload.get("description", "")).lower()
                if "unauthorized" in description or "401" in description:
                    status_line = _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: РЅРµРІРµСЂРЅС‹Р№ С‚РѕРєРµРЅ.",
                        "TG bot: invalid token.",
                        "РўР“ Р±РѕС‚: РЅРµРІС–СЂРЅРёР№ С‚РѕРєРµРЅ.",
                    )
                else:
                    status_line = _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: РѕС€РёР±РєР° API.",
                        "TG bot: API error.",
                        "РўР“ Р±РѕС‚: РїРѕРјРёР»РєР° API.",
                    )
                self._set_telegram_runtime_status(status_line)
                time.sleep(backoff)
                backoff = min(3.2, backoff + 0.4)
                continue

            backoff = 0.4
            updates = payload.get("result")
            if not isinstance(updates, list):
                continue
            if updates:
                self._set_telegram_runtime_status(
                    _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: РїРѕРґРєР»СЋС‡РµРЅ.",
                        "TG bot: connected.",
                        "РўР“ Р±РѕС‚: РїС–РґРєР»СЋС‡РµРЅРѕ.",
                    )
                )

            for update in updates:
                if not isinstance(update, dict):
                    continue
                update_id = int(update.get("update_id", 0) or 0)
                if update_id > 0 and update_id >= int(self._telegram_update_offset):
                    self._telegram_update_offset = update_id + 1
                    self._settings["tg_bot_update_offset"] = int(self._telegram_update_offset)
                    save_ts = float(getattr(self, "_telegram_offset_save_ts", 0.0) or 0.0)
                    now_ts = time.monotonic()
                    if (now_ts - save_ts) >= 1.2:
                        self._telegram_offset_save_ts = now_ts
                        self._schedule_settings_save(180)

                message = update.get("message")
                if not isinstance(message, dict):
                    continue
                chat_data = message.get("chat")
                if not isinstance(chat_data, dict):
                    continue
                chat_id = str(chat_data.get("id", "") or "").strip()
                if not chat_id:
                    continue
                text = _tg_normalize_text(message.get("text", ""))
                if not text:
                    continue

                allowed_chat_id = str(self._settings.get("tg_bot_allowed_chat_id", "") or "").strip()
                if allowed_chat_id and chat_id != allowed_chat_id:
                    continue

                message_id = int(message.get("message_id", 0) or 0)
                cmd = text.casefold()
                if cmd in {"/start", "/help"}:
                    self._queue_telegram_outgoing_message(chat_id, self._telegram_help_text())
                    continue
                if cmd in {"/id", "/chatid"}:
                    self._queue_telegram_outgoing_message(chat_id, f"chat id: {chat_id}")
                    continue
                if cmd in {"/logout", "logout", "выход", "выйти", "log out"}:
                    self._telegram_revoke_chat(chat_id)
                    self._queue_telegram_outgoing_message(
                        chat_id,
                        _tg_pick_language_text(
                            self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                            "Сессия Telegram завершена.",
                            "Telegram session logged out.",
                            "Сесію Telegram завершено.",
                        ),
                    )
                    continue
                if self._telegram_password_required():
                    has_login, supplied_password, command_tail = self._telegram_extract_login_payload(text)
                    if has_login:
                        if not supplied_password:
                            self._queue_telegram_outgoing_message(
                                chat_id,
                                _tg_pick_language_text(
                                    self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                                    "Введите пароль: /login <пароль>",
                                    "Enter password: /login <password>",
                                    "Введіть пароль: /login <пароль>",
                                ),
                            )
                            continue
                        if not self._telegram_check_password(supplied_password):
                            self._telegram_revoke_chat(chat_id)
                            self._queue_telegram_outgoing_message(
                                chat_id,
                                _tg_pick_language_text(
                                    self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                                    "Неверный пароль Telegram-бота.",
                                    "Invalid Telegram bot password.",
                                    "Невірний пароль Telegram-бота.",
                                ),
                            )
                            continue
                        self._telegram_authorize_chat(chat_id)
                        if command_tail:
                            text = command_tail
                            cmd = text.casefold()
                        else:
                            self._queue_telegram_outgoing_message(
                                chat_id,
                                _tg_pick_language_text(
                                    self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                                    "Доступ разрешен. Теперь отправьте команду.",
                                    "Access granted. Send a command now.",
                                    "Доступ дозволено. Тепер надішліть команду.",
                                ),
                            )
                            continue
                    if not self._telegram_is_chat_authorized(chat_id):
                        self._queue_telegram_outgoing_message(
                            chat_id,
                            _tg_pick_language_text(
                                self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                                "Для управления нужен пароль: /login <пароль>",
                                "Password required: /login <password>",
                                "Для керування потрібен пароль: /login <пароль>",
                            ),
                        )
                        continue
                try:
                    self._telegram_phrase_requested.emit(text, chat_id, int(message_id))
                except Exception:
                    pass

        self._set_telegram_runtime_status(
            _tg_pick_language_text(
                self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                "РўР“ Р±РѕС‚ РІС‹РєР»СЋС‡РµРЅ.",
                "TG bot is disabled.",
                "РўР“ Р±РѕС‚ РІРёРјРєРЅРµРЅРѕ.",
            )
        )

    def _sync_telegram_bot_worker(self) -> None:
        enabled = bool(self._settings.get("tg_bot_enabled", False))
        token = str(self._settings.get("tg_bot_token", "") or "").strip()
        thread = getattr(self, "_telegram_thread", None)
        alive = bool(isinstance(thread, threading.Thread) and thread.is_alive())

        if (not enabled) or (not token):
            if alive:
                self._shutdown_telegram_bot_worker(wait_ms=900)
            if enabled and not token:
                self._set_telegram_runtime_status(
                    _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚: РІРєР»СЋС‡РµРЅ, РЅРѕ С‚РѕРєРµРЅ РЅРµ Р·Р°РґР°РЅ.",
                        "TG bot is enabled but token is missing.",
                        "РўР“ Р±РѕС‚ СѓРІС–РјРєРЅРµРЅРѕ, Р°Р»Рµ С‚РѕРєРµРЅ РЅРµ РІРєР°Р·Р°РЅРёР№.",
                    )
                )
            else:
                self._set_telegram_runtime_status(
                    _tg_pick_language_text(
                        self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                        "РўР“ Р±РѕС‚ РІС‹РєР»СЋС‡РµРЅ.",
                        "TG bot is disabled.",
                        "РўР“ Р±РѕС‚ РІРёРјРєРЅРµРЅРѕ.",
                    )
                )
            return

        if alive and str(getattr(self, "_telegram_active_token", "") or "") == token:
            return

        if alive:
            self._shutdown_telegram_bot_worker(wait_ms=1200)

        self._telegram_stop.clear()
        self._telegram_active_token = token
        self._telegram_thread = threading.Thread(target=self._telegram_poll_loop, daemon=True)
        self._telegram_thread.start()
        self._set_telegram_runtime_status(
            _tg_pick_language_text(
                self._settings.get("interface_language", "Р СѓСЃСЃРєРёР№"),
                "РўР“ Р±РѕС‚: РїРѕРґРєР»СЋС‡РµРЅРёРµ...",
                "TG bot: connecting...",
                "РўР“ Р±РѕС‚: РїС–РґРєР»СЋС‡РµРЅРЅСЏ...",
            )
        )

    def _shutdown_telegram_bot_worker(self, wait_ms: int = 1400) -> None:
        timer = getattr(self, "_telegram_sync_timer", None)
        if timer is not None and hasattr(timer, "stop"):
            timer.stop()
        self._telegram_stop.set()
        try:
            self._telegram_outgoing_queue.put_nowait(None)
        except Exception:
            pass
        thread = getattr(self, "_telegram_thread", None)
        if isinstance(thread, threading.Thread) and thread.is_alive():
            thread.join(timeout=max(0.2, float(wait_ms) / 1000.0))
        self._telegram_thread = None
        self._telegram_active_token = ""
        auth_sessions = getattr(self, "_telegram_auth_sessions", None)
        if isinstance(auth_sessions, dict):
            auth_sessions.clear()

