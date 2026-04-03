import os
import json
import uuid
import subprocess
import tempfile
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCcY-pjt7SEFNSOkKhRBcrICNzTkXVDaiE")


def extract_text_from_file(file_storage) -> str:
    """Extract plain text from a .txt or .pdf upload."""
    filename = file_storage.filename.lower()

    if filename.endswith(".txt"):
        raw = file_storage.read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1")

    elif filename.endswith(".pdf"):
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise RuntimeError("PyMuPDF not installed. Run: pip install PyMuPDF")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            file_storage.save(tmp.name)
            tmp_path = tmp.name

        try:
            doc = fitz.open(tmp_path)
            text = "\n".join(page.get_text("text") for page in doc)
            doc.close()
        finally:
            os.unlink(tmp_path)

        # Clean non-encodable characters
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        return text

    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf are allowed.")


def generate_slide_data_with_gemini(text: str, mode: str, slide_topics: list, slide_count: int) -> list:
    """
    Call Gemini AI to generate structured slide data.
    Returns a list of dicts: [{title, bullets: [str], layout: str}, ...]
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    if mode == "manual" and slide_topics:
        topic_list = "\n".join(f"- {t}" for t in slide_topics)
        prompt = f"""You are a presentation expert. Based on the document below, generate exactly {len(slide_topics)} slides for these specific topics:
{topic_list}

For each topic, create a slide with:
- A concise title (max 8 words)
- 3 to 5 bullet points (each max 15 words)
- layout: one of "title", "content", "two_column", "stat"

Document:
\"\"\"
{text[:6000]}
\"\"\"

Respond ONLY with valid JSON array like:
[
  {{
    "title": "Slide Title",
    "bullets": ["Point one", "Point two", "Point three"],
    "layout": "content"
  }}
]
No markdown, no preamble, only the JSON array."""
    else:
        prompt = f"""You are a presentation expert. Analyze the document below and generate a structured presentation with {slide_count} slides.

Include:
- 1 title slide (layout: "title") with a subtitle bullet
- {slide_count - 2} content slides (layout: "content" or "two_column" or "stat")
- 1 summary/conclusion slide (layout: "content")

Each slide:
- concise title (max 8 words)
- 3 to 5 bullet points (each max 15 words)
- layout: one of "title", "content", "two_column", "stat"

Document:
\"\"\"
{text[:6000]}
\"\"\"

Respond ONLY with valid JSON array like:
[
  {{
    "title": "Slide Title",
    "bullets": ["Point one", "Point two", "Point three"],
    "layout": "content"
  }}
]
No markdown, no preamble, only the JSON array."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )

    raw = response.text.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    slides = json.loads(raw)
    return slides


