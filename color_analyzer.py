import sys
import os
import colorsys
from collections import Counter
from PIL import Image
import matplotlib
# Use Agg backend for headless environments (prevents GUI window popup issues)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def classify_hsv_advanced(h, s, v):
    """
    Classify a pixel into one of 11 categories based on HSV values.
    h: Hue in range [0, 360)
    s: Saturation in range [0, 1]
    v: Value in range [0, 1]
    """
    # 1. Achromatic checks
    if s < 0.08 and v >= 0.85:
        return "White"
    elif v < 0.15:
        return "Black"
    elif s < 0.15 and 0.15 <= v < 0.85:
        return "Gray"
    
    # 2. Chromatic checks (H in range 0 to 360)
    # Red Range
    if h < 15 or h >= 345:
        return "Red"
    
    # Orange Range
    elif 15 <= h < 35:
        if v < 0.55:
            return "Brown"
        return "Orange"
        
    # Yellow Range
    elif 35 <= h < 65:
        if v < 0.50 or s < 0.30:
            return "Brown"
        return "Yellow"
        
    # Green Range
    elif 65 <= h < 165:
        return "Green"
        
    # Blue Range
    elif 165 <= h < 265:
        return "Blue"
        
    # Purple Range
    elif 265 <= h < 290:
        return "Purple"
        
    # Pink Range (Magenta/Pink/Brown transitions)
    elif 290 <= h < 345:
        if v >= 0.50 and s >= 0.20:
            return "Pink"
        else:
            return "Brown"
            
    return "Unknown"

def generate_chart(counts, total_pixels, output_path):
    """
    Generate and save a highly polished horizontal bar chart colored by the categories.
    """
    sorted_data = counts.most_common()
    if not sorted_data:
        print("Warning: No color statistics to plot.")
        return
        
    categories = [item[0] for item in sorted_data]
    percentages = [(item[1] / total_pixels) * 100 for item in sorted_data]
    
    # Curated modern HSL/Hex palette matching the 11 categories
    hex_colors = {
        "White": "#F8F9FA",   # Premium off-white
        "Black": "#212529",   # Deep charcoal/black
        "Gray": "#6C757D",    # Cool slate gray
        "Red": "#DC3545",     # Crisp crimson red
        "Orange": "#FD7E14",  # Warm orange
        "Yellow": "#FFC107",  # Soft gold/yellow
        "Green": "#198754",   # Emerald/forest green
        "Blue": "#0D6EFD",    # Royal blue
        "Purple": "#6F42C1",  # Deep indigo/purple
        "Pink": "#E83E8C",    # Hot pink
        "Brown": "#795548",   # Rich brown
    }
    
    colors = [hex_colors.get(cat, "#333333") for cat in categories]
    # Add borders to White so it shows up cleanly on the light background
    edge_colors = ["#CED4DA" if cat == "White" else "none" for cat in categories]
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    
    # Plot horizontal bars
    bars = ax.barh(categories, percentages, color=colors, edgecolor=edge_colors, height=0.6, linewidth=1)
    
    # Customizing look and feel
    ax.invert_yaxis()  # Top-down order (dominant colors on top)
    ax.set_xlabel('Percentage Share (%)', fontsize=12, fontweight='bold', color='#495057')
    ax.set_title('Color Percentage Breakdown', fontsize=16, fontweight='bold', color='#212529', pad=20)
    ax.set_xlim(0, max(percentages) * 1.15)  # Leave margin for bar labels
    
    # Remove top, right, and left spines to create an open modern look
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#DEE2E6')
    ax.tick_params(axis='y', left=False, labelsize=11)
    ax.tick_params(axis='x', labelsize=10, colors='#6C757D')
    
    # Overlay percentage text on the right of each bar
    for bar, pct in zip(bars, percentages):
        width = bar.get_width()
        ax.text(width + 0.8, bar.get_y() + bar.get_height()/2, f'{pct:.1f}%', 
                va='center', ha='left', fontsize=10, fontweight='bold', color='#495057')
                
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Color distribution chart successfully saved to: {output_path}")

def analyze_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' does not exist.")
        sys.exit(1)
        
    try:
        with Image.open(image_path) as img:
            # 1. Transparency / Alpha Channel handling: Composite onto a solid white background
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                print("Image has transparency/alpha channel. Blending onto white background...")
                img = img.convert('RGBA')
                background = Image.new("RGBA", img.size, (255, 255, 255, 255))
                # Paste the transparent image over the solid white background
                img = Image.alpha_composite(background, img)
                img = img.convert('RGB')
            elif img.mode != 'RGB':
                # Convert other modes (like L, Grayscale) to RGB
                img = img.convert('RGB')
            
            width, height = img.size
            total_raw_pixels = width * height
            
            # 2. Resolution Optimization: Auto-downscale large images to max 800px dimensions
            MAX_PIXELS = 1_000_000
            MAX_DIM = 800
            if total_raw_pixels > MAX_PIXELS:
                print(f"Image is large ({width}x{height} = {total_raw_pixels:,} px). Downsampling for performance...")
                scale_factor = min(MAX_DIM / width, MAX_DIM / height)
                new_size = (int(width * scale_factor), int(height * scale_factor))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                width, height = img.size
                print(f"Downsampled to: {width}x{height} ({width * height:,} px).")
            
            # Load pixels safely
            pixel_access = img.load()
            pixels = []
            for y in range(height):
                for x in range(width):
                    pixels.append(pixel_access[x, y])
    except Exception as e:
        print(f"Error opening/reading image: {e}")
        sys.exit(1)
        
    total_pixels = len(pixels)
    if total_pixels == 0:
        print("Error: Image has no pixels.")
        sys.exit(1)
        
    # Classify each pixel using advanced rule matrix
    categories = []
    for r, g, b in pixels:
        h_norm, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h = h_norm * 360.0
        category = classify_hsv_advanced(h, s, v)
        categories.append(category)
        
    # Count frequency of each color category
    counts = Counter(categories)
    
    # Print terminal output report
    print(f"\nColor Analysis Results for: {os.path.basename(image_path)}")
    print(f"Total Pixels Scanned: {total_pixels:,}\n")
    print(f"| {'Color Category':<15} | {'Percentage':<10} | {'Pixel Count':<12} |")
    print(f"|{'-'*17}|{'-'*12}|{'-'*14}|")
    
    for category, count in counts.most_common():
        percentage = (count / total_pixels) * 100
        bar_length = int(percentage / 2)
        bar = "#" * bar_length
        print(f"| {category:<15} | {percentage:>8.2f}% | {count:>12,} | {bar}")
    
    # Generate and save Phase 2 Matplotlib chart
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_chart_path = os.path.join(os.path.dirname(image_path) or ".", f"output_{base_name}.png")
    generate_chart(counts, total_pixels, output_chart_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python color_analyzer.py <path_to_image>")
        sys.exit(1)
    analyze_image(sys.argv[1])
