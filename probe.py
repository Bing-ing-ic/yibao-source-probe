# -*- coding: utf-8 -*-
"""从 GitHub Actions runner 探测医保政策抓取源可达性；仅记录状态码/耗时/标题，不抓正文、不写库。"""
import urllib.request, ssl, time, re, socket, sys

socket.setdefaulttimeout(12)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
TARGETS = [
    ("国家局-首页", "https://www.nhsa.gov.cn"),
    ("国家局-政策文件", "https://www.nhsa.gov.cn/col/col104/index.html"),
    ("国家局-政策解读", "https://www.nhsa.gov.cn/col/col105/index.html"),
    ("国家局-通知公告", "https://www.nhsa.gov.cn/col/col109/index.html"),
    ("云南省局-首页", "https://ylbz.yn.gov.cn"),
    ("云南省局-政策文件", "https://ylbz.yn.gov.cn/zfxxgk/zcwj/qtwj/"),
    ("玉溪市-首页", "http://www.yuxi.gov.cn"),
    ("玉溪市-栏目列表", "http://www.yuxi.gov.cn/yxgovfront/newDepartmentContentds.jspx?channelId=16576&pageNo=1&path=yxszfxxgk"),
    ("澄江市-首页", "https://www.yncj.gov.cn"),
    ("江川区-首页", "https://www.ynjc.gov.cn"),
    ("红塔区-首页", "https://www.hongta.gov.cn"),
    ("通海县-首页", "https://www.tonghai.gov.cn"),
    ("华宁县-首页", "https://www.huaning.gov.cn"),
    ("元江县-首页", "https://www.yjx.gov.cn"),
]

results = []
for name, url in TARGETS:
    t0 = time.time()
    status = "ERR"
    size = 0
    title = ""
    note = ""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
            data = r.read(60000)
            status = r.status
            size = len(data)
            txt = data.decode("utf-8", "ignore")
            m = re.search(r"<title>(.*?)</title>", txt, re.S | re.I)
            title = re.sub(r"\s+", " ", m.group(1)).strip()[:40] if m else ""
    except Exception as e:
        note = repr(e)[:140]
    dt = time.time() - t0
    results.append((name, status, dt, size, title, note))
    print(f"{name}\t{status}\t{dt:.2f}s\t{size}B\t{title}\t{note}")

ok = sum(1 for x in results if x[1] == 200)
print(f"\n可达 {ok}/{len(results)}")

lines = ["# 探测结果（GitHub Actions ubuntu runner）", "", f"可达 {ok}/{len(results)}（200 为可访问）", "",
         "| 站点 | 状态 | 耗时 | 字节 | 标题 | 备注 |", "|---|---|---|---|---|---|"]
for name, status, dt, size, title, note in results:
    lines.append(f"| {name} | {status} | {dt:.2f}s | {size} | {title} | {note} |")
with open("result.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

sys.exit(0)
