#!/usr/bin/env python3
"""
ساخت «گزارش بازبینی و ارتقای فریم‌ور دستگاه ردیاب» در سیستم طراحی آتی فرزام.

هر صفحه یک قطعهٔ HTML در پوشهٔ pages/ است (به ترتیب نام فایل). این اسکریپت
هدر، فوتر، شمارهٔ صفحه (با اعداد فارسی) و پوستهٔ سند را از روی قالب رسمی
brand-kit/templates/report-template.html می‌سازد و خروجی را در ریشهٔ مخزن
با نام firmware-report.html می‌نویسد.

اجرا:  python3 reports/firmware/build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "firmware-report.html"

DOC_CODE = "AF-FWR-1405-01"
DOC_VER = "۱٫۰"
DOC_DATE = "مهر ۱۴۰۵"
TITLE = "گزارش بازبینی و ارتقای فریم‌ور دستگاه ردیاب"
CLASSIF = "محرمانه ـ ویژهٔ کارفرما"

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(n: int, width: int = 2) -> str:
    return str(n).zfill(width).translate(FA)


HEADER = f"""  <header class="a4-header">
    <div class="a4-header-brand">
      <img src="svg/logo%20ati%20farzam.svg" alt="" class="a4-header-logo" />
      <img src="svg/typography%20ati%20farzam.svg" alt="آتی فرزام" class="a4-header-typo" />
      <span class="a4-header-divider"></span>
      <div><div class="a4-header-title">{TITLE}</div><div class="a4-header-subtitle">آتی فرزام ـ مهندسی فریم‌ور و سخت‌افزار ردیاب</div></div>
    </div>
    <div class="a4-header-meta"><span>سند <b class="af-ltr">{DOC_CODE}</b></span><i>|</i><span>نسخهٔ <b>{DOC_VER}</b></span><i>|</i><span><b>{DOC_DATE}</b></span></div>
  </header>
"""


def footer(n: int, total: int) -> str:
    return f"""  <footer class="a4-footer">
    <span>آتی فرزام ـ توسعهٔ نرم‌افزار و سخت‌افزار ردیاب</span>
    <span class="dots3"><i></i><i></i><i></i></span>
    <span>{CLASSIF}</span>
    <span class="a4-footer-left"><img class="a4-footer-en" src="svg/typography%20english.svg" alt="Ati Farzam" /><span class="a4-footer-page">{fa(n)} / {fa(total)}</span></span>
  </footer>
"""


HEAD = (HERE / "head.html").read_text(encoding="utf-8")
TAIL = "\n</main>\n</body>\n</html>\n"


def main() -> None:
    files = sorted((HERE / "pages").glob("*.html"))
    total = len(files)
    out = [HEAD.replace("{{TOTAL}}", fa(total, 1))]
    for i, f in enumerate(files, start=1):
        body = f.read_text(encoding="utf-8").strip("\n")
        body = body.replace("{{TOTAL}}", fa(total, 1))
        if f.name.startswith("00-cover"):
            out.append(f"\n<!-- ══════════ صفحهٔ {fa(i, 1)} — جلد ══════════ -->\n"
                       f'<section class="a4-page a4-cover">\n{body}\n</section>\n')
            continue
        out.append(f"\n<!-- ══════════ صفحهٔ {fa(i, 1)} — {f.stem} ══════════ -->\n"
                   f'<section class="a4-page">\n{HEADER}\n{body}\n\n{footer(i, total)}</section>\n')
    out.append(TAIL)
    OUT.write_text("".join(out), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} — {total} pages")


if __name__ == "__main__":
    main()
