# PM Internship Assignment
## Image Color Analyzer Tool
### Complete Execution Guide — What to Build, How to Build It, What to Submit

#### ELIGIBILITY CHECKLIST — Read Before Starting
* Available 7 hrs/day on weekdays (WFH)
* Minimum 4 months business internship experience (university/college society internships don't count)
* Graduating in 2027 or later
* Your college has no objection to pursuing this internship

**Prepared by:** Prashant Kumar Singh

---

### Assignment Analysis + Execution Roadmap

### SECTION 1 — The Big Picture: What Is This Assignment?
You are being asked to build a Color Percentage Analyzer — a tool that takes any image as input, scans every pixel, and outputs a bar/pie chart showing what percentage of the image belongs to each of 11 standardized color categories.

This is a 3-part deliverable: a working prototype, a Product Requirements Document (PRD), and an explainer video. The assignment tests your ability to (a) solve a real product problem, (b) articulate requirements like a PM, and (c) communicate technical concepts clearly.

| DELIVERABLE | WHAT IT IS | EFFORT ESTIMATE |
| --- | --- | --- |
| Color Charts (×4) | Screenshots of color % charts for 4 test images | ~1–2 hours |
| PRD Document | Detailed product requirements doc (PDF or Google Doc) | ~3–4 hours |
| Explainer Video | Short video of you explaining the PRD to a developer | ~1–2 hours |

---

### SECTION 2 — Understanding the Problem Statement

#### 2.1 What the Tool Does — Step by Step
* User uploads / provides any image (JPG, PNG, etc.)
* Tool reads the image at pixel level — i.e., gets the RGB value (Red, Green, Blue, 0–255 each) of every single pixel
* Each pixel's RGB value is classified into one of 11 color buckets
* The tool counts how many pixels fall into each bucket
* Output: a chart (bar or pie) showing the % share of each color

#### 2.2 The 11 Color Categories
Every color in existence must be mapped to exactly one of these 11 categories. Similar shades are grouped together:

| Category | Examples of What Maps Here |
| --- | --- |
| White | Snow white, cream, ivory, off-white, very light shades |
| Black | Jet black, very dark gray, near-black shades |
| Gray | All medium grays, silver, charcoal, ash |
| Red | Bright red, burgundy, maroon, crimson, dark red |
| Orange | Orange, tangerine, amber, burnt orange |
| Yellow | Yellow, light yellow, gold, lemon, mustard |
| Green | All greens — lime, forest, olive, teal-green, mint |
| Blue | Sky blue, navy, royal blue, cobalt, teal-blue |
| Purple | Violet, indigo, lavender, dark purple, mauve |
| Pink | Hot pink, light pink, rose, blush, fuchsia |
| Brown | Brown, tan, beige, chocolate, khaki, skin tones |

#### 2.3 The Color Mapping Algorithm — How Does It Work?
The core challenge is: given any RGB triplet like (210, 180, 140) — how do you decide it's 'Brown' and not 'Orange'? Two approaches:

##### Approach A — HSV-Based Rule Engine (Recommended)
Convert RGB -> HSV (Hue, Saturation, Value). Then apply rules:
* Saturation very low + Value high -> White
* Saturation very low + Value low -> Black
* Saturation low -> Gray
* Hue 0–15 or 345–360 -> Red
* Hue 16–35 -> Orange
* Hue 36–65 -> Yellow
* Hue 66–165 -> Green
* Hue 166–265 -> Blue
* Hue 266–290 -> Purple
* Hue 291–345 (low saturation) -> Pink / Brown depending on Value

##### Approach B — Nearest Neighbor / K-means Clustering
Define representative RGB values for each of the 11 categories. For every pixel, compute Euclidean distance in RGB space to all 11 reference colors and assign the closest. This is simpler but less perceptually accurate than HSV.

> [!NOTE]
> For the prototype, either approach works. The PRD should describe the chosen algorithm in enough detail that a developer can implement it without ambiguity.

---

### SECTION 3 — Deliverable 1: The Working Prototype
The assignment explicitly says: DO NOT manually code or host a full-fledged app. A simple barebones prototype running locally or inside an LLM environment is enough. You will screenshare and demo this during the interview.

##### Option A — Python Script (Simplest, Recommended)
Use Python with Pillow + matplotlib. Run it in a Jupyter notebook or Google Colab. No installation needed for the interviewer to verify — just show the output.
```bash
# Install once
pip install Pillow matplotlib numpy
# Then run color_analyzer.py
python color_analyzer.py TestImage1.jpg
```
The script should: (1) load the image, (2) loop through pixels, (3) classify each pixel into one of 11 categories, (4) count totals, (5) plot a horizontal bar chart with % values, (6) save the chart as PNG.

##### Option B — Google Colab Notebook
Upload the 4 test images to Colab, run the analysis there, and screenshot the output charts. Colab already has Pillow, numpy, matplotlib pre-installed.

##### Option C — Claude Artifact (What We're Doing Here)
Use Claude's code execution environment to run the analysis directly. This is the fastest path — no local setup needed.

> [!IMPORTANT]
> Key interview tip: You must be able to explain the prompts you used to build the prototype. Keep a copy of all your prompts in a doc before the interview.

##### Expected Output — Color Chart
For each of the 4 images, you need a chart that looks like this:
```
Color     % Share     Visual Bar
Blue      34.2%       ██████████████████████████████
White     28.7%       █████████████████████████
Green     15.1%       ███████████████
Gray      12.0%       ████████████
...       ...         ...
```

---

### SECTION 4 — Deliverable 2: The PRD
The PRD is the most important deliverable from a PM evaluation standpoint. It should be detailed enough that a developer can implement the feature without asking a single question.

| # | PRD Section | What to Cover |
|---|---|---|
| 1 | Overview / Problem Statement | What problem does this solve? Who needs it? Why now? |
| 2 | Goals & Non-Goals | What the tool WILL do. What it explicitly will NOT do. |
| 3 | User Personas | Who are the users? Designer? Marketer? Data analyst? |
| 4 | User Stories | As a [user], I want to [action] so that [benefit]. |
| 5 | Input Specification | Accepted formats (JPG/PNG/WEBP), max file size, resolution limits |
| 6 | Color Mapping Algorithm | Detailed HSV/RGB rules for all 11 categories. Thresholds. Edge cases. |
| 7 | Output Specification | Chart type, axes, labels, export format (PNG/SVG), colors used in chart |
| 8 | Edge Cases | Transparent pixels, very small images, grayscale images, error handling |
| 9 | Performance Requirements | Max processing time, max image size supported |
| 10| Success Metrics | How do we know the tool is working correctly? Accuracy benchmark? |
| 11| Out of Scope | No sub-color detection, no palette extraction, no color naming beyond 11 |

> [!NOTE]
> Length: Aim for 4–8 pages. Too short = not detailed enough. Too long = padding. Use clear headings, bullet points, and tables where possible.

##### The Color Mapping Algorithm Section (Critical — Must Be Unambiguous)
This is what separates a good PRD from a great one. You must define EXACT thresholds. Example:
* IF Saturation < 0.10 AND Value > 0.90 -> White
* IF Saturation < 0.10 AND Value < 0.20 -> Black
* IF Saturation < 0.20 -> Gray
* IF Hue in [0, 15) OR [345, 360] -> Red
* IF Hue in [15, 35) -> Orange
* IF Hue in [35, 65) -> Yellow
* IF Hue in [65, 165) -> Green
* IF Hue in [165, 265) -> Blue
* IF Hue in [265, 290) -> Purple
* IF Hue in [290, 345) AND Value < 0.50 -> Brown
* IF Hue in [290, 345) AND Value >= 0.50 -> Pink

---

### SECTION 5 — Deliverable 3: Explainer Video
Record a short video (3–7 minutes recommended) of yourself explaining the product and the color mapping algorithm as if you're talking to a developer who will implement it.

##### Structure Your Video Like This:
| Step | What to Say/Show | Duration |
|---|---|---|
| 1 | Quick intro — who you are, what the tool does in 1 sentence | 30 sec |
| 2 | Walk through the problem: user uploads image -> pixel analysis -> chart output | 60 sec |
| 3 | Explain the 11 color categories — show examples of edge cases (navy = Blue, burgundy = Red) | 90 sec |
| 4 | Walk through the color mapping algorithm — HSV thresholds, what happens at boundaries | 90 sec |
| 5 | Show the prototype output — share screen, show the 4 charts | 60 sec |
| 6 | Wrap up — mention success metrics and edge cases | 30 sec |

##### Video Tips:
* Face must be clearly visible — good lighting, front-facing camera
* Audio must be clear — use headphones with mic if possible
* Don't read from a script — speak naturally like you're in a meeting
* Use Loom (free) for easy screen + face recording
* Keep the video link public / accessible for the evaluators

> [!NOTE]
> This video simulates how you'd kick off a sprint with your dev team — clarity and confidence matter.

---

### SECTION 6 — Step-by-Step Execution Plan
Here's the recommended order of execution to complete this assignment efficiently:

| STEP | ACTION | TIME | OUTPUT |
|---|---|---|---|
| 1 | Analyze the 4 test images visually — note what colors are dominant | 15 min | Mental baseline |
| 2 | Build/run the Python color analyzer on all 4 images | 1–2 hr | 4 color charts (PNG screenshots) |
| 3 | Draft the PRD — start with algorithm section first, then user stories | 3–4 hr | PRD draft |
| 4 | Review PRD — check: is every section unambiguous? Can a dev build from this? | 30 min | Final PRD |
| 5 | Record explainer video (use Loom or OBS), export and upload | 1–2 hr | Video link/file |
| 6 | Create Google Drive folder, upload all deliverables, set sharing to public | 15 min | Submission link |

---

### SECTION 7 — Tools & Resources
| TOOL | USE CASE | LINK / NOTES |
|---|---|---|
| Python + Pillow | Pixel-level image reading | `pip install Pillow` |
| Matplotlib | Generating bar/pie charts | `pip install matplotlib` |
| Google Colab | Free cloud notebook — no local setup | [colab.research.google.com](https://colab.research.google.com) |
| Loom | Screen + face video recording | [loom.com](https://loom.com) (free plan sufficient) |
| Notion / Google Docs | Writing the PRD | Either format accepted |
| Google Drive | Final submission folder | Set sharing: Anyone with link -> Viewer |
| Claude / ChatGPT | LLM to help build prototype | Use to generate & debug code |

---

### SECTION 8 — Final Submission Checklist
| ITEM | DETAILS | STATUS |
|---|---|---|
| Color Chart — Image 1 | Screenshot of color % chart for TestImage1.jpg | [ ] Pending |
| Color Chart — Image 2 | Screenshot of color % chart for TestImage2.jpg | [ ] Pending |
| Color Chart — Image 3 | Screenshot of color % chart for TestImage3.jpg | [ ] Pending |
| Color Chart — Image 4 | Screenshot of color % chart for TestImage4.jpg | [ ] Pending |
| PRD Document | PDF or Google Doc link — covers all 11 sections | [ ] Pending |
| Explainer Video | Face visible, audio clear, 3–7 min, public link | [ ] Pending |
| Google Drive Folder | Public link, all 6 items uploaded, verified accessible | [ ] Pending |

> [!IMPORTANT]
> Before submitting: open an incognito window and test that your Google Drive link is accessible without signing in. If it asks for login -> the share settings are wrong.
