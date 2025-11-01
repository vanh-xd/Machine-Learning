import os
import sys
import numpy as np
import pandas as pd

# Path setup to import sibling modules within project_retail
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from analytics.customer_clustering import get_customers_by_cluster


def _html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def render_clusters_web(k: int = 5, feature_cols: list[str] | None = None) -> str:
    """
    Generate a styled, interactive HTML page showing all customers per cluster.
    Returns the path to the written HTML file under project_retail/ui.
    """
    clusters_map, df_with_cluster, used_cols = get_customers_by_cluster(k=k, feature_cols=feature_cols)

    title = f"Customer Clusters (k={k})"
    out_dir = os.path.join(PROJECT_ROOT, 'ui')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"customer_clusters_k{k}_web.html")

    # Build interactive controls and polished styling
    style = """
    :root {
      --bg: #0f172a; /* slate-900 */
      --panel: #111827; /* gray-900 */
      --text: #e5e7eb; /* gray-200 */
      --muted: #9ca3af; /* gray-400 */
      --accent: #06b6d4; /* cyan-500 */
      --accent-2: #22c55e; /* green-500 */
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--text); font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
    .wrap { max-width: 1200px; margin: 24px auto; padding: 0 16px; }
    .header { display:flex; align-items:center; justify-content:space-between; padding: 20px; background: linear-gradient(120deg, rgba(6,182,212,.12), rgba(34,197,94,.12)); border: 1px solid rgba(229,231,235,.12); border-radius: 16px; }
    .title { font-size: 22px; font-weight: 700; letter-spacing: .2px; }
    .sub { color: var(--muted); font-size: 14px; }
    .controls { display:flex; gap: 12px; align-items:center; }
    .search { background: var(--panel); border: 1px solid rgba(229,231,235,.08); color: var(--text); padding: 10px 12px; border-radius: 10px; min-width: 260px; outline: none; }
    .pill { background: rgba(6,182,212,.14); color: #67e8f9; border: 1px solid rgba(6,182,212,.34); padding: 8px 12px; border-radius: 999px; font-size: 12px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; margin-top: 14px; }
    .card { background: var(--panel); border: 1px solid rgba(229,231,235,.08); border-radius: 14px; overflow: hidden; }
    .card .head { display:flex; align-items:center; justify-content:space-between; padding: 12px 14px; border-bottom: 1px solid rgba(229,231,235,.06); }
    .card .head h2 { margin: 0; font-size: 16px; }
    .card .head .count { color: var(--muted); font-size: 12px; }
    .collapse-btn { background: transparent; color: var(--muted); border: none; cursor: pointer; font-size: 12px; }
    .table-wrap { overflow: auto; max-height: 460px; }
    table { border-collapse: collapse; width: 100%; }
    thead { position: sticky; top: 0; background: #0b1220; }
    th, td { border-bottom: 1px solid rgba(229,231,235,.06); padding: 8px 10px; text-align: left; font-size: 13px; }
    tr:hover td { background: rgba(229,231,235,.02); }
    .footer { margin-top: 18px; color: var(--muted); font-size: 12px; text-align: center; }
    .note { color: var(--muted); font-size: 12px; }
    """

    # Build cluster navigation and stats
    total_customers = sum(len(cdf) for cdf in clusters_map.values())
    nav_items = []
    for ci, cdf in clusters_map.items():
        nav_items.append(f"<span class='pill'>Cluster {ci}: {len(cdf)}</span>")
    nav_html = "<div class='grid'>" + "".join(nav_items) + "</div>"

    # Search and collapse JS
    script = """
    function filterTables() {
      const q = (document.getElementById('search').value || '').toLowerCase();
      const sections = document.querySelectorAll('.cluster-section');
      sections.forEach(sec => {
        const rows = sec.querySelectorAll('tbody tr');
        rows.forEach(r => {
          const text = r.innerText.toLowerCase();
          r.style.display = text.indexOf(q) !== -1 ? '' : 'none';
        });
      });
    }
    function toggleSection(id) {
      const el = document.getElementById(id);
      if (!el) return;
      el.style.display = (el.style.display === 'none') ? '' : 'none';
    }
    """

    # Build content for each cluster with full details
    sections = []
    for ci, cdf in clusters_map.items():
        # Ensure all columns show, including non-numeric
        # Convert to HTML with sticky header, no index
        table_html = cdf.to_html(index=False, border=0)
        sec = f"""
        <div class='card'>
          <div class='head'>
            <h2>Cluster {ci}</h2>
            <div class='controls'>
              <span class='count'>{len(cdf)} customers</span>
              <button class='collapse-btn' onclick="toggleSection('csec-{ci}')">Collapse/Expand</button>
            </div>
          </div>
          <div id='csec-{ci}' class='table-wrap cluster-section'>
            {table_html}
          </div>
        </div>
        """
        sections.append(sec)

    # Compose full HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset='utf-8'>
      <meta name='viewport' content='width=device-width,initial-scale=1'>
      <title>{_html_escape(title)}</title>
      <style>{style}</style>
    </head>
    <body>
      <div class='wrap'>
        <div class='header'>
          <div>
            <div class='title'>{_html_escape(title)}</div>
            <div class='sub'>Total customers: {total_customers} &middot; Features used: {_html_escape(", ".join(used_cols))}</div>
          </div>
          <div class='controls'>
            <input id='search' class='search' type='search' placeholder='Search customers…' oninput='filterTables()' />
          </div>
        </div>

        {nav_html}

        <div style='margin-top: 16px; display: grid; gap: 14px;'>
          {''.join(sections)}
        </div>

        <div class='footer'>
          Generated by Customer Clustering &mdash; k={k}
          <div class='note'>All customer details originate from the 'customer' table in MySQL (salesdatabase).</div>
        </div>
      </div>
      <script>{script}</script>
    </body>
    </html>
    """

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return out_path


def run_web_exports():
    paths = []
    paths.append(render_clusters_web(k=3))
    paths.append(render_clusters_web(k=5))
    return paths


if __name__ == '__main__':
    outs = run_web_exports()
    print("Written:")
    for p in outs:
        print(" -", p)