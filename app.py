# app.py
from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


def _b64_image(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def _render_header(logo_b64: str) -> None:
    st.markdown(
        f"""
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

          /* Page */
          .stApp {{
            background: #F6F9FC;
            color: var(--text);
          }}

          /* Remove extra top padding */
          section.main > div {{
            padding-top: 0rem;
          }}

          /* Header */
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

          /* Title block under header */
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

          /* Card grid */
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

          /* Clickable card */
          a.app-card {{
            text-decoration: none !important;
            color: inherit !important;
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

          /* Hide Streamlit chrome (optional, keep if you want cleaner portal) */
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
          <h1>FC Den Bosch • App Portal</h1>
          <p>Select an application to launch</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_cards(apps: list[dict[str, str]]) -> None:
    cards_html = ['<div class="card-grid">']
    for app in apps:
        title = app["title"]
        subtitle = app["subtitle"]
        url = app["url"]
        cards_html.append(
            f"""
            <a class="app-card" href="{url}" target="_self" rel="noopener noreferrer">
              <div class="app-card-inner">
                <div class="app-card-title">{title}</div>
                <div class="app-card-subtitle">{subtitle}</div>
                <div class="app-card-cta"><span class="dot"></span> Open app</div>
              </div>
            </a>
            """
        )
    cards_html.append("</div>")
    st.markdown("\n".join(cards_html), unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="FC Den Bosch Portal", page_icon="🧭", layout="wide")

    # Update these URLs + labels
    apps = [
        {"title": "App 1", "subtitle": "Short description of what it does.", "url": "https://your-app-1.streamlit.app/"},
        {"title": "App 2", "subtitle": "Short description of what it does.", "url": "https://your-app-2.streamlit.app/"},
        {"title": "App 3", "subtitle": "Short description of what it does.", "url": "https://your-app-3.streamlit.app/"},
        {"title": "App 4", "subtitle": "Short description of what it does.", "url": "https://your-app-4.streamlit.app/"},
        {"title": "App 5", "subtitle": "Short description of what it does.", "url": "https://your-app-5.streamlit.app/"},
        {"title": "App 6", "subtitle": "Short description of what it does.", "url": "https://your-app-6.streamlit.app/"},
    ]

    logo_path = Path(__file__).parent / "assets" / "fc_den_bosch_logo.png"
    if not logo_path.exists():
        st.error(f"Logo not found at: {logo_path}. Add it to your repo and redeploy.")
        st.stop()

    _render_header(_b64_image(logo_path))

    container = st.container()
    with container:
        _render_cards(apps)

    st.markdown(
        "<div style='text-align:center;color:rgba(0,0,0,.45);font-size:.85rem;margin:22px 0 10px;'>"
        "© FC Den Bosch • Internal tools"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
