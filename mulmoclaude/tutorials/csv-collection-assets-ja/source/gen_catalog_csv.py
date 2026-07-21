#!/usr/bin/env python3
"""商品カタログ CSV の生成(チュートリアル収録用・seed 固定で再現可能)。

v1: 収録開始時にチャットへドロップする 1,000 行。
v2: 「差し替えると自動更新」ビート用。再入荷 + 新商品 12 件。
生成後に、ライブ収録で AI の回答を検算するための集計サマリを表示する。
"""

import csv
import random
from pathlib import Path

OUT_DIR = Path(__file__).parent
SEED = 20260720

# (ベース商品名, 基準価格) をカテゴリごとに定義
CATALOG = {
    "キッチン用品": [
        ("ステンレスタンブラー", 1400), ("ホーロー両手鍋", 3200), ("シリコン調理スプーン", 700),
        ("木製カッティングボード", 1800), ("計量カップ", 500), ("キッチンタイマー", 900),
        ("ガラス保存容器", 1000), ("オイルボトル", 800), ("ステンレスざる", 1100),
        ("鍋つかみミトン", 600), ("キッチンばさみ", 1200), ("ステンレスピーラー", 650),
        ("珪藻土水切りマット", 1300), ("竹製菜箸", 450),
    ],
    "文房具": [
        ("ゲルインクボールペン", 180), ("A5ノート", 320), ("クリップボード", 600),
        ("蛍光マーカー", 200), ("シャープペンシル", 450), ("マスキングテープ", 250),
        ("事務はさみ", 480), ("ホッチキス", 750), ("付箋セット", 350),
        ("クリアファイル10枚組", 400), ("修正テープ", 280), ("定規セット", 300),
        ("万年筆カートリッジ", 550), ("ダブルクリップ", 220),
    ],
    "インテリア雑貨": [
        ("アロマディフューザー", 3500), ("フォトフレーム", 1500), ("壁掛け時計", 2800),
        ("LEDテーブルランプ", 3200), ("フラワーベース", 2200), ("クッションカバー", 1600),
        ("ラグマット", 5500), ("ウォールシェルフ", 2600), ("キャンドルホルダー", 1300),
        ("観葉植物ポット", 1800), ("ドライフラワースワッグ", 2400), ("ブランケット", 3000),
    ],
    "バス・洗面": [
        ("今治タオル", 1200), ("バスマット", 1500), ("ソープディスペンサー", 900),
        ("歯ブラシスタンド", 500), ("シャワーラック", 1600), ("バスピロー", 1100),
        ("ランドリーバスケット", 1800), ("洗面器", 700), ("バススポンジ", 400),
        ("ヘアドライタオル", 800), ("珪藻土バスマット", 2200),
    ],
    "収納用品": [
        ("収納ボックス", 1300), ("ハンガーラック", 4500), ("仕切りケース", 800),
        ("押入れ収納ケース", 2400), ("ワイヤーバスケット", 1400), ("布団収納袋", 1600),
        ("シューズラック", 2200), ("キャスター付きワゴン", 4800), ("吊り下げ収納", 1200),
        ("書類トレー", 1000),
    ],
    "テーブルウェア": [
        ("磁器プレート", 1400), ("木製カトラリーセット", 1800), ("耐熱グラス", 900),
        ("箸置きセット", 700), ("ランチョンマット", 600), ("蕎麦猪口", 800),
        ("豆皿", 500), ("ティーポット", 2400), ("マグカップ", 1000),
        ("カレー皿", 1200), ("サラダボウル", 1300),
    ],
    "アウトドア": [
        ("折りたたみチェア", 3500), ("LEDランタン", 2800), ("保冷バッグ", 1800),
        ("アルミローテーブル", 4500), ("封筒型寝袋", 6500), ("焚き火台", 8500),
        ("ウォータージャグ", 3200), ("ペグセット", 1500), ("ヘキサタープ", 7500),
        ("クッカーセット", 4200),
    ],
}

CATEGORY_COUNTS = {
    "キッチン用品": 170, "文房具": 160, "インテリア雑貨": 150, "バス・洗面": 130,
    "収納用品": 130, "テーブルウェア": 130, "アウトドア": 130,
}

COLORS = ["ホワイト", "ブラック", "ネイビー", "グレー", "ベージュ", "カーキ", "テラコッタ", "ブルーグレー"]
SIZES = [("S", 0.9), ("M", 1.0), ("L", 1.15)]

