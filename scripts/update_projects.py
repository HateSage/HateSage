"""Rewrite the Latest Projects table in README.md from HateSage's public repos."""
import json
import os
import re
import urllib.request

USER = "HateSage"
SKIP = {USER.lower()}
MAX = 8

req = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?per_page=100&sort=created&direction=desc",
    headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
             "Accept": "application/vnd.github+json"},
)
repos = json.load(urllib.request.urlopen(req))
repos = [r for r in repos if not r["fork"] and not r["archived"]
         and r["name"].lower() not in SKIP and r.get("description")][:MAX]

rows = ["| Project | What it does | ⭐ |", "|---|---|---|"]
for r in repos:
    name = r["name"].replace("-", " ").title()
    desc = r["description"].replace("|", "/")
    rows.append(f"| 🚀 [**{name}**]({r['html_url']}) | {desc} | {r['stargazers_count']} |")
table = "\n".join(rows)

path = "README.md"
text = open(path, encoding="utf-8").read()
text = re.sub(r"<!-- PROJECTS:START -->.*?<!-- PROJECTS:END -->",
              f"<!-- PROJECTS:START -->\n{table}\n<!-- PROJECTS:END -->",
              text, flags=re.S)
open(path, "w", encoding="utf-8").write(text)
print(table)