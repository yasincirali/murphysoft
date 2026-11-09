"""Ana sayfa üreteci: tool/ana_sayfa.kaynak.html -> index.html (İngilizce) ve tr/index.html (Türkçe).

Çalıştırma (repo kökünden): python3 tool/ana_sayfa.py

Neden böyle (2026-11-10): iki dil tek kaynaktan çıkar ki sürü betiği ve stil iki dosyada ayrışmasın.
Metin İngilizce kaynakta değişince aşağıdaki TR tablosundaki karşılığı da değişir; eşleşmeyen satır
betiği durdurur (assert), çeviri sessizce eskimez. Kaynak bir parçadır (head yok); head burada yazılır."""
import pathlib

here = pathlib.Path(__file__).parent
src = (here / "ana_sayfa.kaynak.html").read_text(encoding="utf-8")
site = here.parent

css = src[src.index("<style>") + 7:src.index("</style>")]
body = src[src.index("</style>") + 8:]


def rep(text, a, b, n=None):
    assert a in text, a
    if n is not None:
        assert text.count(a) == n, (a, text.count(a))
    return text.replace(a, b)


# no outside requests: the face is served from the site itself
font = """/* Urbanist (SIL Open Font License 1.1), served from this site: no request leaves murphysoft.app. */
@font-face {
  font-family: "Urbanist"; font-style: normal; font-weight: 400 800; font-display: swap;
  src: url("/assets/fonts/urbanist-latin.woff2") format("woff2");
}
"""
css = font + css.lstrip("\n")
css = rep(css, "  .hero-foot { grid-template-columns: 1fr; }", "  .hero-foot { grid-template-columns: 1fr; }\n  .nav nav a.opt { display: none; }", 1)

body = rep(body, 'src="img/', 'src="/assets/apps/', 5)
body = rep(body, 'href="https://murphysoft.app/birdie-smash/privacy/"', 'href="/birdie-smash/privacy/"', 1)
body = rep(body, 'href="https://murphysoft.app/birdie-smash/"', 'href="/birdie-smash/"', 1)
body = rep(body, '<a href="#method">Method</a>', '<a class="opt" href="#method">Method</a>', 1)

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#18191b">
<meta name="description" content="{desc}">
<meta property="og:title" content="Murphysoft">
<meta property="og:description" content="{og}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://murphysoft.app{path}">
<link rel="canonical" href="https://murphysoft.app{path}">
<link rel="alternate" hreflang="en" href="https://murphysoft.app/">
<link rel="alternate" hreflang="tr" href="https://murphysoft.app/tr/">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/urbanist-latin.woff2" as="font" type="font/woff2" crossorigin>
<title>Murphysoft</title>
<!-- Ana sayfa (2026-11-10, "Swarm"): stili kendi içinde; _build.py bu dosyanın <style> bloğuna dokunmaz.
     Bu dosya elle düzenlenmez: kaynak ve Türkçe çeviri tablosu README'de anlatılan üreteçtedir (tool/ana_sayfa.py). -->
