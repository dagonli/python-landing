#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时监控百度伊朗局势页面
3分钟刷新一次，检测新增内容并发送通知
"""

import time
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import hashlib
import shutil

# 监控配置
MONITOR_URL = "https://events.baidu.com/search/vein?platform=pc&record_id=793253&query=%E4%BC%8A%E6%9C%97%E5%B1%80%E5%8A%BF&srcid=50367"
CHECK_INTERVAL = 600  # 3分钟
# 默认保存在脚本同目录，支持用环境变量覆盖
DEFAULT_HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "iran_situation_history.json",
)
HISTORY_FILE = os.getenv("IRAN_MONITOR_HISTORY_FILE", DEFAULT_HISTORY_FILE)
NOTIFICATION_CHANNEL = "feishu"

# 发送通知函数
def send_notification(title, content) -> bool:
    """通过飞书发送通知"""
    try:
        import subprocess
        if shutil.which("openclaw") is None:
            print("通知发送失败：命令 `openclaw` 未找到（请检查 PATH 或安装）。")
            return False
        msg_text = f"🔔 **伊朗局势新增消息** 🔔\n\n**时间**: {title}\n**内容**: {content}\n\n**查看详情**: [百度伊朗局势专题页面](https://events.baidu.com/search/vein?platform=pc&record_id=793253&query=%E4%BC%8A%E6%9C%97%E5%B1%80%E5%8A%BF&srcid=50367)\n\n---\n⏰ 监控脚本自动发送 (每3分钟检查一次)"
        cmd = [
            "openclaw", "message", "send",
            "--channel", NOTIFICATION_CHANNEL,
            "--target", "user:ou_9728c0cff9812fa42792defac38658a1",
            "--message", msg_text
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"通知发送成功: {title}")
            return True
        else:
            print(f"通知发送失败: {result.stderr}")
            return False

    except Exception as e:
        print(f"发送通知时出错: {e}")
        return False


# 获取网页内容
def get_page_content():
    """获取页面内容并解析"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        response = requests.get(MONITOR_URL, headers=headers, timeout=30)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        # 解析消息列表
        messages = []

        # 查找所有消息条目 - 使用正确的HTML结构
        content_div = soup.find("div", class_="infinite-list-container")
        if content_div:
            list_div = content_div.find("div", class_="list")
            if list_div:
                items = list_div.find_all("div", class_="item")
                print(f"找到 {len(items)} 个消息项")

                for item in items:
                    # 优先使用 DOM 结构解析，避免页面对中文做“反爬变体字符”导致正则失效
                    time_el = item.find("span", class_="time")
                    content_el = item.find("a", class_="content-link") or item.find("div", class_="c-text")
                    label_el = item.find("span", class_="label")

                    time_str = (time_el.get_text(strip=True) if time_el else "").strip()
                    content = (content_el.get_text(" ", strip=True) if content_el else "").strip()
                    label_text = (label_el.get_text(strip=True) if label_el else "").strip()

                    # 若 DOM 解析不全，再回退到纯文本正则提取
                    if not time_str or not content:
                        item_text = item.get_text(" ", strip=True)
                        time_pattern = re.compile(
                            r"(刚刚|\d+\s*分钟前|\d+\s*小时前|(?:今天|昨天|明天)?\s*\d{1,2}:\d{2})"
                        )
                        time_match = time_pattern.search(item_text)
                        if time_match:
                            time_str = time_str or time_match.group(1).strip()
                            content = content or item_text[time_match.end():].strip()

                    # 有些条目会带“新”标签（或反爬后的等价字符），尽量从内容里去掉
                    if label_text:
                        content = content.replace(label_text, " ")
                    content = re.sub(r"^(新\s*)+", "", content).strip()
                    content = _normalize_text(content)

                    if time_str and content and len(content) > 5:
                        messages.append({"time": time_str, "content": content})

                print(f"成功解析出 {len(messages)} 条消息")

        if not messages:
            # 如果没有找到预期的结构，使用备用解析方法
            print("未找到预期的消息结构，使用备用解析方法")
            text = soup.get_text()
            patterns = [
                r"((?:今天|昨天)\s+\d{1,2}:\d{1,2})\s+([^\n]+)",
                r"(\d{4}年\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{1,2})\s+([^\n]+)",
                r"(\d+\s*小时前|\d+\s*分钟前|刚刚)\s+([^\n]+)"
            ]

            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    time_str, content = match
                    if content and len(content.strip()) > 5:
                        messages.append({
                            "time": time_str.strip(),
                            "content": content.strip()
                        })

        return messages

    except Exception as e:
        print(f"获取页面内容出错: {e}")
        return []


