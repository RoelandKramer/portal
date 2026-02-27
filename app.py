# app.py
from __future__ import annotations

import base64
import html
import textwrap
from pathlib import Path

import streamlit as st


def _b64_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _render_header(logo_b64: str) -> None:
    header_html = f"""
<style>
  :root {{
    --club-blue: #0077C8;
    --strip: #E9F2FA;
    --card-bg: #FFFFFF;
    --text: #0B1B2B;
    --muted: #5A6B7B;
    --shadow: 0 10px 25px rgba(0,0,0,.10);
    --shadow-hover: 0 14px 34px rgba(0,0,0,.16);
    --radius: 18px;
  }}

  .stApp {{
    background: #F6F9FC;
    color: var(--text);
  }}

  section.main > div {{
    padding-top: 0rem;
  }}

  /* Hide sidebar + its toggle */
  [data-testid="stSidebar"] {{ display: none; }}
  [data-testid="collapsedControl"] {{ display: none; }}

  .portal-header {{
    position: relative;
    height: 170px;
    margin: 0 -1rem 1.1rem -1rem;
  }}

  .portal-header .bar {{
    height: 120px;
    background: var(--club-blue);
  }}

  .portal-header .strip {{
    height: 50px;
    background: var(--strip);
    border-bottom: 1px solid rgba(0,0,0,.06);
  }}

  .portal-header .logo {{
    position: absolute;
    left: 50%;
    top: 74px;
    transform: translate(-50%, -50%);
    width: 96px;
    height: 96px;
    border-radius: 999px;
    background: white;
    display: grid;
    place-items: center;
    box-shadow: var(--shadow);
    border: 6px solid rgba(255,255,255,.85);
  }}

  .portal-header .logo img {{
    width: 78px;
    height: 78px;
    object-fit: contain;
  }}

  .portal-title {{
    text-align: center;
    margin-top: .2rem;
    margin-bottom: 1.2rem;
  }}

  .portal-title h1 {{
    font-size: 1.6rem;
    margin: 0;
    letter-spacing: .2px;
  }}

  .portal-title p {{
    margin: .35rem 0 0 0;
    color: var(--muted);
    font-size: .95rem;
  }}

  .card-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }}

  @media (max-width: 760px) {{
    .card-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  a.app-card {{
    text-decoration: none !important;
    color: inherit !important;
    display: block;
  }}

  .app-card-inner {{
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 18px 18px 16px 18px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(0,0,0,.06);
    transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    height: 100%;
  }}

  .app-card-inner:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
    border-color: rgba(0,0,0,.10);
  }}

  .app-card-title {{
    font-weight: 700;
    font-size: 1.05rem;
    margin: 0 0 .25rem 0;
  }}

  .app-card-subtitle {{
    margin: 0 0 .75rem 0;
    color: var(--muted);
    font-size: .92rem;
    line-height: 1.25rem;
  }}

  .app-card-cta {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    color: var(--club-blue);
    font-size: .95rem;
  }}

  .app-card-cta .dot {{
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: var(--club-blue);
    box-shadow: 0 0 0 6px rgba(0,119,200,.10);
  }}

  #MainMenu {{visibility: hidden;}}
  footer {{visibility: hidden;}}
  header {{visibility: hidden;}}
</style>

<div class="portal-header">
  <div class="bar"></div>
  <div class="strip"></div>
  <div class="logo">
    <img src="data:image/png;base64,{logo_b64}" alt="Logo"/>
  </div>
</div>

<div class="portal-title">
  <h1>FC Den Bosch • App Portal: Data-Driven applications</h1>
  <p>Select an application to launch</p>
</div>
"""
    st.markdown(textwrap.dedent(header_html).strip(), unsafe_allow_html=True)


def _render_cards(apps: list[dict[str, str]]) -> None:
    parts: list[str] = ["<div class='card-grid'>"]

    for app in apps:
        title = html.escape(app["title"])
        subtitle = html.escape(app["subtitle"])
        url = html.escape(app["url"], quote=True)

        parts.append(
            (
                f"<a class='app-card' href='{url}' target='_blank' rel='noopener noreferrer'>"
                f"<div class='app-card-inner'>"
                f"<div class='app-card-title'>{title}</div>"
                f"<div class='app-card-subtitle'>{subtitle}</div>"
                f"<div class='app-card-cta'><span class='dot'></span> Open app</div>"
                f"</div>"
                f"</a>"
            )
        )

    parts.append("</div>")
    st.markdown("\n".join(parts), unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="FC Den Bosch Portal", page_icon="🧭", layout="wide")

    apps = [
        {
            "title": "Opponent Corner Analysis",
            "subtitle": (
                "Insights on attacking and defensive corners by any team in the KKD. "
                "Select team + number of matches and receive a pptx analysis."
            ),
            "url": "https://opponent-analysis-fcdb2.streamlit.app/",
        },
        {
            "title": "Physical Radar Graph",
            "subtitle": (
                "Radar chart comparing FC Den Bosch players to KKD/Eredivisie players "
                "based on physical output (runs, sprints, total distance)."
            ),
            "url": "https://fcdenbosch-playerbenchmarks.streamlit.app/",
        },
        {
            "title": "Player Report",
            "subtitle": "Automatically generate a player report based on SciSports data.",
            "url": "https://spelersrapport-ofnaaw7mqygeaths7pkg8r.streamlit.app/",
        },
        {
            "title": "Player Movement per game",
            "subtitle": "Overview of player movement by FC Den Bosch players per match.",
            "url": "https://speler-beweging-wedstrijd.streamlit.app/",
        },
        {
            "title": "Team & Player analysis",
            "subtitle": "Compare player data vs KKD/Eredivisie levels (football & physical metrics).",
            "url": "https://team-player-data-comparison-fcdb-3471893472.streamlit.app/",
        },
    ]

    logo_path = Path(__file__).parent / "assets" / "fc_den_bosch_logo.png"
    if not logo_path.exists():
        st.error(f"Logo not found at: {logo_path}")
        st.stop()

    _render_header(_b64_image(logo_path))
    _render_cards(apps)

    st.markdown(
        "<div style='text-align:center;color:rgba(0,0,0,.45);font-size:.85rem;margin:22px 0 10px;'>"
        "© FC Den Bosch • Internal tools"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
