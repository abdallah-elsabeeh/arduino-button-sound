# Agent Instructions — Arduino Button Sound

تعليمات لأي AI agent يعمل على هذا المستودع.

## Required Reading

قبل تعديل غير بسيط، اقرأ:

- `PROJECT_AI_INSTRUCTIONS.md`
- `README.md`
- الملفات المتأثرة: `.ino` في `arduino/` و/أو `pc/play_sound.py`

## Project Summary

- **Arduino:** 5 أزرار → Serial (`1`–`5` @ 9600 baud).
- **PC:** Python يقرأ COM ويشغّل MP3 من `pc/`.
- **السكيتش الافتراضي:** `arduino/button_sound/button_sound.ino`.

## Agent Rules

- لا ترفع ملفات صوت (`.mp3`/`.wav`) — موجودة في `.gitignore`.
- حافظ على تزامن بروتوكول Serial بين Arduino و Python.
- لا تفترض منفذ COM — القيمة الافتراضية `COM5` قابلة للتغيير محلياً.
- لا commit ولا push إلا بطلب صريح من المستخدم.
- لا أوامر SSH على السيرفر — المشروع محلي فقط.
- الفرع الرئيسي: `master`.

التفاصيل في `PROJECT_AI_INSTRUCTIONS.md`.