def build_pptx_from_slides(slides: list, output_path: str) -> None:
    """Use pptxgenjs via Node.js to build the .pptx file from slide data."""

    # Color palette: Ocean Gradient + white
    PALETTE = {
        "primary": "065A82",
        "secondary": "1C7293",
        "accent": "21295C",
        "white": "FFFFFF",
        "light_bg": "EEF6FB",
        "text_dark": "1A1A2E",
        "text_muted": "4A6572",
    }

    js_slides = json.dumps(slides, ensure_ascii=True)
    palette_js = json.dumps(PALETTE)

    # Use forward slashes for Node.js path compatibility on Windows
    output_path_js = output_path.replace("\\", "/")

    node_script = f"""
const pptxgen = require("C:/Users/LENOVO/AppData/Roaming/npm/node_modules/pptxgenjs")

const slides = {js_slides};
const C = {palette_js};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Shiksha Sahayak Presentation";
pres.author = "Shiksha Sahayak AI";

function makeShadow() {{
  return {{ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.12 }};
}}

slides.forEach((slide, idx) => {{
  const s = pres.addSlide();
  const layout = slide.layout || "content";
  const bullets = slide.bullets || [];

  if (layout === "title") {{
    // ── TITLE SLIDE ──
    s.background = {{ color: C.accent }};

    // Large decorative shape top-right
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 7.5, y: 0, w: 2.5, h: 5.625,
      fill: {{ color: C.primary, transparency: 40 }},
      line: {{ color: C.primary, transparency: 40 }}
    }});
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 8.5, y: 0, w: 1.5, h: 5.625,
      fill: {{ color: C.secondary, transparency: 30 }},
      line: {{ color: C.secondary, transparency: 30 }}
    }});

    // Slide number chip
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {{
      x: 0.5, y: 0.35, w: 0.5, h: 0.3,
      fill: {{ color: C.secondary }},
      line: {{ color: C.secondary }},
      rectRadius: 0.05
    }});
    s.addText(String(idx + 1), {{
      x: 0.5, y: 0.35, w: 0.5, h: 0.3,
      fontSize: 10, color: C.white, align: "center", valign: "middle", bold: true, margin: 0
    }});

    // Title
    s.addText(slide.title, {{
      x: 0.6, y: 1.5, w: 6.8, h: 1.5,
      fontSize: 40, fontFace: "Cambria", bold: true, color: C.white,
      align: "left", valign: "middle"
    }});

    // Subtitle bullet
    if (bullets.length > 0) {{
      s.addText(bullets[0], {{
        x: 0.6, y: 3.2, w: 6.8, h: 0.8,
        fontSize: 16, fontFace: "Calibri", color: "CADCFC",
        align: "left", italic: true
      }});
    }}

    // Bottom bar
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 5.2, w: 10, h: 0.425,
      fill: {{ color: C.primary }},
      line: {{ color: C.primary }}
    }});
    s.addText("Shiksha Sahayak · AI-Powered Education", {{
      x: 0.5, y: 5.2, w: 9, h: 0.425,
      fontSize: 10, color: C.white, align: "left", valign: "middle", margin: 0
    }});

  }} else if (layout === "stat") {{
    // ── STAT SLIDE ──
    s.background = {{ color: C.light_bg }};

    // Header bar
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 10, h: 1.0,
      fill: {{ color: C.primary }},
      line: {{ color: C.primary }}
    }});
    s.addText(slide.title, {{
      x: 0.5, y: 0, w: 9, h: 1.0,
      fontSize: 22, fontFace: "Cambria", bold: true, color: C.white,
      align: "left", valign: "middle", margin: 0
    }});

    // Stat cards
    const cols = Math.min(bullets.length, 3);
    const cardW = (10 - 1.0) / cols;
    bullets.slice(0, 3).forEach((b, i) => {{
      const cx = 0.5 + i * (cardW + 0.1);
      s.addShape(pres.shapes.RECTANGLE, {{
        x: cx, y: 1.3, w: cardW - 0.1, h: 2.8,
        fill: {{ color: C.white }},
        line: {{ color: "D0E8F2", width: 1 }},
        shadow: makeShadow()
      }});
      // Accent left border
      s.addShape(pres.shapes.RECTANGLE, {{
        x: cx, y: 1.3, w: 0.08, h: 2.8,
        fill: {{ color: C.secondary }},
        line: {{ color: C.secondary }}
      }});
      s.addText(b, {{
        x: cx + 0.2, y: 1.5, w: cardW - 0.4, h: 2.4,
        fontSize: 14, fontFace: "Calibri", color: C.text_dark,
        align: "left", valign: "middle", wrap: true
      }});
    }});

    // Footer
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 5.2, w: 10, h: 0.425,
      fill: {{ color: C.accent }},
      line: {{ color: C.accent }}
    }});
    s.addText("Shiksha Sahayak", {{
      x: 0.5, y: 5.2, w: 9, h: 0.425,
      fontSize: 9, color: C.white, align: "right", valign: "middle", margin: 0
    }});

  }} else if (layout === "two_column") {{
    // ── TWO COLUMN SLIDE ──
    s.background = {{ color: C.white }};

    // Header bar
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 10, h: 1.0,
      fill: {{ color: C.primary }},
      line: {{ color: C.primary }}
    }});
    s.addText(slide.title, {{
      x: 0.5, y: 0, w: 9, h: 1.0,
      fontSize: 22, fontFace: "Cambria", bold: true, color: C.white,
      align: "left", valign: "middle", margin: 0
    }});

    const half = Math.ceil(bullets.length / 2);
    const leftBullets = bullets.slice(0, half);
    const rightBullets = bullets.slice(half);

    // Left column
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0.4, y: 1.2, w: 4.3, h: 4.0,
      fill: {{ color: C.light_bg }},
      line: {{ color: "D0E8F2", width: 1 }},
      shadow: makeShadow()
    }});
    s.addText(leftBullets.map(b => ({{ text: b, options: {{ bullet: true, breakLine: true, paraSpaceAfter: 4 }} }})), {{
      x: 0.6, y: 1.3, w: 4.0, h: 3.8,
      fontSize: 14, fontFace: "Calibri", color: C.text_dark, valign: "top"
    }});

    // Right column
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 5.2, y: 1.2, w: 4.3, h: 4.0,
      fill: {{ color: C.light_bg }},
      line: {{ color: "D0E8F2", width: 1 }},
      shadow: makeShadow()
    }});
    s.addText(rightBullets.map(b => ({{ text: b, options: {{ bullet: true, breakLine: true, paraSpaceAfter: 4 }} }})), {{
      x: 5.4, y: 1.3, w: 4.0, h: 3.8,
      fontSize: 14, fontFace: "Calibri", color: C.text_dark, valign: "top"
    }});

    // Footer
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 5.2, w: 10, h: 0.425,
      fill: {{ color: C.accent }},
      line: {{ color: C.accent }}
    }});
    s.addText("Shiksha Sahayak", {{
      x: 0.5, y: 5.2, w: 9, h: 0.425,
      fontSize: 9, color: C.white, align: "right", valign: "middle", margin: 0
    }});

  }} else {{
    // ── CONTENT SLIDE (default) ──
    s.background = {{ color: C.white }};

    // Header bar
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 10, h: 1.0,
      fill: {{ color: C.primary }},
      line: {{ color: C.primary }}
    }});
    // Accent strip
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 0.25, h: 1.0,
      fill: {{ color: C.secondary }},
      line: {{ color: C.secondary }}
    }});
    s.addText(slide.title, {{
      x: 0.5, y: 0, w: 9, h: 1.0,
      fontSize: 22, fontFace: "Cambria", bold: true, color: C.white,
      align: "left", valign: "middle", margin: 0
    }});

    // Slide number chip
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {{
      x: 9.0, y: 0.3, w: 0.5, h: 0.3,
      fill: {{ color: C.accent }},
      line: {{ color: C.accent }},
      rectRadius: 0.05
    }});
    s.addText(String(idx + 1), {{
      x: 9.0, y: 0.3, w: 0.5, h: 0.3,
      fontSize: 9, color: C.white, align: "center", valign: "middle", bold: true, margin: 0
    }});

    // Content area
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0.4, y: 1.15, w: 9.2, h: 4.05,
      fill: {{ color: C.light_bg }},
      line: {{ color: "D0E8F2", width: 1 }},
      shadow: makeShadow()
    }});

    s.addText(bullets.map(b => ({{ text: b, options: {{ bullet: true, breakLine: true, paraSpaceAfter: 6 }} }})), {{
      x: 0.65, y: 1.3, w: 8.7, h: 3.75,
      fontSize: 15, fontFace: "Calibri", color: C.text_dark, valign: "top"
    }});

    // Footer
    s.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 5.2, w: 10, h: 0.425,
      fill: {{ color: C.accent }},
      line: {{ color: C.accent }}
    }});
    s.addText("Shiksha Sahayak", {{
      x: 0.5, y: 5.2, w: 9, h: 0.425,
      fontSize: 9, color: C.white, align: "right", valign: "middle", margin: 0
    }});
  }}
}});

pres.writeFile({{ fileName: "{output_path_js}" }})
  .then(() => console.log("PPT_DONE"))
  .catch(err => {{ console.error("PPT_ERROR:", err.message); process.exit(1); }});
"""

    # Write JS to temp file
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w", encoding="utf-8") as f:
        f.write(node_script)
        js_path = f.name

    try:
        result = subprocess.run(
            ["node", js_path],
            capture_output=True, text=True, timeout=60, encoding="utf-8"
        )
        if result.returncode != 0 or "PPT_ERROR" in result.stdout:
            raise RuntimeError(f"pptxgenjs failed: {result.stderr or result.stdout}")
        if "PPT_DONE" not in result.stdout:
            raise RuntimeError(f"pptxgenjs did not complete: {result.stdout}")
    finally:
        os.unlink(js_path)


def generate_ppt(file_storage, mode: str, slide_topics: list, slide_count: int) -> str:
    """
    Full pipeline: extract text → Gemini generates slides → pptxgenjs builds PPTX.
    Returns the output file path.
    """
    # 1. Extract text
    text = extract_text_from_file(file_storage)
    if not text.strip():
        raise ValueError("No readable text found in the uploaded file.")

    # 2. Gemini generates structured slide data
    slides = generate_slide_data_with_gemini(text, mode, slide_topics, slide_count)

    # 3. Build PPTX
    output_dir = os.path.join(os.getcwd(), "generated_ppts")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"presentation_{uuid.uuid4().hex[:8]}.pptx"
    output_path = os.path.join(output_dir, filename)

    build_pptx_from_slides(slides, output_path)

    return output_path