# Routing tests

Run `python check.py`. Each row: a message → expected specialist and model (steps 1–3; Answer mode isn't simulated, so every message asks for work).
Add a row whenever you change keywords or hit a misroute.

## Cases

| Message | Specialist | Model |
|---|---|---|
| السلام عليكم | chat | Haiku |
| إسلام عايز لاندنج بيدج للعيادة | ui-designer | Sonnet |
| اعملي ترجمة على الفيديو ده | video-editor | Sonnet |
| ترجملي الجملة دي للإنجليزي | general | Haiku |
| دمج الـbranch ده في main وارفع الكود | coder | Sonnet |
| اعمل merge للـbranch ده ورجّع الكود | coder | Sonnet |
| copy the config file to the server and deploy | coder | Sonnet |
| find the bug in auth.ts | coder | Opus |
| الكود مش شغال في صفحة اللوجين | coder | Opus |
| !opus اكتبلي بوست عن الذكاء الاصطناعي | content-writer | Opus |
| اعمل سكيل جديدة للفواتير | skill-builder | Opus |
| اعملي ريل 30 ثانية عن المنتج | reels-maker | Sonnet |
| عايز تعليق صوتي بصوتي للسكريبت ده | voice | Haiku |
| ابني تطبيق كامل لإدارة المخزن | project | Opus |
| اعمل workflow على n8n يبعت ايميل | automation | Sonnet |
| اعمل كاروسيل 5 سلايدات عن التسويق | social-designer | Sonnet |
| راجع الكود ده من ناحية الأمان | reviewer | Opus |
| صمم النظام لمنصة حجوزات | architect | Opus |
| ابحث عن ريبو OCR عربي مجاني | researcher | Sonnet |
| build a quick landing page | ui-designer | Sonnet |
| اعملي لاندنج بيدج بسرعة كده | ui-designer | Sonnet |
| what is wrong with my api endpoint, fix it | coder | Sonnet |
| لخصلي المقال ده في بوست لينكدان | content-writer | Haiku |
