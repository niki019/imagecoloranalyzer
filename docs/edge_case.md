# Edge Case Management: Image Color Analyzer Tool

This document outlines critical edge cases identified for the **Image Color Analyzer Tool** and details the corresponding architectural and programmatic mitigation strategies.

---

## 1. File Handling & Format Validation

### Case 1.1: Unsupported or Corrupt File Formats
* **Description**: User provides a file with an image extension (e.g., `.png`, `.jpg`) but the content is corrupted, or provides an unsupported format (e.g., `.svg`, `.psd`, `.pdf`).
* **Impact**: Application crashes with an unhandled exception or hangs during processing.
* **Mitigation**:
  * Implement safe file loading using try-except blocks catching `PIL.UnidentifiedImageError` and standard `IOError`.
  * Validate file extension and MIME type before reading pixel data.
  * *Code Pattern*:
    ```python
    from PIL import Image, UnidentifiedImageError

    try:
        with Image.open(image_path) as img:
            img.verify() # Verify integrity of header
    except (UnidentifiedImageError, IOError) as e:
        print(f"Error: The file is corrupt or not a supported image format. Details: {e}")
        sys.exit(1)
    ```

### Case 1.2: Empty / Zero-byte Files
* **Description**: The provided image file is empty (0 bytes).
* **Impact**: Crash on attempt to read or verify the image.
* **Mitigation**:
  * Check file size before opening, or catch the resulting I/O exception.

---

## 2. Image Properties & Formats

### Case 2.1: Alpha / Transparency Channels (PNG, WEBP, GIF)
* **Description**: Transparent or semi-transparent pixels ($A < 255$ in RGBA mode) can distort the color analysis. Transparent pixels mapped directly to RGB may evaluate to black `(0, 0, 0)` or white `(255, 255, 255)`, falsely inflating those categories.
* **Impact**: Falsely high counts for "Black" or "White" depending on the default background pixel values in transparency.
* **Mitigation**:
  * If the image has an alpha channel (mode `RGBA` or `LA` or has transparency info), inspect the Alpha ($A$) channel for each pixel.
  * **Rule**: Discard pixels where $A < 50$ (fully or highly transparent).
  * For semi-transparent pixels ($50 \le A < 255$), blend them with a solid background color (default to White) using alpha compositing:
    $$C_{blended} = C_{pixel} \times \left(\frac{A}{255}\right) + C_{bg} \times \left(1 - \frac{A}{255}\right)$$
  * Alternatively, convert the RGBA image to RGB by pasting it onto a solid white background:
    ```python
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        background = Image.new("RGB", img.size, (255, 255, 255))
        # Paste using alpha channel as mask
        background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = background
    ```

### Case 2.2: Grayscale Images (Mode `L` or `LA`)
* **Description**: Single-channel grayscale images do not contain separate Red, Green, and Blue values. Directly index-accessing them (e.g., `r, g, b = pixel`) will raise a `TypeError` or `ValueError`.
* **Impact**: Crash during pixel extraction.
* **Mitigation**:
  * Check the image mode. If the mode is not `RGB` or `RGBA`, convert it to `RGB` before scanning.
  * *Code Pattern*:
    ```python
    if img.mode != 'RGB':
        img = img.convert('RGB')
    ```

---

## 3. Scale and Performance

### Case 3.1: Ultra-High Resolution Images (e.g., 50 Megapixels)
* **Description**: Processing an image pixel-by-pixel scales linearly ($O(N)$ where $N = W \times H$). Large images can take several minutes to run and consume excessive memory.
* **Impact**: Long delay, UI lockup, or Out of Memory (OOM) crashes.
* **Mitigation**:
  * Check the total pixel count ($W \times H$). If it exceeds $1,000,000$ pixels, scale the image down.
  * Resize the image so its maximum dimension is $800$ pixels, maintaining the original aspect ratio.
  * Use `PIL.Image.Resampling.LANCZOS` (or `LANCZOS` constant depending on Pillow version) to prevent color distortion during downsampling.
  * *Code Pattern*:
    ```python
    MAX_PIXELS = 1_000_000
    MAX_DIM = 800
    width, height = img.size
    if (width * height) > MAX_PIXELS:
        scale_factor = min(MAX_DIM / width, MAX_DIM / height)
        new_size = (int(width * scale_factor), int(height * scale_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    ```

### Case 3.2: Extremely Small Images (e.g., 1x1, 2x2 pixels)
* **Description**: Analyzing tiny images can result in round-off or zero-division errors if not handled correctly.
* **Impact**: Crash during percentage calculations.
* **Mitigation**:
  * Check that the total count of valid pixels is greater than zero before dividing.
  * If valid pixel count is 0, raise a descriptive exception.

---

## 4. Algorithmic Color Classification Edge Cases

### Case 4.1: Fuzzy Boundaries (Hue/Saturation/Value Transitions)
* **Description**: A pixel with H=14.9° is Red, and H=15.1° is Orange. Value-based transitions (e.g., Brown vs. Pink or Orange) are particularly sensitive.
* **Impact**: Minor lighting changes in an image can shift color classifications drastically.
* **Mitigation**:
  * Use strict floating-point comparisons (e.g., using `float` for HSV calculations instead of truncated integers).
  * Document exact boundary thresholds in the code and avoid gaps between intervals. For example, use standard half-open intervals $[H_{start}, H_{end})$ for hue rules.

### Case 4.2: Monochromatic Images
* **Description**: The input image contains only a single color (e.g., an all-white background or a solid blue screen).
* **Impact**: Matplotlib might fail or produce empty/flat-lined charts if data has only one category.
* **Mitigation**:
  * Ensure the chart generator handles single-value lists gracefully.
  * Set explicit axis limits (e.g., `plt.xlim(0, 100)`) so the bar reaches 100% cleanly without breaking layout dimensions.
