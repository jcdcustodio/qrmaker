from PIL import Image
import segno

import io
import os
import sys


def make_qr(url, is_micro=False):
    qr = segno.make(url, error="H", micro=is_micro)
    return qr


def export_qr(filename, qr, scale_size=1, border_size=4, fg_color=None, bg_color=None):
    set_dark = "#000000" if not fg_color else fg_color
    set_light = bg_color if bg_color else None

    qr.save(f"{filename}.svg", scale=scale_size, border=border_size, dark=set_dark, light=set_light)
    qr.save(f"{filename}.png", scale=scale_size, border=border_size, dark=set_dark, light=set_light)


def export_qr_logo(filename, qr, scale_size=1, border_size=4):
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer, kind="png", scale=scale_size, border=border_size, light=None)

    qr_buffer.seek(0)
    qr_img = Image.open(qr_buffer)

    qr_img_width, qr_img_height = qr_img.size
    container_size = min(qr_img_width, qr_img_height) // 4
    container_shape = ((qr_img_width - container_size) // 2, (qr_img_height - container_size) // 2)
    
    logo_container = Image.new("RGB", (container_size, container_size), "white")
    qr_img.paste(logo_container, container_shape)

    qr_img.save(f"{filename}-logo.png")


if __name__ == "__main__":
    defaultname = ("qrout", "qrout-logo")
    if not os.path.exists("qrcodes/"):
        os.makedirs("qrcodes/")

    if len(sys.argv) < 2:
        print(f"Usage: {__file__} [url/str] Optional[filename] Optional[filename_logo]")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("Warning: Excessive input arguments found. Default file names will be used.")

    filename, filename_logo = defaultname
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    if len(sys.argv) == 4:
        filename, filename_logo = sys.argv[2], sys.argv[3]
        
    qr = make_qr(sys.argv[1])
    export_qr(f"qrcodes/{filename}", qr, scale_size=15, border_size=3)
    export_qr_logo(f"qrcodes/{filename_logo}", qr, scale_size=15, border_size=3)

