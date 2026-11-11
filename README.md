# murphysoft.app

Stüdyo sitesi (GitHub Pages, `main` kökü, özel alan `CNAME`).

- Yasal ve destek metinlerinin TEK kaynağı `legal/<uygulama>/*.md`. HTML elle düzenlenmez: `python3 _build.py`.
- Metin değişince md'deki "Sürüm/Version" artar; mağazadaki gizlilik etiketi de aynı değişiklikte gözden geçirilir.
- Dış kaynak (yazı tipi, betik, analitik) yok.
- Birdie Smash: `/birdie-smash/` · `/support/` · `/privacy/` · `/destek/` · `/gizlilik/`.
- Coverline (Rafım) ve My Pocket Money (Harçlıklarım), 2026-11-10: aynı düzen (`/coverline/`, `/pocket-money/`; Harçlıklarım'ın gizlilik metni 6 dilde). Metnin kaynağı artık burası; uygulama repolarındaki `legal/` kopyaları ve mağaza alanları bu adreslere çevrilmeli. İletişim her yerde support@murphysoft.app.
- `sitemap.xml` `_build.py` her koştuğunda klasörlerden yeniden yazılır; `robots.txt` onu gösterir. Paylaşım görseli `assets/og.png` (1200×630), ana ekran ikonu `assets/apple-touch-icon.png`.
- Tasarım (2026-11-07): tek stil `assets/site.css` (yön A "Test kaydı"); `_build.py` el yazımı sayfaların (`index.html`, `404.html`, `birdie-smash/index.html`) `<style>` bloğunu da bu dosyadan yeniler. Stil değişince betiği koş.
- Uygulama ikonları `assets/apps/`: sahnedeki büyük ikon `<ad>-800.webp` (1024'lük asıldan; 380 pt kutuda retina ekranda
  keskin kalsın diye, yasin 2026-11-11: "websitesi bizim tezgâhımız"), küçük kullanımlar için `<ad>.png` 192 px. Kepler Drift'in ikonu yokken kodla çizilmiş yer tutucu `kepler-drift.svg`.
- Ana sayfa (2026-11-10, "Swarm"): `index.html` kendi stilini ve betiğini taşır; `_build.py` ona dokunmaz. Bir nokta sürüsü açılışta adı, kaydırdıkça sırayla her uygulamanın ikonunu (`assets/apps/`'tan okunur) oluşturur. Betik yoksa ya da "hareketi azalt" açıksa sürü kapanır, sayfa düz liste olarak gelir. Uygulama eklemek: `.panel` + durum panosu satırı + alt şerit düğmesi, üçü birden.
- Yazı tipi Urbanist (SIL OFL 1.1) `assets/fonts/urbanist-latin.woff2` olarak siteden sunulur; "dış kaynak yok" kuralı sürer. Alt sayfalar (`birdie-smash/`, `404.html`) hâlâ `site.css` ("Test defteri") stilinde.
- Mobil akıcılık (2026-11-10): hareket süreleri ve eğrileri Astryx tasarım sisteminin (Meta, MIT) varsayılan temposundan alındı; kütüphanenin kendisi (React + StyleX) siteye girmedi, "dış kaynak yok" ve tek dosya kuralı sürüyor. Yükseklikler `svh` (adres çubuğu), dokunmatik ekranda kaydırma uygulamanın üstünde durur (scroll-snap proximity), parmak sürüyü dağıtmaz (yalnız dokunuş), adres çubuğu resize'ı sürüyü yeniden kurmaz, sürü durunca çizim durur (pil).
- Dil (2026-11-10): varsayılan İngilizce `/`, Türkçe `/tr/`. `tr/index.html` elle düzenlenmez: `_build.py` içindeki `TR` çiftleriyle `index.html`'den üretilir; İngilizce metin değişince çift güncellenmezse betik durur. Türkçe ğ/ş/İ için `assets/fonts/urbanist-latin-ext.woff2` (OFL, @fontsource-variable/urbanist 5.3.0).
- Ana sayfa (2026-11-11, "Renk sahnesi", yasin: "Swarm içime sinmedi"): nokta sürüsü kalktı. Her bölüm bir ekran; zemin kaydırmayla uygulamanın rengine akar ve her sahnede uygulamanın fikrini elle deneten bir oyuncak var (Sandık çizgisi, Birdie topu, Harçlıklarım parası, Rafım fişi, Kepler sondası). Açılışta y harfi ve "Break something". İkonlar takla atmaz (denendi, profesyonel durmadı). Yazı tipi Bricolage Grotesque (OFL, @fontsource-variable 5.3.0, `assets/fonts/bricolage-*.woff2`); Urbanist kaldırıldı. Uygulama eklemek: `section.app` + `data-bg` rengi + `_build.py` içindeki `TR` çiftleri. Bu dosyanın yukarısındaki "Swarm" ve Urbanist notları tarihseldir.

## Uygulamanın içi (2026-11-11)

Her uygulama sahnesinin altında aynı renkte bir `section.look` durur: üç gerçek ekran (`assets/shots/`, 520 px WebP),
ne yaptığı (üç cümle) ve durum tablosu. Ekranlar mağaza görsellerinden küçültülür; Birdie Smash, Harçlıklarım ve
Rafım için `-en-` ve `-tr-` dosyaları vardır, `_build.py` içindeki çift yolu Türkçe sayfada değiştirir. Kepler Drift
ekranları oynanabilir prototipten alınmıştır ve sayfada öyle yazar. Durum satırı değişince (yayın, mağaza bağlantısı)
`index.html` ile `_build.py` içindeki çift birlikte güncellenir.

## Marka: logo, zemin, geçişler (2026-11-11)

- **Logo (yasin: "Kayan y"):** ayrı simge yok; yazının içindeki y 13 derece kaymış durur. Sekme ikonu ve alt sayfalar
  için y harfi yola çevrildi (`assets/mark.svg`, `_build.py` `MARKA_SVG`). Açılışta harfler yükselir, y en son kayar.
- **Zemin:** açık bölümler kemik rengi `--lg` (#f0eadc) ve mürekkep; doku harita kontur çizgileri (maske, rengi `--ldot`).
  yasin sarıyı beğenmedi (2026-11-11). Açık bölümler (`.lite`) kendi zeminini taşır, yuvarlak kenarlı bir sayfa gibi renkli
  sahnelerin üstünden kayar; üst şerit altındaki zemine göre renk değiştirir. Karşılamanın alt kenarı beş uygulamanın
  rengidir (`.spine`) ve o sahneye götürür. Renk değişkenleri `:root` içinde; zemin değişirse yalnız oradan değişir.
- **Geçişler:** sahne renkleri OKLab'da ve dar bir bantta karışır; başlık perdenin altından çıkar; ikon ve başlık
  kaydırmayla hafifçe süzülür (`--q`). Hareketi azalt açıkken hiçbiri oynamaz.
- **Sahne dekoru:** her sahnenin zemini uygulamanın dünyasından ton üstü ton çizilir (`svg.deco`): dalgalar, kort, bozuk
  paralar, raflar, yıldızlar. Katmanlar `--q` ile farklı hızda kayar. Sarı bölümlerde matbaa noktası, üstte ince kumlanma.

## Site ikonu (2026-11-11)

Kiremit zemin (`#b93a0a`) üstünde kemik rengi kayan y. Dosyalar: `favicon.ico` (16, 32, 48; kökte, çünkü tarayıcılar ve
arama motorları orada arar), `assets/mark.svg` (keskin sekme ikonu), `assets/apple-touch-icon.png` (180, köşesiz ve
saydamsız: iOS kendi yuvarlar), `assets/icon-192.png`, `icon-512.png`, `icon-maskable-512.png` ve `site.webmanifest`
(Android ana ekranı). 16 ve 32 pikselde harf biraz daha büyük çizilir ki okunur kalsın. Bağlantılar her sayfanın
başlığında; üretilen sayfalarda `_build.py` şablonundan gelir.
