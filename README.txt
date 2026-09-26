Payo Language Patch

This patch adds:
- A visible English / فارسی language switcher in the top bar
- Persistent language selection with localStorage
- RTL for Persian and LTR for English
- Bilingual top navigation, Add button, print/reset menu and mobile labels
- A reusable i18n provider and useLanguage hook

Apply:
1. Open PowerShell in the Payo project root.
2. Run:
   powershell -ExecutionPolicy Bypass -File .\add_payo_language.ps1
3. Then:
   npm run build
4. Then:
   git add .
   git commit -m "Add English and Persian language switcher"
   git push origin main

This patch intentionally avoids changing the Telegram bot.
