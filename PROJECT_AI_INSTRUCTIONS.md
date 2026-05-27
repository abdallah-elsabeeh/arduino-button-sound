# Arduino Button Sound — تعليمات المشروع

## نظرة عامة

مشروع **Hardware + PC**: Arduino يقرأ 5 أزرار ويرسل رقم الزر عبر Serial؛ Python على Windows يستقبل الرقم ويشغّل MP3 من مجلد `pc/`.

| الحقل | القيمة |
|-------|--------|
| **GitHub** | https://github.com/abdallah-elsabeeh/arduino-button-sound |
| **الفرع الرئيسي** | `master` |
| **Arduino** | C++ (Arduino IDE)، 9600 baud |
| **PC** | Python 3.10+، `pyserial`، `playsound3` |
| **النشر** | لا يوجد سيرفر — تشغيل محلي على Windows فقط |

---

## هيكل المشروع

```
arduino-button-sound/
├── arduino/
│   ├── button_sound/button_sound.ino      # الإنتاج: Pins 4,8,9,10,11
│   └── button_sound_five/button_sound_five.ino  # بديل: Pins 2–6
├── pc/
│   ├── play_sound.py      # نقطة الدخول — Serial → تشغيل صوت
│   ├── requirements.txt
│   └── *.mp3              # محلياً فقط (gitignored)
├── README.md
├── PROJECT_AI_INSTRUCTIONS.md
└── AGENTS.md
```

---

## بروتوكول Serial

- **Baud:** 9600
- **الرسالة:** سطر نصي `1`–`5` + `\n` عند **ضغطة** (انتقال HIGH→LOW مع debounce).
- **Debounce:** 60 ms (`button_sound`) أو 50 ms (`button_sound_five`).

لا تغيّر البروتوكول من جهة Arduino دون تحديث `SOUND_FILES` في Python.

---

## خريطة الأزرار (السكيتش الافتراضي `button_sound`)

| `btn_id` | Pin | ملف MP3 | تسمية في الكود |
|----------|-----|---------|----------------|
| `1` | 4 | `madrid.mp3` | madrid |
| `2` | 8 | `jordan.mp3` | jordan |
| `3` | 9 | `wehdat.mp3` | wehdat |
| `4` | 10 | `faisaly.mp3` | faisaly |
| `5` | 11 | `baracalona.mp3` | baracalona |

---

## منطق Python (`play_sound.py`)

- **PORT:** `COM5` (ثابت — يُعدّل يدوياً).
- **PLAY_DURATION_SEC:** 60 — مدة التشغيل قبل الإيقاف التلقائي.
- **تزامن:** `threading.Lock` + `_play_generation` لإيقاف الصوت السابق عند زر جديد.
- **نفس الزر مرتين:** إذا `_active_btn == btn_id` يُتجاهل الضغط الثاني.
- عند البدء: يتحقق من وجود كل ملفات MP3؛ إن وُجد ناقص يخرج بـ `sys.exit(1)`.
- بعد فتح Serial: `time.sleep(2)` لانتظار reset Arduino.

---

## تشغيل التطوير

```powershell
cd projects/arduino-button-sound/pc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# ضع ملفات mp3 في pc/ ثم:
python play_sound.py
```

**تحذير:** Serial Monitor في Arduino IDE يحجز المنفذ — أغلقه قبل `play_sound.py`.

---

## تعديلات شائعة

| المطلوب | أين |
|---------|-----|
| منفذ COM | `PORT` في `play_sound.py` |
| مدة التشغيل | `PLAY_DURATION_SEC` |
| أسماء/مسارات MP3 | `SOUND_FILES`, `BUTTON_LABELS` |
| Pins الأزرار | `BUTTON_PINS[]` في `.ino` + مزامنة Python |
| عدد الأزرار | `NUM_BUTTONS` في `.ino` + قاموس Python |

---

## ما لا يفعله المشروع

- لا WiFi / Bluetooth / MQTT.
- لا واجهة ويب ولا قاعدة بيانات.
- لا نشر على السيرفر (`77.42.71.95`) — غير ذي صلة.

---

## قواعد للمساعد AI

1. لا ترفع ملفات `.mp3` إلى Git.
2. لا تُدرج مفاتيح SSH أو tokens في الكود أو التوثيق.
3. عند تغيير Pins في Arduino، حدّث README و`BUTTON_LABELS` معاً.
4. الفرع الافتراضي: **`master`** — لا تحذف الفرع بعد الدمج على GitHub.
5. لا `git commit` إلا إذا طلب المستخدم صراحة.

---

*آخر مراجعة: 2026-05-28.*
