import math
from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    # Create high-res image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded rectangle background with romantic gradient
    corner_radius = int(size * 0.22)
    
    # Base background (Rose-wine romantic warm gradient)
    for y in range(size):
        interp = y / size
        # From #FFF2F4 to #FDE2E4
        r = int(255 - interp * 45)
        g = int(240 - interp * 65)
        b = int(243 - interp * 50)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Mask for rounded corners (iOS icon mask)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, size, size], corner_radius, fill=255)
    
    # Outer subtle gold/rose border
    final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    final_img.paste(img, (0, 0), mask=mask)
    draw = ImageDraw.Draw(final_img)
    draw.rounded_rectangle([2, 2, size - 3, size - 3], corner_radius, outline=(232, 165, 152, 200), width=max(2, size // 64))

    # Inner glow / vignette
    center_x, center_y = size // 2, int(size * 0.54)
    jar_w = int(size * 0.44)
    jar_h = int(size * 0.52)

    # Glow behind jar
    glow_radius = int(size * 0.35)
    for r in range(glow_radius, 0, -2):
        alpha = int((1 - r / glow_radius) * 45)
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(244, 196, 48, alpha))

    # Cork Stopper
    cork_w = int(jar_w * 0.58)
    cork_h = int(size * 0.08)
    cork_y = center_y - jar_h // 2 - cork_h + int(size * 0.02)
    cork_box = [center_x - cork_w // 2, cork_y, center_x + cork_w // 2, cork_y + cork_h]
    draw.rounded_rectangle(cork_box, radius=max(3, size // 40), fill=(180, 125, 80, 255), outline=(130, 85, 45, 255), width=max(1, size // 100))

    # Red ribbon on jar neck
    ribbon_w = int(jar_w * 0.68)
    ribbon_h = max(3, int(size * 0.025))
    ribbon_y = cork_y + cork_h - 2
    draw.rounded_rectangle([center_x - ribbon_w // 2, ribbon_y, center_x + ribbon_w // 2, ribbon_y + ribbon_h], radius=2, fill=(170, 45, 70, 255))

    # Jar Body (glass)
    jar_box = [center_x - jar_w // 2, center_y - jar_h // 2 + int(size * 0.04), center_x + jar_w // 2, center_y + jar_h // 2]
    jar_radius = int(jar_w * 0.28)
    
    # Glass fill
    draw.rounded_rectangle(jar_box, radius=jar_radius, fill=(255, 255, 255, 110), outline=(255, 255, 255, 230), width=max(2, size // 70))
    # Inner glass shadow/depth
    draw.rounded_rectangle([jar_box[0] + 4, jar_box[1] + 4, jar_box[2] - 4, jar_box[3] - 4], radius=jar_radius - 2, outline=(232, 165, 152, 90), width=max(1, size // 120))

    # Glass highlight reflection
    hl_x = jar_box[0] + int(jar_w * 0.12)
    hl_y = jar_box[1] + int(jar_h * 0.15)
    hl_w = max(2, int(size * 0.025))
    hl_h = int(jar_h * 0.55)
    draw.rounded_rectangle([hl_x, hl_y, hl_x + hl_w, hl_y + hl_h], radius=hl_w // 2, fill=(255, 255, 255, 200))

    # Hearts inside jar
    # Main glowing red/rose heart in center
    def draw_heart(cx, cy, h_size, color):
        points = []
        for t in range(0, 360, 5):
            rad = math.radians(t)
            # Parametric equation of a heart
            x = 16 * (math.sin(rad) ** 3)
            y = -(13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad))
            px = cx + (x * h_size / 16)
            py = cy + (y * h_size / 16)
            points.append((px, py))
        draw.polygon(points, fill=color)

    # Glowing main heart
    draw_heart(center_x, center_y + int(size * 0.02), size * 0.14, (225, 29, 72, 230))
    # Small floating hearts
    draw_heart(center_x - int(jar_w * 0.2), center_y + int(jar_h * 0.2), size * 0.07, (244, 114, 182, 200))
    draw_heart(center_x + int(jar_w * 0.22), center_y - int(jar_h * 0.1), size * 0.06, (251, 146, 60, 200))

    # Fairy light sparkles
    sparkles = [
        (center_x - int(jar_w * 0.18), center_y - int(jar_h * 0.15), size * 0.018),
        (center_x + int(jar_w * 0.16), center_y + int(jar_h * 0.18), size * 0.022),
        (center_x, center_y - int(jar_h * 0.22), size * 0.015),
    ]
    for sx, sy, sr in sparkles:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 235, 120, 255))

    final_img.save(filename, 'PNG')
    print(f"Generated {filename} ({size}x{size})")

create_icon(180, 'apple-touch-icon.png')
create_icon(192, 'icon-192.png')
create_icon(512, 'icon-512.png')
