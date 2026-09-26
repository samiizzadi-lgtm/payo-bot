Payo — Full English Mode Patch

This patch expands the existing language switcher so English mode affects:
- visible Persian UI text across rendered pages
- buttons, labels, empty states and common errors
- placeholders, titles and aria labels
- categories and common demo merchant names
- Persian/Arabic numerals -> Latin numerals
- Persian percent sign -> %
- Persian dates -> English dates
- تومان -> Toman in English mode (no unverified currency conversion)

It keeps Persian mode as before.

Apply:
1. Extract the ZIP into the Payo project root.
2. Run:
   powershell -ExecutionPolicy Bypass -File .pply_payo_full_english.ps1
3. Build:
   & "C:\Program Files
odejs
pm.cmd" run build
4. Test:
   - English: UI should be English and numerals Latin.
   - فارسی: UI returns to Persian/RTL.

Then deploy:
   git add .
   git commit -m "Complete English localization"
   git push origin main
