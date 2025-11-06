from PIL import Image, ImageOps

# Open the original logo
img = Image.open('logo-icon.png')

# Convert to RGBA if not already
img = img.convert('RGBA')

# Split into channels
r, g, b, a = img.split()

# Invert RGB channels (not alpha)
r = ImageOps.invert(r)
g = ImageOps.invert(g)
b = ImageOps.invert(b)

# Merge back
negative = Image.merge('RGBA', (r, g, b, a))

# Save
negative.save('logo-icon-negative.png')
print("Negative logo created: logo-icon-negative.png")
