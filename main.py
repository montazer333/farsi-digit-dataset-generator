import os
import random
from PIL import Image, ImageDraw, ImageFont

numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
fonts_path = "./fonts/"  
output_path = "./farsi_digits_dataset/"
image_size = (32, 32)   
samples_per_digit = 1000 
# ایجاد پوشه اصلی خروجی
if not os.path.exists(output_path):
    os.makedirs(output_path)

# لیست کردن تمام فونت‌های موجود در پوشه
try:
    fonts = [os.path.join(fonts_path, f) for f in os.listdir(fonts_path) if f.endswith(('.ttf', '.otf'))]
    if not fonts:
        raise FileNotFoundError("هیچ فایلی با پسوند .ttf در پوشه فونت پیدا نشد.")
except Exception as e:
    print(f"Error: {e}")
    fonts = []

if fonts:
    print(f"شروع ساخت دیتاست با {len(fonts)} فونت مختلف...")
    
    for idx, num in enumerate(numbers):
        # ایجاد پوشه اختصاصی برای هر عدد (از 0 تا 9)
        label_path = os.path.join(output_path, str(idx))
        os.makedirs(label_path, exist_ok=True)
        
        for i in range(samples_per_digit):
            # ایجاد یک تصویر سیاه (L برای تصاویر سیاه و سفید / RGB برای رنگی)
            img = Image.new('L', image_size, color=0)
            draw = ImageDraw.Draw(img)
            
            # انتخاب فونت و اندازه تصادفی برای تنوع بخشیدن به دیتاست
            font_file = random.choice(fonts)
            font_size = random.randint(35, 50)
            font = ImageFont.truetype(font_file, font_size)
            
            # محاسبه مرکز تصویر با استفاده از متد جدید textbbox
            left, top, right, bottom = draw.textbbox((0, 0), num, font=font)
            text_w = right - left
            text_h = bottom - top
            

            pos_x = (image_size[0] - text_w) // 2 - left + random.randint(-4, 4)
            pos_y = (image_size[1] - text_h) // 2 - top + random.randint(-4, 4)
            
            # رسم عدد روی تصویر
            draw.text((pos_x, pos_y), num, fill=255, font=font)
            
            # اعمال چرخش تصادفی به تصویر
            img = img.rotate(random.randint(-15, 15))
            
            # ذخیره نهایی
            img.save(os.path.join(label_path, f"digit_{idx}_sample_{i}.png"))
        
        print(f"تصاویر عدد {num} ساخته شد.")

    print(f"\nعملیات با موفقیت تمام شد. تصاویر در پوشه {output_path} ذخیره شدند.")
else:
    print("عملیات متوقف شد چون فونتی یافت نشد.")