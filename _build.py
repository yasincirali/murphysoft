"""
Site üreteci: legal/<uygulama>/<sayfa>.md -> <uygulama>/<sayfa>/index.html (GitHub Pages, main kökü).

Çalıştırma (repo kökünden): python3 _build.py

Neden böyle (2026-11-07, yasin: stüdyo alanı murphysoft.app):
- Tek kaynak md'dir; HTML elle düzenlenmez. Metin değişince md'deki "Sürüm" artar, betik koşulur, ikisi aynı commit'e girer.
  Her sayfaya kaynak md'nin sha256'sı gömülür (`kaynak-sha256`): md değişip betik koşulmadıysa fark görünür.
- Adresler klasör biçiminde (/birdie-smash/privacy/): mağazaya verilen link uzantısız ve kısa kalır.
- Dış kaynak yok (yazı tipi, betik, analitik): gizlilik sayfası okuyanın IP'sini kimseye götürmesin.
- Tasarım (2026-11-07, yön A "Test defteri"): tek stil assets/site.css. El yazımı sayfalar (EL_SAYFALARI) da
  aynı CSS'i satır içi alır: betik onların <style> bloğunu yeniler, böylece stil tek yerde değişir.
- Birdie'nin yasal metni önceden birdie-smash reposunda (legal/, docs/) duruyordu; kaynak artık burası, eski sayfalar buraya yönlenir.
"""
import hashlib
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEGAL = ROOT / "legal"

# kaynak (uygulama/sayfa.md) -> dil
DIL = {"privacy": "en", "support": "en", "gizlilik": "tr", "destek": "tr",
       # Harçlıklarım'ın mağaza dilleri (2026-11-10): metin piggy-crew/legal'den buraya taşındı.
       "datenschutz": "de", "privacidad": "es", "confidentialite": "fr", "privacidade": "pt"}

CSS = (ROOT / "assets" / "site.css").read_text(encoding="utf-8").strip()

# Elle yazılan ama stili site.css'ten gelen sayfalar.
# index.html listede YOK (2026-11-10): ana sayfa "Swarm" tasarımına geçti, stili kendi içinde;
# buraya geri eklenirse betik o stili site.css ile ezer.
EL_SAYFALARI = ["404.html", "birdie-smash/index.html", "coverline/index.html", "pocket-money/index.html"]

MARKA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5" fill="none" '
             'stroke="currentColor" stroke-width="2"/><path d="M7.5 12.5l3 3 6-7" fill="none" stroke="currentColor" '
             'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# Uygulama klasörü -> görünen ad (yasal sayfanın üst şeridinde uygulama sayfasına dönüş).
# coverline ve pocket-money (2026-11-10): mağazadaki gizlilik bağlantısı GitHub dosyasıydı (Rafım) ya da hiç yoktu
# (Harçlıklarım, Kids kategorisinde zorunlu); metin buraya taşındı, iletişim support@murphysoft.app oldu.
UYGULAMA_ADI = {"birdie-smash": "Birdie Smash", "coverline": "Coverline", "pocket-money": "My Pocket Money"}


