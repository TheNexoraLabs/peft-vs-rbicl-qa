# راهنمای اعمال Patch یکپارچه زمان‌سنجی Q1

این بسته جایگزین Patchهای قبلی زمان‌سنجی و QA است. Patchهای قبلی را جداگانه اعمال نکن.

## A) مقاله

1. از پروژه LaTeX فعلی یک نسخه پشتیبان بگیر.
2. فایل `article/sn-article.tex` را جایگزین فایل اصلی `sn-article.tex` کن.
3. فایل `article/figures/computational_cost_and_memory_comparison.pdf` را در پوشه `figures` پروژه جایگزین کن.
4. فعلاً فایل BibTeX و Code Availability را تغییر نده: DOI فعلی مقاله به نسخه آرشیوشده v0.1.1 اشاره می‌کند. پس از ساخت Release v0.1.2 و دریافت DOI جدید، همان بخش و مدخل BibTeX را یک‌بار به‌روزرسانی می‌کنیم.
5. در Overleaf کامپایل کامل انجام بده و جدول Computational Cost، جدول Token F1/runtime مخصوص RB-ICL، نمودار و Appendix با عنوان `Computational Measurement Conventions` را کنترل کن.

## B) GitHub محلی

مسیر محلی Repository:

`D:\Programming\AI\GitHub\peft-vs-rbicl-qa`

1. محتویات پوشه `github` داخل این ZIP را با حفظ ساختار پوشه‌ها در ریشه Repository کپی کن و فایل‌های هم‌نام را Replace کن.
2. چهار Notebook جدید در `notebooks/qa_inference_runs/` قرار می‌گیرند. این نسخه‌ها خروجی‌ها را پاک کرده‌اند، ولی Metadata زمان اجرا را حفظ می‌کنند. سلول دانلود Checkpoint از Google Drive حذف شده و مسیر مدل، CSV ورودی و خروجی با متغیرهای محیطی قابل تنظیم‌اند.
3. از PowerShell در ریشه Repository اجرا کن:

```powershell
python scripts/update_file_manifest.py
```

4. GitHub Desktop را باز کن. بررسی کن که تغییرات شامل README، CITATION.cff، PREPARATION_LOG، docs، workbook/CSVها، چهار Notebook و Manifest باشد.
5. Commit با عنوان زیر بساز:

`Align Q1 QA runtimes and computational cost records`

6. Push origin را انجام بده.

## C) Release و Zenodo

چون این Push چهار Notebook شواهد QA و جدول‌های زمان‌سنجی جدید را به Repository اضافه می‌کند، برای Snapshot آرشیوی جدید یک Release بساز:

- Tag: `v0.1.2`
- Target: `main`
- Title: `v0.1.2 – Q1 QA Timing and Computational Cost Evidence`

مخزن Zenodo را همان‌طور فعال نگه دار. پس از آرشیو موفق، Version DOI جدید را برای من بفرست. بعد از آن `CITATION.cff`، README، Code Availability و BibTeX را با DOI نسخه 0.1.2 نهایی می‌کنیم. Concept DOI همان `10.5281/zenodo.24582467` باقی می‌ماند.

## D) چه چیزی را فعلاً تغییر نده

- Release قبلی v0.1.1 و DOI آن را حذف نکن.
- Concept DOI را تغییر نده.
- Peak GPU memory را تغییر نده.
- Notebookهای اصلی آموزش LoRA/DoRA و RB-ICL را تغییر نده.
- فایل‌های خام 280-sample Q2 را برای زمان QA اصلی استفاده نکن؛ جدول اصلی زمان‌سنجی اکنون برای 300 سؤال Q1 یکسان شده است.
