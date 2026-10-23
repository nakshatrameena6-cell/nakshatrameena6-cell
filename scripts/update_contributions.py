import urllib.request
import re
from datetime import datetime
import os

url = 'https://github.com/users/nakshatrameena6-cell/contributions'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

table_rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
day_rows = []
for r in table_rows[1:8]:
    tds = re.findall(r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([^"]+)"', r)
    day_rows.append(tds)

num_weeks = max(len(r) for r in day_rows)

level_colors = {
    '0': '#111c44',
    '1': '#3b4ba5',
    '2': '#8b4cd6',
    '3': '#d946a4',
    '4': '#fb7185',
    '5': '#fde047',
}

svg_w = 1060
svg_h = 320

gap_x = 16.5
gap_y = 15
sq_size = 11.5

x_start = 116
y_start = 106

y_mon = y_start + 1 * gap_y + 9
y_wed = y_start + 3 * gap_y + 9
y_fri = y_start + 5 * gap_y + 9

month_cols = {}
for w in range(num_weeks):
    for r in range(7):
        if w < len(day_rows[r]):
            date_str, lvl = day_rows[r][w]
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            m_name = dt.strftime("%b")
            if dt.day <= 7 and m_name not in month_cols:
                month_cols[m_name] = w

months_svg = []
for m_name, col_idx in month_cols.items():
    mx = x_start + col_idx * gap_x
    months_svg.append(f'<text x="{mx:.1f}" y="90">{m_name}</text>')

months_header_str = "\\n    ".join(months_svg)

squares_list = []
for w in range(num_weeks):
    for r in range(7):
        if w < len(day_rows[r]):
            date_str, lvl = day_rows[r][w]
            color = level_colors.get(lvl, level_colors['0'])
            opacity = "0.5" if lvl == '0' else "1"
            sx = x_start + w * gap_x
            sy = y_start + r * gap_y
            squares_list.append(
                f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sq_size}" height="{sq_size}" rx="2.5" fill="{color}" fill-opacity="{opacity}"><title>{date_str}: level {lvl}</title></rect>'
            )

all_squares_svg = "\\n    ".join(squares_list)

grid_end_x = x_start + (num_weeks - 1) * gap_x + sq_size
legend_x = grid_end_x - 146

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}" role="img" aria-labelledby="title description">
  <title id="title">Nakshatra S.V Contribution Activity</title>
  <desc id="description">GitHub contribution heatmap calendar in cosmic mission control theme for Nakshatra S.V.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#02051d"/>
      <stop offset=".48" stop-color="#071033"/>
      <stop offset="1" stop-color="#030718"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="soft"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="shadow">
      <feDropShadow dx="0" dy="8" stdDeviation="14" flood-color="#00031b" flood-opacity=".7"/>
    </filter>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&amp;display=swap');
      .font {{
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }}
      .card {{
        fill: #071033;
        fill-opacity: .90;
        stroke: #314475;
        stroke-opacity: .85;
        stroke-width: 1.5;
      }}
    </style>
  </defs>

  <!-- Container Card -->
  <rect x="8" y="8" width="{svg_w - 16}" height="{svg_h - 16}" rx="14" class="card" filter="url(#shadow)"/>

  <!-- Card Header -->
  <g class="font">
    <text x="50" y="52">
      <tspan font-size="25" font-weight="700" fill="#f4f4ff" letter-spacing="0.5px">Contribution Activity</tspan>
      <tspan font-size="15" font-weight="400" fill="#8890bc" dx="16">|  Small commits, a brighter galaxy</tspan>
    </text>
  </g>

  <!-- Month Labels -->
  <g class="font" font-size="12.5" font-weight="500" fill="#8890bc">
    {months_header_str}
  </g>

  <!-- Day Labels (Mon, Wed, Fri) -->
  <g class="font" font-size="12.5" font-weight="500" fill="#8890bc">
    <text x="74" y="{y_mon:.1f}">Mon</text>
    <text x="74" y="{y_wed:.1f}">Wed</text>
    <text x="74" y="{y_fri:.1f}">Fri</text>
  </g>

  <!-- Real Contribution Squares -->
  <g>
    {all_squares_svg}
  </g>

  <!-- Legend (Less to More) -->
  <g class="font" transform="translate({legend_x:.1f} 224)">
    <text x="0" y="9" font-size="12" fill="#8890bc">Less</text>
    <rect x="34" y="0" width="10" height="10" rx="2" fill="#111c44" fill-opacity="0.5"/>
    <rect x="48" y="0" width="10" height="10" rx="2" fill="#3b4ba5"/>
    <rect x="62" y="0" width="10" height="10" rx="2" fill="#8b4cd6"/>
    <rect x="76" y="0" width="10" height="10" rx="2" fill="#d946a4"/>
    <rect x="90" y="0" width="10" height="10" rx="2" fill="#fb7185"/>
    <rect x="104" y="0" width="10" height="10" rx="2" fill="#fde047"/>
    <text x="120" y="9" font-size="12" fill="#8890bc">More</text>
  </g>

  <!-- Bottom Pill Card with Glowing Star and Quote -->
  <rect x="50" y="248" width="{svg_w - 100}" height="46" rx="8" fill="#091338" stroke="#1d2e68" stroke-width="1.2"/>
  <g transform="translate(76 271)">
    <path d="M0-9l2.5 6.5 6.5 2.5-6.5 2.5-2.5 6.5-2.5-6.5-6.5-2.5 6.5-2.5z" fill="#ffe49a" filter="url(#glow)"/>
    <circle r="9" fill="#ffd08d" opacity="0.35" filter="url(#soft)"/>
  </g>
  <text x="100" y="277" class="font" font-size="16" font-weight="500" fill="#c4c8f8">Consistency creates its own gravity.</text>
</svg>
'''

target_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'contribution-activity.svg')
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print("Updated assets/contribution-activity.svg successfully!")
