# Image Color Percentage Analyzer

A high-performance, local-first tool designed to scan image pixels and classify their colors into **11 standardized color categories** using an HSV-based rule engine.

---

## Features

1. **Precision HSV Rule Engine**: Accurately maps all RGB pixels to 11 standardized buckets (`White`, `Black`, `Gray`, `Red`, `Orange`, `Yellow`, `Green`, `Blue`, `Purple`, `Pink`, `Brown`).
2. **Resolution Optimization**: Auto-downsamples ultra-high-resolution images (exceeding 1,000,000 pixels) to a maximum dimension of 800px using high-quality LANCZOS interpolation. Keeps processing sub-second while maintaining exact color ratios.
3. **Alpha Channel Blending**: Safely handles transparent PNG/WEBP/GIF images by alpha-compositing transparent pixels onto a solid white background, avoiding distorted counts for Black or White.
4. **Visual Dashboard Charts**: Generates highly polished horizontal bar charts sorted by color dominance, with bars colored using matching hex representations.
5. **Jupyter / Colab Drag-and-Drop Notebook**: Contains a ready-to-run interactive Google Colab notebook with an upload widget supporting drag-and-drop manual testing.

---

## Directory Structure

```
imagecoloranalyzer/
├── color_analyzer.py          # Main analyzer script (Pillow, Matplotlib)
├── color_analyzer_colab.ipynb # Interactive Google Colab notebook
├── run_analyzer.bat           # Portable batch file for manual testing
├── .gitignore                 # Excludes caches and temporary outputs
├── README.md                  # Project overview and usage
└── docs/                      # Project documentation
    ├── problemStatement.txt   # Original problem requirements
    ├── context.md             # Roadmaps and checklists
    ├── architecture.md        # System flow, algorithm, and rulesets
    └── edge_case.md           # Edge-case strategies and mitigations
```

---

## Installation & Running Locally

This project uses **`uv`** (a fast Python package installer and runner). If you don't have `uv` installed, you can install it or run standard python environments.

### Local Execution (Manual Testing)
You can run the analyzer on any image using the portable batch script:
```cmd
run_analyzer.bat <path_to_your_image.jpg>
```
This command automatically sets up the environment and packages (`Pillow`, `matplotlib`, `numpy`) and outputs:
1. A sorted markdown table in your console.
2. A matching horizontal bar chart saved as `output_<image_name>.png` in the same directory.

---

## Interactive Google Colab (Drag-and-Drop)

1. Open **[Google Colab](https://colab.research.google.com)**.
2. Select **Upload** and choose the `color_analyzer_colab.ipynb` file from this repository.
3. Execute the cells sequentially.
4. Use the **Choose Files** or **Drag-and-Drop** area in the final step to analyze any custom image dynamically.

---

## Color Mapping Ruleset (HSV Decision Matrix)

The analyzer converts RGB inputs to the HSV (Hue, Saturation, Value) color space to implement perceptual rules:

* **White**: $S < 0.08$ and $V \ge 0.85$
* **Black**: $V < 0.15$
* **Gray**: $S < 0.15$ and $0.15 \le V < 0.85$
* **Chromatic Colors** (when $S \ge 0.15$ and $V \ge 0.15$):
  * **Red**: $H \in [0, 15) \cup [345, 360]$
  * **Orange**: $H \in [15, 35)$ (maps to **Brown** if $V < 0.55$)
  * **Yellow**: $H \in [35, 65)$ (maps to **Brown** if $V < 0.50$ or $S < 0.30$)
  * **Green**: $H \in [65, 165)$
  * **Blue**: $H \in [165, 265)$
  * **Purple**: $H \in [265, 290)$
  * **Pink**: $H \in [290, 345)$ (maps to **Pink** if $V \ge 0.50$ and $S \ge 0.20$; else **Brown**)

---

## Analysis Results of Test Paintings

| Painting Name | Dominant Colors (Percentages) |
|---|---|
| **1. Mona Lisa** (Leonardo da Vinci) | **Black** (28.9%), **Brown** (26.2%), **Green** (20.5%), **Yellow** (10.0%), **Red** (9.9%) |
| **2. Flowers in a Vase** (Edouard Manet) | **Black** (43.0%), **Gray** (15.5%), **Red** (11.6%), **Brown** (8.9%), **Green** (7.0%) |
| **3. Landscape with Houses** (August Macke) | **Red** (27.7%), **Green** (22.4%), **Blue** (22.1%), **Gray** (8.7%), **Yellow** (7.0%) |
| **4. Wheatfield with Cypresses** (Vincent van Gogh) | **Blue** (27.6%), **Gray** (20.4%), **Green** (19.8%), **Yellow** (18.7%), **Brown** (6.3%) |
