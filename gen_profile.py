"""neofetch 스타일 프로필 카드(dark_mode.svg / light_mode.svg) 생성.

GitHub Actions에서 매일 돌면서 Uptime이랑 GitHub Stats를 갱신한다.
로컬: GITHUB_TOKEN=$(gh auth token) python gen_profile.py
"""
import datetime as dt
import json
import os
import urllib.request
from html import escape

USER = "haneul-dev"
CODING_SINCE = dt.date(2023, 3, 2)
WIDTH = 59  # 오른쪽 칸 한 줄 글자 수

ASCII = r"""
          \     |     /
       `.  .-'''''-.  .'
     --   /         \   --
     --  |           |  --
          \         /
       .'  '-.___.-'  `.
          /     |     \

    v               v
           v

          .--.
       .-(    )-.          .-.
      (___.__)___)     .-(    )-.
                      (___.__.___)_)

   ~    ~     ~    ~     ~    ~
     ~     ~    ~     ~    ~
   ~    ~     ~    ~     ~    ~

      h a n e u l  =  s k y
""".strip("\n").split("\n")

THEMES = {
    "dark": dict(bg="#161b22", fg="#c9d1d9", key="#7dd3fc", value="#e6edf3",
                 dots="#616e7f", accent="#a5b4fc", art="#7dd3fc"),
    "light": dict(bg="#f6f8fa", fg="#24292f", key="#0369a1", value="#24292f",
                  dots="#8c959f", accent="#4f46e5", art="#0284c7"),
}


def fetch_stats():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    query = """{ user(login: "%s") {
        repositories(ownerAffiliations: OWNER) { totalCount }
        followers { totalCount }
        contributionsCollection {
          totalCommitContributions
          contributionCalendar { totalContributions }
        } } }""" % USER
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {token}"},
    )
    u = json.load(urllib.request.urlopen(req))["data"]["user"]
    c = u["contributionsCollection"]
    return dict(
        repos=u["repositories"]["totalCount"],
        followers=u["followers"]["totalCount"],
        commits=c["totalCommitContributions"],
        contribs=c["contributionCalendar"]["totalContributions"],
    )


def uptime(today):
    y = today.year - CODING_SINCE.year
    m = today.month - CODING_SINCE.month
    d = today.day - CODING_SINCE.day
    if d < 0:
        m -= 1
        d += 30
    if m < 0:
        y -= 1
        m += 12
    return f"{y} years, {m} months, {d} days"


def rows(stats, today):
    s = stats or dict(repos="-", followers="-", commits="-", contribs="-")
    return [
        ("title", "haneul@kang"),
        ("kv", "OS", "macOS, Linux"),
        ("kv", "Uptime", uptime(today)),
        ("kv", "Host", "Dankook Univ. / Software Eng."),
        ("kv", "Kernel", "Backend & AI Engineer"),
        ("kv", "IDE", "IntelliJ IDEA, VSCode, Android Studio"),
        ("blank",),
        ("kv", "Languages.Programming", "Java, Python, Dart, JS, C"),
        ("kv", "Languages.Real", "Korean, English"),
        ("blank",),
        ("kv", "Stack.Backend", "Spring Boot, JPA, MySQL, Redis, Kafka"),
        ("kv", "Stack.AI", "RAG, Qwen2.5, Upstage Solar, Gemini"),
        ("kv", "Stack.Infra", "Docker, AWS, NHN Cloud"),
        ("blank",),
        ("section", "Now"),
        ("kv", "Research", "Multimodal RAG / Evidence Decoder"),
        ("kv", "Status", "Open to work (2027.02 grad)"),
        ("blank",),
        ("section", "GitHub Stats"),
        ("kv", "Repos", f"{s['repos']}  |  Followers: {s['followers']}"),
        ("kv", "Commits (1y)", f"{s['commits']}  |  Contributions: {s['contribs']}"),
    ]


def render(theme, stats, today):
    t = THEMES[theme]
    lh, top, rx = 20, 30, 400
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,Menlo,monospace" '
        f'width="985px" height="450px" font-size="16px">',
        "<style>",
        "@font-face { src: local('Consolas'), local('Consolas Bold'); font-family: 'ConsolasFallback';"
        " font-display: swap; size-adjust: 109%; }",
        f".key {{fill: {t['key']};}} .value {{fill: {t['value']};}} .cc {{fill: {t['dots']};}}",
        f".sec {{fill: {t['accent']}; font-weight: bold;}} .art {{fill: {t['art']};}}",
        "text, tspan {white-space: pre;}",
        "</style>",
        f'<rect width="985px" height="450px" fill="{t["bg"]}" rx="15"/>',
        f'<text x="20" y="{top}" class="art">',
    ]
    for i, line in enumerate(ASCII):
        out.append(f'<tspan x="20" y="{top + i * lh}">{escape(line)}</tspan>')
    out.append("</text>")
    out.append(f'<text x="{rx}" y="{top}" fill="{t["fg"]}">')
    for i, r in enumerate(rows(stats, today)):
        y = top + i * lh
        if r[0] == "title":
            bar = "-" + "—" * (WIDTH - len(r[1]) - 2) + "-"
            out.append(f'<tspan x="{rx}" y="{y}" class="sec">{r[1]}</tspan> {bar}')
        elif r[0] == "section":
            label = f"- {r[1]}"
            bar = "-" + "—" * (WIDTH - len(label) - 2) + "-"
            out.append(f'<tspan x="{rx}" y="{y}" class="sec">{label}</tspan> {bar}')
        elif r[0] == "blank":
            out.append(f'<tspan x="{rx}" y="{y}" class="cc">. </tspan>')
        else:
            _, k, v = r
            keys = k.split(".")
            key_svg = '<tspan class="cc">.</tspan>'.join(f'<tspan class="key">{p}</tspan>' for p in keys)
            ndots = max(WIDTH - 2 - len(k) - 1 - len(v) - 2, 1)
            out.append(
                f'<tspan x="{rx}" y="{y}" class="cc">. </tspan>{key_svg}:'
                f'<tspan class="cc"> {"." * ndots} </tspan><tspan class="value">{escape(v)}</tspan>'
            )
    out.append("</text>")
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    today = dt.date.today()
    stats = fetch_stats()
    here = os.path.dirname(os.path.abspath(__file__))
    for theme in THEMES:
        with open(os.path.join(here, f"{theme}_mode.svg"), "w", encoding="utf-8") as f:
            f.write(render(theme, stats, today))
