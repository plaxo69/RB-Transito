#!/usr/bin/env python3
"""Build the CHOCAS app into one self-contained HTML file."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    js = (ROOT / "app.js").read_text(encoding="utf-8")
    workbook = (ROOT / "data" / "workbook.json").read_text(encoding="utf-8")

    # The single-file build has no separate PWA/service-worker assets.
    js = re.sub(
        r"if\s*\(\s*['\"]serviceWorker['\"]\s+in\s+navigator[^\{]*\{.*?\n\s*\}",
        "",
        js,
        flags=re.DOTALL,
    )

    # Keep embedded content from closing its containing HTML tags.
    workbook = workbook.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    css = re.sub(r"</style", r"<\\/style", css, flags=re.IGNORECASE)
    js = re.sub(r"</script", r"<\\/script", js, flags=re.IGNORECASE)

    html = re.sub(r"\s*<link\b[^>]*rel=[\"']manifest[\"'][^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s*<link\b[^>]*href=[\"']styles\.css[\"'][^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s*<script\b[^>]*src=[\"']app\.js[\"'][^>]*>\s*</script>", "", html, flags=re.IGNORECASE)

    embedded_head = (
        "\n<style>\n" + css + "\n</style>\n"
        '<script type="application/json" id="workbook-data">'
        + workbook
        + "</script>\n"
    )
    html = html.replace("</head>", embedded_head + "</head>", 1)

    embedded_app = '''\n<script>
// The regular app expects workbook.json. Serve the embedded data from this one-file build.
const chocasOriginalFetch = window.fetch.bind(window);
window.fetch = async (input, init) => {
  const url = typeof input === 'string' ? input : input.url;
  if (url === './data/workbook.json' || url.endsWith('/data/workbook.json')) {
    return new Response(document.getElementById('workbook-data').textContent, {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
  return chocasOriginalFetch(input, init);
};
</script>
<script>\n''' + js + '''\n</script>\n'''
    html = html.replace("</body>", embedded_app + "</body>", 1)

    output_dir = ROOT / "dist"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"Ficheiro único criado: {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
