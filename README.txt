Payo Full English Fix

این پچ مشکل صفحه‌ای که فقط لوگوی Payo را نشان می‌دهد را اصلاح می‌کند.

Changes:
- MutationObserver دیگر هنگام ترجمه خودش را دوباره trigger نمی‌کند.
- Observer هنگام اعمال ترجمه disconnect می‌شود و سپس دوباره فعال می‌شود.
- Splash overlay حذف می‌شود تا سایت همیشه وارد Dashboard شود.
- English / فارسی و ترجمه سراسری فعلی حفظ می‌شود.
- Telegram bot files are not modified.

Apply:
1. Extract this ZIP into:
   C:\Users\orchidpharmed\OneDrive\Documents\telegram_bot

2. Run:
   powershell -ExecutionPolicy Bypass -File .\fix_payo_full_english.ps1

3. Build:
   & "C:\Program Files\nodejs\npm.cmd" run build

4. Test locally:
   & "C:\Program Files\nodejs\npm.cmd" run preview -- --host 127.0.0.1

   Open:
   http://127.0.0.1:4173/payo-bot/

5. After the site opens correctly:
   git add .
   git commit -m "Fix Payo English mode runtime"
   git push origin main
