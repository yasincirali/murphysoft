# murphysoft.app

Stüdyo sitesi (GitHub Pages, `main` kökü, özel alan `CNAME`).

- Yasal ve destek metinlerinin TEK kaynağı `legal/<uygulama>/*.md`. HTML elle düzenlenmez: `python3 _build.py`.
- Metin değişince md'deki "Sürüm/Version" artar; mağazadaki gizlilik etiketi de aynı değişiklikte gözden geçirilir.
- Dış kaynak (yazı tipi, betik, analitik) yok.
- Birdie Smash: `/birdie-smash/` · `/support/` · `/privacy/` · `/destek/` · `/gizlilik/`.
- Tasarım (2026-11-07): tek stil `assets/site.css` (yön A "Test kaydı"); `_build.py` el yazımı sayfaların (`index.html`, `404.html`, `birdie-smash/index.html`) `<style>` bloğunu da bu dosyadan yeniler. Stil değişince betiği koş.
- Uygulama ikonları `assets/apps/` (1024'lük ikonlardan 192 px). Kepler Drift'in ikonu yokken kodla çizilmiş yer tutucu `kepler-drift.svg`.
