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

    sitemap_yaz()

    for yol in EL_SAYFALARI:
        dosya = ROOT / yol
        metin = dosya.read_text(encoding="utf-8")
        yeni = re.sub(r"<style>.*?</style>", lambda _: f"<style>\n{CSS}\n</style>", metin, count=1, flags=re.S)
        if yeni != metin:
            dosya.write_text(yeni, encoding="utf-8")
        print(f"{yol}: stil yenilendi")


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
