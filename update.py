import requests, yaml, os

# 免费源合集（我挑了最稳的7个）
sources = [
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml",
    "https://nodefree.org/dy/2025/11/2025-11-26.yaml",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/clash.yaml",
    "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/main/clash.meta.yml"
]

all_proxies = []

for url in sources:
    try:
        print(f"正在抓取: {url}")
        r = requests.get(url, timeout=20)
        if "proxies" in r.text:
            config = yaml.safe_load(r.text)
            if config and "proxies" in config:
                all_proxies.extend(config["proxies"])
    except Exception as e:
        print(f"失败: {e}")

# 去重（server+port）
seen = set()
unique_proxies = []
for p in all_proxies:
    key = (p.get('server'), p.get('port'))
    if key not in seen and key[0] not in ['DOMAIN', '']:
        seen.add(key)
        unique_proxies.append(p)

# 生成最终配置
final_config = {
    "proxies": unique_proxies,
    "proxy-groups": [
        {
            "name": "🚀 节点选择",
            "type": "select",
            "proxies": [p.get("name", "未命名节点") for p in unique_proxies[:200]]  # 最多200个
        },
        {
            "name": "🌿 自动选择",
            "type": "url-test",
            "proxies": [p.get("name", "未命名节点") for p in unique_proxies[:100]],
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300
        }
    ],
    "rules": ["MATCH,🌿 自动选择"]
}

with open("clash.yaml", "w", encoding="utf-8") as f:
    yaml.dump(final_config, f, allow_unicode=True, sort_keys=False)

print(f"成功！共生成 {len(unique_proxies)} 个节点，已更新 clash.yaml")
