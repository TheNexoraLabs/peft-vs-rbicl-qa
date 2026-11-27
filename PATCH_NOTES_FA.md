# یادداشت Patch یکپارچه Q1

- چهار Notebook موجود در `loader-llamas.rar` دقیقاً به DoRA، DoRA+DeepSeek، LoRA و LoRA+DeepSeek نگاشت شدند.
- هر Notebook دقیقاً 300 پاسخ داشت، صفر پاسخ خالی داشت و 300/300 پاسخ آن با CSV مخصوص همان مدل در Q1 به‌صورت ردیف‌به‌ردیف برابر بود.
- زمان QA هر شش سیستم از Metadata اجرای سلول حاوی حلقه 300 سؤالی استخراج شد؛ برای RB-ICL، تایمر داخلی time.time() نیز با اختلاف کمتر از 0.30 ثانیه آن را تأیید می‌کند.
- جدول مقاله، جدول RB-ICL، پاراگراف نتیجه‌گیری زمان و توضیحات Appendix اصلاح شدند.
- زمان‌های Training از GPU-calculator code timers گرفته شدند.
- Full Run Allها همچنان در مستندات و workbook جدا هستند و با زمان QA loop مخلوط نشده‌اند.
- چهار Notebook عمومی QA outputs را پاک کرده و سلول لینک خصوصی Google Drive در آن‌ها حذف شده است.
- `computational_cost_table.xlsx` و CSVهای زمان‌سنجی بازسازی شده‌اند.
- DOI v0.1.1 همچنان معتبر است؛ برای snapshot جدید باید Release v0.1.2 و Version DOI جدید ایجاد شود.