def satir_ici(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', s)
    s = re.sub(r'(?<![\w.:/"])([\w.+-]+@murphysoft\.app)', r'<a href="mailto:\1">\1</a>', s)
    return s


def donustur(md: str):
    baslik, parcalar, paragraf, liste = "", [], [], []
    sirali = False  # "1. " ile başlayan liste <ol> olur (Rafım/Harçlıklarım metinleri numaralı).

    def bosalt():
        if paragraf:
            metin = " ".join(paragraf)
            sinif = ' class="surum"' if re.match(r"^(Sürüm|Version|Versión|Versão)\b", metin) else ""
            parcalar.append(f"<p{sinif}>{satir_ici(metin)}</p>")
            paragraf.clear()
        if liste:
            etiket = "ol" if sirali else "ul"
            parcalar.append(f"<{etiket}>" + "".join(f"<li>{satir_ici(x)}</li>" for x in liste) + f"</{etiket}>")
            liste.clear()

    for satir in md.splitlines():
        t = satir.strip()
        if not t:
            bosalt()
        elif t.startswith("# "):
            bosalt(); baslik = t[2:].strip(); parcalar.append(f"<h1>{satir_ici(baslik)}</h1>")
        elif t.startswith("## "):
            bosalt(); parcalar.append(f"<h2>{satir_ici(t[3:].strip())}</h2>")
        elif t.startswith("- ") or re.match(r"^\d+\. ", t):
            yeni_sirali = not t.startswith("- ")
            if paragraf or (liste and yeni_sirali != sirali): bosalt()
            sirali = yeni_sirali
            liste.append(re.sub(r"^(- |\d+\. )", "", t).strip())
        elif liste:
            liste[-1] += " " + t
        else:
            paragraf.append(t)
    bosalt()
    return baslik, "\n".join(parcalar)


def main() -> None:
    for kaynak in sorted(LEGAL.glob("*/*.md")):
        uyg, sayfa = kaynak.parent.name, kaynak.stem
        md = kaynak.read_text(encoding="utf-8").lstrip("﻿").replace("\r\n", "\n").rstrip() + "\n"
        ozet = hashlib.sha256(md.encode("utf-8")).hexdigest()
        baslik, govde = donustur(md)
        dil = DIL.get(sayfa, "en")
        ad = UYGULAMA_ADI.get(uyg, uyg)
        cikti = ROOT / uyg / sayfa / "index.html"
        cikti.parent.mkdir(parents=True, exist_ok=True)
        cikti.write_text(f"""<!doctype html>
<html lang="{dil}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="kaynak-sha256" content="{ozet}">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="canonical" href="https://murphysoft.app/{uyg}/{sayfa}/">
<title>{html.escape(baslik)} · Murphysoft</title>
<style>
{CSS}
</style>
</head>
<body>
<!-- legal/{uyg}/{sayfa}.md kaynağından _build.py ile üretildi; elle düzenleme. -->
<header class="ust kap"><a href="/" class="marka" aria-label="Murphysoft home">{MARKA_SVG}<span>Murphysoft</span></a><nav aria-label="Site"><a href="/{uyg}/">{html.escape(ad)}</a></nav></header>
<main class="kap metin">
{govde}
</main>
<footer class="kap">© 2026 Murphysoft · <a href="mailto:support@murphysoft.app">support@murphysoft.app</a></footer>
</body>
</html>
""", encoding="utf-8")
        print(f"{kaynak.relative_to(ROOT)} -> {cikti.relative_to(ROOT)} ({ozet[:12]})")

    ana_sayfa_tr()
    sitemap_yaz()

    for yol in EL_SAYFALARI:
        dosya = ROOT / yol
        metin = dosya.read_text(encoding="utf-8")
        yeni = re.sub(r"<style>.*?</style>", lambda _: f"<style>\n{CSS}\n</style>", metin, count=1, flags=re.S)
        if yeni != metin:
            dosya.write_text(yeni, encoding="utf-8")
        print(f"{yol}: stil yenilendi")


# Ana sayfanın Türkçesi (yasin 2026-11-10: "dil seçeneği olsun, default en"). Kaynak index.html'dir; /tr/index.html
# aşağıdaki çiftlerle ondan üretilir, elle düzenlenmez. Her çift kaynakta bulunmak ZORUNDA: İngilizce metin
# değişip çevirisi unutulursa betik burada durur, yarı çevrilmiş sayfa yayına çıkmaz. Sıra önemli (uzun önce).
TR = [
    ('<html lang="en">', '<html lang="tr">'),
    ('content="Murphysoft is an independent studio making small games and apps: Sandık, Birdie Smash, My Pocket Money, Coverline and Kepler Drift."',
     'content="Murphysoft küçük oyunlar ve uygulamalar yapan bağımsız bir stüdyodur: Sandık, Birdie Smash, Harçlıklarım, Rafım ve Kepler Drift."'),
    ('content="Whatever can go wrong, we test first. Small games and apps that respect your time and your privacy."',
     'content="Ters gidebilecek ne varsa önce biz deneriz. Zamanına ve gizliliğine saygılı küçük oyunlar ve uygulamalar."'),
    ('<meta property="og:url" content="https://murphysoft.app/">', '<meta property="og:url" content="https://murphysoft.app/tr/">'),
    ('content="Murphysoft wordmark with the icons of its five apps"', 'content="Murphysoft yazısı ve beş uygulamasının ikonları"'),
    ('<link rel="canonical" href="https://murphysoft.app/">', '<link rel="canonical" href="https://murphysoft.app/tr/">'),
    ('<a class="skip" href="#sandik">Skip to the apps</a>',
     '<a class="skip" href="#sandik">Uygulamalara geç</a>'),
    ('<a class="lang" href="/tr/" lang="tr" hreflang="tr" aria-label="Türkçe">TR</a>',
     '<a class="lang" href="/" lang="en" hreflang="en" aria-label="English">EN</a>'),
    ('<h1>Whatever can go wrong, we test first.</h1>',
     '<h1>Ters gidebilecek ne varsa önce biz deneriz.</h1>'),
    ('An independent studio making small games and apps that respect your time and your privacy.',
     'Zamanına ve gizliliğine saygılı küçük oyunlar ve uygulamalar yapan bağımsız bir stüdyo.'),
    ('The y has slipped. Tap it to fix it.',
     'y harfi yerinden oynamış. Dokun, düzelt.'),
    ('>See the apps</a>',
     '>Uygulamaları gör</a>'),
    ('type="button">Break something</button>',
     'type="button">Bir şeyi boz</button>'),
    ('aria-label="Sandık icon"',
     'aria-label="Sandık ikonu"'),
    ('Live · iPhone and Android',
     'Yayında · iPhone ve Android'),
    ('Your whole portfolio on one screen. Stocks, funds, gold and currencies in Türkiye, measured against inflation.',
     'Bütün portföyün tek ekranda. Hisse, fon, altın ve döviz; enflasyona karşı ölçülür.'),
    ('As you scroll, the solid line is the portfolio, <b>the dotted line is inflation</b>.',
     'Kaydırdıkça çizilen düz çizgi portföy, <b>noktalı çizgi enflasyon</b>.'),
    ('aria-label="Birdie Smash icon: tap to hit the shuttle"',
     'aria-label="Birdie Smash ikonu: dokun, topa vur"'),
    ('Coming soon · iPhone',
     'Yakında · iPhone'),
    ('Arcade badminton. Swipe to hit, time your smash and climb the career. No account needed.',
     'Arcade badminton. Kaydırarak vur, smacı zamanla, kariyerde yüksel. Hesap gerekmez.'),
    ('Tap the icon to hit the shuttle.',
     'İkona dokun, topa vur.'),
    ('href="/birdie-smash/">About Birdie Smash</a>',
     'href="/birdie-smash/">Birdie Smash sayfası</a>'),
    ('aria-label="My Pocket Money icon: tap to drop a coin in"',
     'aria-label="Harçlıklarım ikonu: dokun, kumbaraya para at"'),
    ('In development · iPhone',
     'Geliştiriliyor · iPhone'),
    ('<h2>My Pocket Money</h2>',
     '<h2>Harçlıklarım</h2>'),
    ('A piggy bank for kids aged 7 to 15. Four characters grow with their savings. No ads, no tracking.',
     '7–15 yaş çocuklar için kumbara. Dört karakter birikimle birlikte büyür. Reklam yok, takip yok.'),
    ('Tap the jar to drop a coin in.',
     'Kumbaraya dokun, para at.'),
    ('href="/pocket-money/">Support and privacy</a>',
     'href="/pocket-money/">Destek ve gizlilik</a>'),
    ('<div><span>COVERLINE</span><span>RECEIPT</span></div>',
     '<div><span>RAFIM</span><span>FİŞ</span></div>'),
    ('<span>Data collected</span>',
     '<span>Toplanan veri</span>'),
    ('<span>Ads</span>',
     '<span>Reklam</span>'),
    ('<span>Tracking</span>',
     '<span>Takip</span>'),
    ('<span>Account</span><span>none</span>',
     '<span>Hesap</span><span>yok</span>'),
    ('<span>Server</span><span>none</span>',
     '<span>Sunucu</span><span>yok</span>'),
    ('<span>TOTAL</span><span>0.00</span>',
     '<span>TOPLAM</span><span>0,00</span>'),
    ('aria-label="Coverline icon"',
     'aria-label="Rafım ikonu"'),
    ('<h2>Coverline</h2>',
     '<h2>Rafım</h2>'),
    ('Receipts and warranties in one place. See which of your rights still apply today.',
     'Fişler ve garantiler tek yerde. Hangi hakkının bugün hâlâ geçerli olduğunu gör.'),
    ('The receipt prints as you scroll. <b>Everything we take from you adds up to zero.</b>',
     'Kaydırdıkça fiş uzar. <b>Bizden aldığın her şey sıfır.</b>'),
    ('href="/coverline/">Support and privacy</a>',
     'href="/coverline/">Destek ve gizlilik</a>'),
    ('aria-label="Kepler Drift icon: hold to orbit, release to launch"',
     'aria-label="Kepler Drift ikonu: basılı tut, yörüngede dön; bırak, fırlat"'),
    ('One-finger orbit arcade. Hold to circle a planet, let go to launch, land softly.',
     'Tek parmakla yörünge oyunu. Basılı tut, gezegenin çevresinde dön; bırak, fırla; yumuşak in.'),
    ('Hold the planet, then let go.',
     'Gezegene basılı tut, sonra bırak.'),
    ('<h2>What happens when it goes wrong</h2>',
     '<h2>İşler ters gidince ne olur</h2>'),
    ('A price source stops responding',
     'Fiyat kaynağı yanıt vermez'),
    ('Sandık leaves that point off the chart. No number is ever made up.',
     'Sandık o noktayı grafiğe koymaz. Hiçbir sayı uydurulmaz.'),
    ('Someone signs in on another phone',
     'Biri başka telefondan giriş yapar'),
    ('Sandık sends a code to your email and the old session closes.',
     'Sandık e-postana bir kod yollar, eski oturum kapanır.'),
    ('You don’t want another account',
     'Bir hesap daha açmak istemezsin'),
    ('Birdie Smash needs no account. Your progress stays with you.',
     'Birdie Smash hesap istemez. İlerlemen sende kalır.'),
    ('A child is holding the phone',
     'Telefon bir çocuğun elinde'),
    ('My Pocket Money shows no ads and tracks nothing.',
     'Harçlıklarım reklam göstermez, hiçbir şeyi takip etmez.'),
    ('<h2>Write to us</h2>',
     '<h2>Bize yaz</h2>'),
    ('Questions, bug reports or ideas for any of our apps. We read every message and usually reply within two days.',
     'Uygulamalarımızla ilgili soru, hata bildirimi ya da fikir. Her mesajı okuruz, genellikle iki gün içinde yanıtlarız.'),
    ('type="button">Copy the address</button>',
     'type="button">Adresi kopyala</button>'),
    ('<nav aria-label="Legal">',
     '<nav aria-label="Yasal">'),
    ('<a href="https://yasincirali.github.io/sandikapp/privacy-en/">Sandık privacy</a>',
     '<a href="https://yasincirali.github.io/sandikapp/privacy/">Sandık gizlilik</a>'),
    ('<a href="/birdie-smash/privacy/">Birdie Smash privacy</a>',
     '<a href="/birdie-smash/gizlilik/">Birdie Smash gizlilik</a>'),
    ('<a href="/pocket-money/privacy/">My Pocket Money privacy</a>',
     '<a href="/pocket-money/gizlilik/">Harçlıklarım gizlilik</a>'),
    ('<a href="/coverline/privacy/">Coverline privacy</a>',
     '<a href="/coverline/gizlilik/">Rafım gizlilik</a>'),
    ("out.textContent = 'Rally ' + n;",
     "out.textContent = 'Ralli ' + n;"),
    ("out.textContent = 'Coins in the jar: ' + sum;",
     "out.textContent = 'Kumbaradaki para: ' + sum;"),
    ("out.textContent = laps + (laps === 1 ? ' orbit' : ' orbits');",
     "out.textContent = laps + ' tur';"),
    ("out.textContent = laps ? laps + (laps === 1 ? ' orbit, launched' : ' orbits, launched') : 'Launched';",
     "out.textContent = laps ? laps + ' tur, fırlatıldı' : 'Fırlatıldı';"),
    ("s.setAttribute('aria-label', 'Fix the letter y');",
     "s.setAttribute('aria-label', 'y harfini düzelt');"),
    ("hint.textContent = 'Fixed. We had tested that first.';",
     "hint.textContent = 'Düzeldi. Önce biz denemiştik.';"),
    ("hint.textContent = 'Reduce Motion is on, so nothing fell. We tested that too.';",
     "hint.textContent = 'Hareketi azalt açık: hiçbir şey düşmedi. Bunu da denedik.';"),
    ("hint.textContent = 'Everything is falling.';",
     "hint.textContent = 'Her şey düşüyor.';"),
    ("hint.textContent = 'Putting it back.';",
     "hint.textContent = 'Toplanıyor.';"),
    ("hint.textContent = 'Tested. It works.';",
     "hint.textContent = 'Denedik. Çalışıyor.';"),
    ("brk.textContent = 'Break it again';",
     "brk.textContent = 'Bir daha boz';"),
    ("copy.textContent = 'Copied';",
     "copy.textContent = 'Kopyalandı';"),
    ("copy.textContent = 'Copy the address';",
     "copy.textContent = 'Adresi kopyala';"),
    ("copy.textContent = 'Selected, now copy';",
     "copy.textContent = 'Seçildi, şimdi kopyala';"),
]


def ana_sayfa_tr() -> None:
    kaynak = (ROOT / "index.html").read_text(encoding="utf-8")
    for en, tr in TR:
        if en not in kaynak:
            raise SystemExit(f"tr/index.html: kaynakta bulunamadı, çeviri çiftini güncelle: {en[:70]!r}")
        kaynak = kaynak.replace(en, tr)
    cikti = ROOT / "tr" / "index.html"
    cikti.parent.mkdir(exist_ok=True)
    cikti.write_text(kaynak.replace("<body>", "<body>\n<!-- index.html kaynağından _build.py ile üretildi; elle düzenleme. -->", 1), encoding="utf-8")
    print("index.html -> tr/index.html")


def sitemap_yaz() -> None:
    """sitemap.xml her koşuda klasörlerden yeniden yazılır (2026-11-10): yeni uygulama ya da dil eklenince elle
    güncellemeyi unutmak mümkün olmasın. 404 ve eski yönlendirme sayfaları (noindex) girmez."""
    sayfalar = ["/"]
    for dosya in sorted(ROOT.glob("*/**/index.html")):
        rel = dosya.parent.relative_to(ROOT).as_posix()
        if rel.startswith(("assets", "legal", ".")) or 'name="robots" content="noindex' in dosya.read_text(encoding="utf-8"):
            continue
        sayfalar.append(f"/{rel}/")
    satirlar = "".join(f"  <url><loc>https://murphysoft.app{s}</loc></url>\n" for s in sayfalar)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + satirlar + "</urlset>\n", encoding="utf-8")
    print(f"sitemap.xml: {len(sayfalar)} adres")


if __name__ == "__main__":
    main()