FIELDNAMES = ["商品ID", "商品名", "カテゴリ", "価格", "在庫状況", "在庫数"]


def build_variants(base: str, base_price: int) -> list[tuple[str, int]]:
    variants = []
    for color in COLORS:
        for size, mult in SIZES:
            name = f"{base} {color} {size}"
            price = round(base_price * mult / 10) * 10
            variants.append((name, price))
    return variants


def pick_stock(rng: random.Random) -> tuple[str, int]:
    roll = rng.random()
    if roll < 0.87:
        return "在庫あり", rng.randint(10, 120)
    if roll < 0.96:
        return "残りわずか", rng.randint(1, 9)
    return "在庫切れ", 0


def generate_v1() -> list[dict]:
    rng = random.Random(SEED)
    rows = []
    for category, count in CATEGORY_COUNTS.items():
        pool = []
        for base, price in CATALOG[category]:
            pool.extend(build_variants(base, price))
        rng.shuffle(pool)
        for name, price in pool[:count]:
            status, qty = pick_stock(rng)
            rows.append({"商品名": name, "カテゴリ": category, "価格": price,
                         "在庫状況": status, "在庫数": qty})
    rng.shuffle(rows)
    for i, row in enumerate(rows, start=1):
        row["商品ID"] = f"P-{i:04d}"
    return rows


def generate_v2(v1_rows: list[dict]) -> list[dict]:
    """再入荷後: 在庫切れの 6 割が在庫ありに戻り、新商品 12 件が加わる。"""
    rng = random.Random(SEED + 1)
    rows = [dict(r) for r in v1_rows]
    out_of_stock = [r for r in rows if r["在庫状況"] == "在庫切れ"]
    restocked = rng.sample(out_of_stock, k=round(len(out_of_stock) * 0.6))
    for row in restocked:
        row["在庫状況"] = "在庫あり"
        row["在庫数"] = rng.randint(20, 80)
    new_products = [
        ("琺瑯マグカップ 限定カラー", "キッチン用品", 1650),
        ("ステンレスタンブラー 真空断熱 750ml", "キッチン用品", 2200),
        ("リサイクルコットンノート", "文房具", 380),
        ("木軸ボールペン", "文房具", 890),
        ("ペーパーコードバスケット", "インテリア雑貨", 2900),
        ("リネンクッションカバー 45cm", "インテリア雑貨", 2100),
        ("オーガニックコットンタオル", "バス・洗面", 1450),
        ("折りたたみランドリーラック", "収納用品", 3200),
        ("スタッキング収納キューブ", "収納用品", 1500),
        ("美濃焼マグ ペアセット", "テーブルウェア", 2600),
        ("チタンマグカップ", "アウトドア", 3800),
        ("焚き火グローブ", "アウトドア", 1900),
    ]
    for i, (name, category, price) in enumerate(new_products, start=len(rows) + 1):
        rows.append({"商品ID": f"P-{i:04d}", "商品名": name, "カテゴリ": category,
                     "価格": price, "在庫状況": "在庫あり", "在庫数": rng.randint(30, 90)})
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def summarize(label: str, rows: list[dict]) -> None:
    print(f"=== {label}: {len(rows)} 行 ===")
    for status in ["在庫あり", "残りわずか", "在庫切れ"]:
        print(f"  {status}: {sum(1 for r in rows if r['在庫状況'] == status)} 件")
    print(f"  要補充(在庫数≤5): {sum(1 for r in rows if int(r['在庫数']) <= 5)} 件")
    print("  カテゴリ別 件数 / 平均価格 / 在庫切れ:")
    for category in CATEGORY_COUNTS:
        subset = [r for r in rows if r["カテゴリ"] == category]
        avg = sum(r["価格"] for r in subset) / len(subset)
        oos = sum(1 for r in subset if r["在庫状況"] == "在庫切れ")
        print(f"    {category}: {len(subset)} 件 / ¥{avg:,.0f} / 在庫切れ {oos} 件")


def main() -> None:
    v1 = generate_v1()
    v2 = generate_v2(v1)
    write_csv(OUT_DIR / "商品カタログ_v1.csv", v1)
    write_csv(OUT_DIR / "商品カタログ_v2.csv", v2)
    summarize("v1", v1)
    summarize("v2 (再入荷後)", v2)


if __name__ == "__main__":
    main()
