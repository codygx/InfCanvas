"""Render README.md to README.html for browser viewing.

Usage:
  python render_readme.py

Optional:
  pip install markdown
"""

from pathlib import Path
import html


ROOT = Path(__file__).resolve().parent
README_MD = ROOT / "README.md"
README_HTML = ROOT / "README.html"


def markdown_to_html(md_text: str) -> tuple[str, bool]:
  try:
    import markdown  # type: ignore

    body = markdown.markdown(
      md_text,
      extensions=["fenced_code", "tables", "toc", "sane_lists"],
    )
    return body, True
  except Exception:
    # Fallback keeps docs readable even without extra packages.
    escaped = html.escape(md_text)
    body = (
      "<div class='notice'>Install <code>markdown</code> for full rendering: "
      "<code>pip install markdown</code></div>"
      f"<pre>{escaped}</pre>"
    )
    return body, False


def main() -> None:
  if not README_MD.exists():
    raise SystemExit("README.md not found")

  md_text = README_MD.read_text(encoding="utf-8")
  body, used_markdown_pkg = markdown_to_html(md_text)

  title = "InfCanvas README"
  css = """
body {
  margin: 2rem auto;
  max-width: 900px;
  padding: 0 1rem;
  background: #0f1115;
  color: #e6edf3;
  font-family: Segoe UI, Roboto, Arial, sans-serif;
  line-height: 1.55;
}
a { color: #8cc8ff; }
pre, code {
  font-family: Consolas, 'Courier New', monospace;
}
pre {
  background: #171b24;
  border: 1px solid #2a3140;
  border-radius: 8px;
  padding: 0.75rem;
  overflow: auto;
}
blockquote {
  border-left: 4px solid #2f6feb;
  margin-left: 0;
  padding-left: 0.9rem;
  color: #9fb0c2;
}
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #2a3140;
  padding: 0.4rem 0.6rem;
}
.notice {
  margin-bottom: 1rem;
  padding: 0.6rem 0.75rem;
  border: 1px solid #2f6feb;
  border-radius: 8px;
  background: #152238;
}
""".strip()

  html_doc = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
  {body}
</body>
</html>
"""

  README_HTML.write_text(html_doc, encoding="utf-8")
  mode = "full markdown" if used_markdown_pkg else "fallback plain text"
  print(f"Wrote {README_HTML.name} ({mode})")


if __name__ == "__main__":
  main()
