from PIL import Image
from io import BytesIO

# Open the image
img = Image.open("fins_logo.png")

# Convert image to RGBA (if not already)
img = img.convert("RGBA")

# Resize to favicon standard sizes (e.g., 16x16, 32x32, 48x48)
sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]

# Save as favicon.ico
img.save("favicon.ico", format="ICO", sizes=sizes)

print("favicon.ico created successfully.")