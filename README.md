# Personal Assistant with Sub-Agents (Supervisor Pattern)

نظام مساعد شخصي يعتمد على **نمط المشرف (Supervisor)**:
- **طبقة أدوات**: أدوات تقويم وبريد تحتاج مدخلات منظمة (ISO، عناوين بريد).
- **طبقة وكلاء فرعيين**: وكيل تقويم ووكيل بريد يترجمان الطلبات الطبيعية إلى استدعاءات API.
- **طبقة مشرف**: مشرف واحد يوجّه الطلبات إلى الوكيل المناسب ويجمع النتائج.

## التثبيت

```bash
pip install -r requirements.txt
```

## المفاتيح

- **OpenRouter** (مثل Nemotron): اضبط `OPENROUTER_API_KEY`.
- **OpenAI**: أو اضبط `OPENAI_API_KEY`.

```bash
export OPENROUTER_API_KEY="sk-..."   # من https://openrouter.ai/keys
# أو
export OPENAI_API_KEY="sk-..."
```

## التشغيل

طلب واحد من سطر الأوامر:

```bash
python main.py "Schedule a team standup for tomorrow at 9am"
```

تشغيل أمثلة (تقويم فقط، ثم تقويم + بريد):

```bash
python main.py
```

## الهيكل

- `tools.py` — أدوات API: `create_calendar_event`, `get_available_time_slots`, `send_email`
- `agents.py` — وكيل تقويم، وكيل بريد، وكلاهما مُعرّف كأداة للمشرف؛ ثم المشرف
- `main.py` — نقطة الدخول واستدعاء المشرف

## ملاحظة

أدوات التقويم والبريد حالياً **stubs** (لا تتصل بـ Google Calendar أو Gmail فعلياً). يمكن استبدالها لاحقاً بـ APIs حقيقية.