# 加载历史记录
def _normalize_text(text):
    """压缩空白字符，避免格式差异导致重复判定失败"""
    return re.sub(r"\s+", " ", (text or "")).strip()


def build_message_key(msg):
    """构建消息唯一键（时间 + 内容）"""
    time_part = _normalize_text(msg.get("time", ""))
    content_part = _normalize_text(msg.get("content", ""))
    raw_key = f"{time_part}|{content_part}"
    return hashlib.sha1(raw_key.encode("utf-8")).hexdigest()


def load_history():
    """加载历史状态，兼容旧版 list 格式"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 兼容旧格式：直接保存消息数组
            if isinstance(data, list):
                seen_keys = [build_message_key(msg) for msg in data]
                return {"messages": data, "seen_keys": seen_keys}

            if isinstance(data, dict):
                messages = data.get("messages", [])
                seen_keys = data.get("seen_keys", [])

                if not seen_keys and messages:
                    seen_keys = [build_message_key(msg) for msg in messages]

                return {"messages": messages, "seen_keys": seen_keys}
        except Exception as e:
            print(f"加载历史记录出错: {e}")
    return {"messages": [], "seen_keys": []}


# 保存历史记录
def save_history(messages, seen_keys):
    """保存历史状态（最近消息 + 全量已见键）"""
    try:
        # 防止 seen_keys 无限制增长
        seen_keys = seen_keys[-20000:]
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "messages": messages,
                    "seen_keys": seen_keys
                },
                f,
                ensure_ascii=False,
                indent=2
            )
    except Exception as e:
        print(f"保存历史记录出错: {e}")


# 检测新增内容
def detect_new_messages(current_messages, seen_keys):
    """检测新增消息"""
    new_messages = []
    seen_set = set(seen_keys)

    for msg in current_messages:
        key = build_message_key(msg)
        if key not in seen_set:
            new_messages.append(msg)

    return new_messages


# 主监控函数
def main():
    print(f"启动监控脚本 - 监控页面: {MONITOR_URL}")
    print(f"刷新间隔: {CHECK_INTERVAL}秒")
    print("=" * 50)

    # 初始化历史记录
    history_state = load_history()
    history = history_state.get("messages", [])
    seen_keys = history_state.get("seen_keys", [])

    if not history and not seen_keys:
        print("首次运行，获取当前内容作为历史记录...")
        current = get_page_content()
        print(f"解析到的原始消息数量: {len(current)}")
        if current:
            print("解析到的消息列表:")
            for i, msg in enumerate(current):
                print(f"  {i+1}. {msg['time']} - {msg['content']}")
        seen_keys = [build_message_key(msg) for msg in current]
        save_history(current, seen_keys)
        print(f"已获取 {len(current)} 条初始记录")
        print()

    while True:
        try:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - 检查更新...")

            current = get_page_content()

            if current:
                print(f"获取到 {len(current)} 条消息")
                history_state = load_history()
                seen_keys = history_state.get("seen_keys", [])
                new_messages = detect_new_messages(current, seen_keys)

                if new_messages:
                    print(f"发现 {len(new_messages)} 条新增消息!")

                    seen_set = set(seen_keys)
                    for msg in new_messages:
                        print(f"[新增] {msg['time']} - {msg['content']}")
                        msg_key = build_message_key(msg)
                        if msg_key in seen_set:
                            continue

                        # 发送通知：仅在成功后才标记为已见过
                        ok = send_notification(msg['time'], msg['content'])
                        if ok:
                            seen_keys.append(msg_key)
                            seen_set.add(msg_key)
                else:
                    print("暂无新增消息")

                # 更新历史记录：只保存 messages 快照，seen_keys 代表“已成功推送”的消息指纹
                save_history(current, seen_keys)
            else:
                print("未获取到有效内容")

            print(f"下次检查: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + CHECK_INTERVAL))}")
            print()

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"监控过程出错: {e}")
            import traceback
            print("详细错误信息:")
            print(traceback.format_exc())
            print(f"将在 {CHECK_INTERVAL} 秒后重试")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
