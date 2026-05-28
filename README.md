# Arduino Button Sound

مشروع تفاعلي: **5 أزرار** على Arduino — كل ضغطة ترسل رقم الزر عبر **USB Serial** إلى Python على Windows فيشغّل **فيديو MP4** (صوت + صورة معاً) **ملء شاشة البروجكتور** عبر HDMI.

## المتطلبات

| الطرف | الأدوات |
|--------|---------|
| **Arduino** | لوحة Uno/Nano، 5 أزرار، أسلاك، USB |
| **الكمبيوتر** | Windows، Python 3.10+، منفذ COM (افتراضي `COM5`) |
| **البروجكتور** | HDMI كشاشة ثانية (وضع **توسيع** في Windows) |
| **مشغّل فيديو** | [mpv](https://mpv.io/) (مفضّل) أو VLC |
| **Arduino IDE** | لرفع السكيتش |

## هيكل المشروع

```
arduino-button-sound/
├── arduino/
│   ├── button_sound/           # السكيتش المستخدم (Pins 4,8,9,10,11)
│   └── button_sound_five/      # بديل (Pins 2,3,4,5,6)
├── pc/
│   ├── play_sound.py           # يستمع للـ Serial ويشغّل الفيديو على البروجكتور
│   ├── requirements.txt
│   └── videos/*.mp4            # ملفات الفيديو (محلياً — غير مرفوعة لـ Git)
├── README.md
├── PROJECT_AI_INSTRUCTIONS.md
└── AGENTS.md
```

## التوصيل (السكيتش `button_sound`)

كل زر: طرف واحد → **Pin**، الطرف الآخر → **GND**. السكيتش يستخدم `INPUT_PULLUP` (الضغطة = LOW).

| الزر | Pin Arduino | ملف الفيديو (في `pc/videos/`) |
|------|-------------|-------------------------|
| 1 | 4 | `realmadrid.mp4` |
| 2 | 8 | `barca.mp4` |

عند الضغط يرسل Arduino سطراً واحداً: `1` … `5` على **9600 baud**.

## ملفات الفيديو

ضع ملفات **MP4** داخل `pc/videos/` بالأسماء أعلاه. الصوت مدمج داخل الفيديو — لا حاجة لملفات MP3 منفصلة. الملفات **مستثناة من Git** لأنها كبيرة.

## إعداد البروجكتور (HDMI)

1. وصّل البروجكتور بـ HDMI واختر **توسيع** الشاشة (Win + P → Extend).
2. في `play_sound.py` اضبط `PROJECTOR_SCREEN`:
   - `0` = الشاشة الرئيسية
   - `1` = الشاشة الثانية (غالباً البروجكتور)
3. ثبّت **mpv** أو **VLC** على Windows.

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

- كل زر يشغّل **فيديوه كاملاً** (صوت + صورة على البروجكتور).
- `PLAY_DURATION_SEC = 0` يعني تشغيل الملف حتى النهاية؛ ضع رقماً (مثلاً `60`) لحد أقصى بالثواني.
- ضغطة زر **آخر** توقف الفيديو الحالي وتبدأ الجديد.
- الضغط المتكرر على **نفس الزر** أثناء التشغيل يُتجاهل.

## تغيير منفذ COM

عدّل في `pc/play_sound.py`:

```python
PORT = "COM5"  # غيّره حسب Device Manager
```

## السكيتش البديل

`arduino/button_sound_five/button_sound_five.ino` يستخدم Pins **2–6** بدلاً من 4,8,9,10,11. إذا استخدمته، حدّث `VIDEO_FILES` و`BUTTON_LABELS` في `play_sound.py` لتطابق التوصيل.

## GitHub

- **المستودع:** https://github.com/abdallah-elsabeeh/arduino-button-sound
- **الفرع الرئيسي:** `master`

## توثيق AI

- `PROJECT_AI_INSTRUCTIONS.md` — تعليمات تفصيلية للمساعدين
- `AGENTS.md` — قواعد مختصرة