<style>
"""

TR = [
    ('<a class="skip" href="#apps">Skip to the apps</a>', '<a class="skip" href="#apps">Uygulamalara geç</a>'),
    ('<nav aria-label="Sections">', '<nav aria-label="Bölümler">'),
    ('<a href="#apps">Apps</a>', '<a href="#apps">Uygulamalar</a>'),
    ('<a class="opt" href="#method">Method</a>', '<a class="opt" href="#method">Yöntem</a>'),
    ('<a href="#contact">Contact</a>', '<a href="#contact">İletişim</a>'),
    ('<h1>Whatever can go wrong, we test first.</h1>', '<h1>Ters gidebilecek her şeyi önce biz test ederiz.</h1>'),
    ("Murphysoft is an independent studio making small games and apps. The kids’ app shows no ads, the game needs no account, and Sandık lets you delete your data. <b>Five titles, one live on the App Store and Google Play.</b>",
     "Murphysoft küçük oyunlar ve uygulamalar yapan bağımsız bir stüdyo. Çocuk uygulaması reklam göstermez, oyun hesap istemez, Sandık verini silmene izin verir. <b>Beş uygulama, biri App Store ve Google Play’de yayında.</b>"),
    ('<a class="btn" href="#apps">See the apps</a>', '<a class="btn" href="#apps">Uygulamaları gör</a>'),
    ('<a class="btn ghost" href="#contact">Write to us</a>', '<a class="btn ghost" href="#contact">Bize yaz</a>'),
    ('aria-label="Apps and their status"', 'aria-label="Uygulamalar ve durumları"'),
    ('<span class="st live">Live</span>', '<span class="st live">Yayında</span>'),
    ('<span class="st soon">Coming soon</span>', '<span class="st soon">Yakında</span>'),
    ('<span class="st dev">In development</span>', '<span class="st dev">Geliştiriliyor</span>'),
    ('<span class="st live"><span>Live</span></span>', '<span class="st live"><span>Yayında</span></span>'),
    ('<span class="st soon"><span>Coming soon</span></span>', '<span class="st soon"><span>Yakında</span></span>'),
    ('<span class="st dev"><span>In development</span></span>', '<span class="st dev"><span>Geliştiriliyor</span></span>'),
    ('<h2>Apps and games</h2>', '<h2>Uygulamalar ve oyunlar</h2>'),
    ('<span class="plat">iPhone and Android</span>', '<span class="plat">iPhone ve Android</span>'),
    ('Portfolio tracker for investors in Türkiye. Stocks, funds, gold, currencies and deposits on one screen, measured against inflation.',
     'Türkiye’deki yatırımcı için portföy takibi. Hisse, fon, altın, döviz ve mevduat tek ekranda, enflasyonla yan yana.'),
    ('>Get it on the App Store</a>', '>App Store’dan indir</a>'),
    ('>Get it on Google Play</a>', '>Google Play’den indir</a>'),
    ('Arcade badminton. Swipe to hit, time your smash, climb the career and dress your player your way. No account needed.',
     'Arcade badminton. Kaydırarak vur, smacını zamanla, kariyerde yüksel, oyuncunu dilediğin gibi giydir. Hesap gerekmez.'),
    ('>Read about Birdie Smash</a>', '>Birdie Smash’i incele</a>'),
    ('A pocket money jar for kids, looked after by four characters. No ads, no tracking, everything stays on the device.',
     'Çocuklar için harçlık kumbarası; dört karakter ona göz kulak olur. Reklam yok, takip yok, her şey cihazda kalır.'),
    ('Receipts and warranties in one place, and which of your rights still apply today: returns, legal guarantee, manufacturer warranty.',
     'Fişler ve garantiler tek yerde. Hangi hakkının bugün hâlâ geçerli olduğunu gösterir: iade, yasal garanti, üretici garantisi.'),
    ('One-finger orbit arcade. Hold to circle a planet, let go to launch, and arrive softly at the target.',
     'Tek parmakla yörünge oyunu. Basılı tutup gezegenin çevresinde dön, bırakıp fırla, hedefe yumuşakça var.'),
    ('aria-label="Choose an app"', 'aria-label="Uygulama seç"'),
    ('<h2>What happens when it goes wrong</h2>', '<h2>Ters gidince ne olur</h2>'),
    ('Murphy’s law says anything that can go wrong will. Here are six cases our apps are built to handle.',
     'Murphy yasasına göre ters gidebilecek her şey ters gider. Uygulamalarımızın hazır olduğu altı durum aşağıda.'),
    ('<th scope="col">What goes wrong</th><th scope="col">App</th><th scope="col">What happens next</th>',
     '<th scope="col">Ne ters gider</th><th scope="col">Uygulama</th><th scope="col">Sonra ne olur</th>'),
    ('A price source stops responding', 'Fiyat kaynağı yanıt vermez'),
    ('The point is left off the chart. No number is ever made up.', 'O nokta grafiğe girmez. Hiçbir sayı uydurulmaz.'),
    ('Someone signs in on another phone', 'Biri başka telefondan giriş yapar'),
    ('A code goes to your email and the old session closes.', 'E-postana kod gelir, eski oturum kapanır.'),
    ('A request fails halfway through a tap', 'İstek yarı yolda başarısız olur'),
    ('You see the reason in plain words and can try again.', 'Nedenini sade bir dille görürsün, yeniden deneyebilirsin.'),
    ('You want to leave', 'Ayrılmak istersin'),
    ('Download your data or delete the account from Settings.', 'Verini indirirsin ya da hesabını Ayarlar’dan silersin.'),
    ('You don’t want another account', 'Bir hesap daha açmak istemezsin'),
    ('No account needed. Your progress stays with you.', 'Hesap gerekmez. İlerlemen sende kalır.'),
    ('A child is holding the phone', 'Telefon bir çocuğun elindedir'),
    ('It shows no ads and tracks nothing. All data stays on the device.', 'Reklam göstermez, hiçbir şeyi takip etmez. Tüm veri cihazda kalır.'),
    ('<h2>Write to us</h2>', '<h2>Bize yaz</h2>'),
    ('Questions, bug reports or ideas for any of our apps. We read every message and usually reply within two days.',
     'Uygulamalarımızla ilgili soru, hata bildirimi ya da fikir. Her mesajı okuruz, çoğu zaman iki gün içinde yanıtlarız.'),
    ('>Copy the address</button>', '>Adresi kopyala</button>'),
    ("copy.textContent = 'Copied'", "copy.textContent = 'Kopyalandı'"),
    ("copy.textContent = 'Copy the address'", "copy.textContent = 'Adresi kopyala'"),
    ("copy.textContent = 'Selected, now copy'", "copy.textContent = 'Seçildi, şimdi kopyala'"),
    ('<nav aria-label="Legal">', '<nav aria-label="Yasal">'),
    ('<a href="/birdie-smash/privacy/">Birdie Smash privacy</a>', '<a href="/birdie-smash/gizlilik/">Birdie Smash gizlilik</a>'),
    ('<a href="https://yasincirali.github.io/sandikapp/privacy-en/">Sandık privacy</a>', '<a href="https://yasincirali.github.io/sandikapp/privacy/">Sandık gizlilik</a>'),
    ('<a href="#top">Back to top</a>', '<a href="#top">Başa dön</a>'),
]


def page(lang):
    b = body
    if lang == "tr":
        for a, t in TR:
            b = rep(b, a, t)
        b = rep(b, '</a>\n    </nav>\n  </header>', '</a>\n      <a href="/" lang="en" hreflang="en">English</a>\n    </nav>\n  </header>', 1)
        head = HEAD.format(lang="tr", path="/tr/",
                           desc="Murphysoft küçük oyunlar ve uygulamalar yapan bağımsız bir stüdyo: Sandık, Birdie Smash, My Pocket Money, Coverline ve Kepler Drift.",
                           og="Ters gidebilecek her şeyi önce biz test ederiz. Küçük oyunlar ve uygulamalar.")
        out = site / "tr" / "index.html"
    else:
        b = rep(b, '</a>\n    </nav>\n  </header>', '</a>\n      <a href="/tr/" lang="tr" hreflang="tr">Türkçe</a>\n    </nav>\n  </header>', 1)
        head = HEAD.format(lang="en", path="/",
                           desc="Murphysoft is an independent studio making small games and apps: Sandık, Birdie Smash, My Pocket Money, Coverline and Kepler Drift.",
                           og="Whatever can go wrong, we test first. Small games and apps from an independent studio.")
        out = site / "index.html"
    html = head + css + "</style>\n</head>\n<body>" + b.rstrip() + "\n</body>\n</html>\n"
    assert "fonts.googleapis" not in html and "gstatic" not in html and "cdnjs" not in html
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8", newline="\n")
    print(out.relative_to(site), len(html))


page("en")
page("tr")
