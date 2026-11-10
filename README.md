# murphysoft.app

Stüdyo sitesi (GitHub Pages, `main` kökü, özel alan `CNAME`).

- Yasal ve destek metinlerinin TEK kaynağı `legal/<uygulama>/*.md`. HTML elle düzenlenmez: `python3 _build.py`.
- Metin değişince md'deki "Sürüm/Version" artar; mağazadaki gizlilik etiketi de aynı değişiklikte gözden geçirilir.
- Dış kaynak (yazı tipi, betik, analitik) yok.
- Birdie Smash: `/birdie-smash/` · `/support/` · `/privacy/` · `/destek/` · `/gizlilik/`.
- Coverline (Rafım) ve My Pocket Money (Harçlıklarım), 2026-11-10: aynı düzen (`/coverline/`, `/pocket-money/`; Harçlıklarım'ın gizlilik metni 6 dilde). Metnin kaynağı artık burası; uygulama repolarındaki `legal/` kopyaları ve mağaza alanları bu adreslere çevrilmeli. İletişim her yerde support@murphysoft.app.
- `sitemap.xml` `_build.py` her koştuğunda klasörlerden yeniden yazılır; `robots.txt` onu gösterir. Paylaşım görseli `assets/og.png` (1200×630), ana ekran ikonu `assets/apple-touch-icon.png`.
- Tasarım (2026-11-07): tek stil `assets/site.css` (yön A "Test kaydı"); `_build.py` el yazımı sayfaların (`index.html`, `404.html`, `birdie-smash/index.html`) `<style>` bloğunu da bu dosyadan yeniler. Stil değişince betiği koş.
- Uygulama ikonları `assets/apps/` (1024'lük ikonlardan 192 px). Kepler Drift'in ikonu yokken kodla çizilmiş yer tutucu `kepler-drift.svg`.
- Ana sayfa (2026-11-10, "Swarm"): `index.html` kendi stilini ve betiğini taşır; `_build.py` ona dokunmaz. Bir nokta sürüsü açılışta adı, kaydırdıkça sırayla her uygulamanın ikonunu (`assets/apps/`'tan okunur) oluşturur. Betik yoksa ya da "hareketi azalt" açıksa sürü kapanır, sayfa düz liste olarak gelir. Uygulama eklemek: `.panel` + durum panosu satırı + alt şerit düğmesi, üçü birden.
- Yazı tipi Urbanist (SIL OFL 1.1) `assets/fonts/urbanist-latin.woff2` olarak siteden sunulur; "dış kaynak yok" kuralı sürer. Alt sayfalar (`birdie-smash/`, `404.html`) hâlâ `site.css` ("Test defteri") stilinde.
- Mobil akıcılık (2026-11-10): hareket süreleri ve eğrileri Astryx tasarım sisteminin (Meta, MIT) varsayılan temposundan alındı; kütüphanenin kendisi (React + StyleX) siteye girmedi, "dış kaynak yok" ve tek dosya kuralı sürüyor. Yükseklikler `svh` (adres çubuğu), dokunmatik ekranda kaydırma uygulamanın üstünde durur (scroll-snap proximity), parmak sürüyü dağıtmaz (yalnız dokunuş), adres çubuğu resize'ı sürüyü yeniden kurmaz, sürü durunca çizim durur (pil).
