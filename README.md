# Arduino Button Sound

مشروع تفاعلي: **5 أزرار** على Arduino Uno (أو متوافق) — كل ضغطة ترسل رقم الزر عبر **USB Serial** إلى سكربت Python على Windows فيشغّل ملف MP3 مرتبط بالزر.

## المتطلبات

| الطرف | الأدوات |
|--------|---------|
| **Arduino** | لوحة Uno/Nano، 5 أزرار، أسلاك، USB |
| **الكمبيوتر** | Windows، Python 3.10+، منفذ COM (افتراضي `COM5`) |
| **Arduino IDE** | لرفع السكيتش |

## هيكل المشروع

```
arduino-button-sound/
├── arduino/
│   ├── button_sound/           # السكيتش المستخدم (Pins 4,8,9,10,11)
│   └── button_sound_five/      # بديل (Pins 2,3,4,5,6)
├── pc/
│   ├── play_sound.py           # يستمع للـ Serial ويشغّل الصوت
│   ├── requirements.txt
│   └── *.mp3                   # ملفات الصوت (محلياً — غير مرفوعة لـ Git)
├── README.md
├── PROJECT_AI_INSTRUCTIONS.md
└── AGENTS.md
```

## التوصيل (السكيتش `button_sound`)

كل زر: طرف واحد → **Pin**، الطرف الآخر → **GND**. السكيتش يستخدم `INPUT_PULLUP` (الضغطة = LOW).

| الزر | Pin Arduino | ملف الصوت (في `pc/`) |
|------|-------------|----------------------|
| 1 | 4 | `madrid.mp3` |
| 2 | 8 | `jordan.mp3` |
| 3 | 9 | `wehdat.mp3` |
| 4 | 10 | `faisaly.mp3` |
| 5 | 11 | `baracalona.mp3` |

عند الضغط يرسل Arduino سطراً واحداً: `1` … `5` على **9600 baud**.

## ملفات الصوت

ضع ملفات MP3 الخمسة داخل مجلد `pc/` بالأسماء أعلاه. الملفات **مستثناة من Git** (`.gitignore`) لأنها كبيرة.

## التشغيل

### 1) رفع السكيتش

1. افتح `arduino/button_sound/button_sound.ino` في Arduino IDE.
2. اختر اللوحة والمنفذ الصحيح.
3. ارفع السكيتش (**Upload**).
4. أغلق **Serial Monitor** قبل تشغيل Python (منفذ COM واحد فقط).

### 2) تشغيل Python

```powershell
cd pc
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python play_sound.py
```

### 3) السلوك

- كل زر يشغّل صوته لمدة **60 ثانية** (قابلة للتعديل في `PLAY_DURATION_SEC`).
- ضغطة زر **آخر** توقف الصوت الحالي وتبدأ الجديد.
- الضغط المتكرر على **نفس الزر** أثناء التشغيل يُتجاهل.

## تغيير منفذ COM

عدّل في `pc/play_sound.py`:

```python
PORT = "COM5"  # غيّره حسب Device Manager
```

## السكيتش البديل

`arduino/button_sound_five/button_sound_five.ino` يستخدم Pins **2–6** بدلاً من 4,8,9,10,11. إذا استخدمته، حدّث `SOUND_FILES` و`BUTTON_LABELS` في `play_sound.py` لتطابق التوصيل.

## GitHub

- **المستودع:** https://github.com/abdallah-elsabeeh/arduino-button-sound
- **الفرع الرئيسي:** `master`

## توثيق AI

- `PROJECT_AI_INSTRUCTIONS.md` — تعليمات تفصيلية للمساعدين
- `AGENTS.md` — قواعد مختصرة
