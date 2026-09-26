$ErrorActionPreference = "Stop"

$root = Get-Location
$i18n = Join-Path $root "src\i18n.tsx"
$app = Join-Path $root "src\App.tsx"

if (-not (Test-Path $i18n)) {
    throw "src\i18n.tsx پیدا نشد. اسکریپت را از ریشه پروژه Payo اجرا کن."
}
if (-not (Test-Path $app)) {
    throw "src\App.tsx پیدا نشد. اسکریپت را از ریشه پروژه Payo اجرا کن."
}

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item $i18n "$i18n.before-fix-$stamp.bak" -Force
Copy-Item $app "$app.before-fix-$stamp.bak" -Force

# --- Fix the DOM translator ---
# The previous implementation watched characterData/attributes while also changing
# those same nodes, creating a mutation loop that can freeze the page.
$i18nText = Get-Content -Raw -Encoding UTF8 $i18n

$startMarker = "function createDocumentTranslator() {"
$endMarker = "const docTranslator ="

$start = $i18nText.IndexOf($startMarker)
$end = $i18nText.IndexOf($endMarker)

if ($start -lt 0 -or $end -lt 0 -or $end -le $start) {
    throw "بخش createDocumentTranslator در src\i18n.tsx پیدا نشد؛ فایل با نسخه فعلی متفاوت است."
}

$safeTranslator = @'
function createDocumentTranslator() {
  const textOriginals = new WeakMap<Text, string>();
  const elementOriginals = new WeakMap<HTMLElement, Record<string, string>>();
  let english = false;
  let observer: MutationObserver | null = null;
  let scanning = false;

  const observerOptions: MutationObserverInit = {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['placeholder', 'title', 'aria-label', 'aria-description'],
  };

  const skip = (node: Node) => {
    const parent = node.parentElement;
    if (!parent) return false;
    return !!parent.closest(
      'script,style,noscript,code,pre,svg,[data-payo-no-i18n]',
    );
  };

  const translateTextNode = (node: Text) => {
    if (skip(node)) return;

    const current = node.nodeValue ?? '';

    if (!textOriginals.has(node) && containsPersian(current)) {
      textOriginals.set(node, current);
    }

    const original = textOriginals.get(node);
    if (original == null) return;

    const next = english ? translatePersianText(original) : original;

    if (node.nodeValue !== next) {
      node.nodeValue = next;
    }
  };

  const translateElementAttributes = (element: HTMLElement) => {
    const attrs = ['placeholder', 'title', 'aria-label', 'aria-description'];

    for (const attr of attrs) {
      const current = element.getAttribute(attr);
      if (current == null) continue;

      if (!elementOriginals.has(element)) {
        elementOriginals.set(element, {});
      }

      const store = elementOriginals.get(element)!;

      if (store[attr] == null && containsPersian(current)) {
        store[attr] = current;
      }

      const original = store[attr] ?? current;

      if (english) {
        if (containsPersian(original)) {
          const translated = translatePersianText(original);
          if (current !== translated) {
            element.setAttribute(attr, translated);
          }
        }
      } else if (store[attr] != null && current !== store[attr]) {
        element.setAttribute(attr, store[attr]);
      }
    }
  };

  const scan = () => {
    if (typeof document === 'undefined' || scanning) return;

    scanning = true;

    try {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
      );

      let node: Node | null;

      while ((node = walker.nextNode())) {
        translateTextNode(node as Text);
      }

      document.querySelectorAll<HTMLElement>('*').forEach(
        translateElementAttributes,
      );
    } finally {
      scanning = false;
    }
  };

  const observe = () => {
    if (!observer || typeof document === 'undefined') return;

    observer.disconnect();
    observer.observe(document.body, observerOptions);
  };

  const start = () => {
    if (typeof document === 'undefined') return;

    if (!observer) {
      observer = new MutationObserver(() => {
        // IMPORTANT: disconnect before changing the DOM so our own translations
        // cannot recursively trigger the observer.
        if (!english || scanning) return;

        observer?.disconnect();
        scan();
        observe();
      });
    }

    scan();
    observe();
  };

  return {
    setLanguage(nextLanguage: Language) {
      english = nextLanguage === 'en';

      // Translate once immediately, with the observer disconnected.
      if (observer) observer.disconnect();
      scan();
      observe();
    },
    start,
  };
}
'@

$i18nText =
    $i18nText.Substring(0, $start) +
    $safeTranslator +
    "`r`n`r`n" +
    $i18nText.Substring($end)

Set-Content -Path $i18n -Value $i18nText -Encoding UTF8

# --- Remove the splash overlay ---
# The splash is unnecessary for the dashboard and can hide the UI if the browser
# is under heavy load. Removing it makes the app always enter the actual site.
$appText = Get-Content -Raw -Encoding UTF8 $app

$splashRegex = '(?s)\s*/\* Splash \*/\s*<div\s*\r?\n\s*style=\{\{.*?\r?\n\s*\}\}\s*\r?\n\s*aria-hidden="true"\s*\r?\n\s*>\s*\r?\n\s*<Logo size=\{32\} \/>\s*\r?\n\s*</div>'

$fixedApp = [regex]::Replace($appText, $splashRegex, '', 1)

if ($fixedApp -eq $appText) {
    Write-Host "Splash block was not found; leaving App.tsx unchanged." -ForegroundColor Yellow
} else {
    Set-Content -Path $app -Value $fixedApp -Encoding UTF8
}

Write-Host ""
Write-Host "Payo runtime fix applied successfully." -ForegroundColor Green
Write-Host "Fixed: src\i18n.tsx (no self-triggering MutationObserver loop)"
Write-Host "Fixed: src\App.tsx (removed blocking splash overlay)"
Write-Host ""
Write-Host "Backups created beside the edited files."
Write-Host ""
Write-Host "Next:"
Write-Host '& "C:\Program Files\nodejs\npm.cmd" run build'
