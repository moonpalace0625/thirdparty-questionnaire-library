# 準備中

# thirdparty-questionnaire-library

第三者／ベンダー評価に必要な **汎用質問票** （一般的に「セキュリティチェックシート」と呼ばれます）を、  
共同メンテナンスするオープンソース・プロジェクトです。  
セキュリティだけに留まらず、データ管理・コンプライアンス・運用リスクなど  
企業間取引で頻出するチェック項目を 1 か所に集約することを目的としています。

---

## なぜ作るのか 🚀

| 従来の課題 | 本プロジェクトのアプローチ |
|------------|---------------------------|
| xxxx | yyyy |


---

## ディレクトリ構成

.<br> 
├ categories.yaml # カテゴリのマスタ（順序・表示名）<br> 
├ questions/ # 質問1件=1YAML（uid.yml）<br> 
│ ├ 000001.yml<br> 
│ ├ 000002.yml<br> 
│ └ ...<br> 
├ scripts/<br> 
│ └ build_index.py # INDEX.md / Excel 生成スクリプト<br> 
├ docs/<br> 
│ └ INDEX.md # 自動生成された一覧（✏️リンク付き）<br> 
└ .github/workflows/<br> 
└ ci.yml # Lint & INDEX 自動更新 CI<br> 

---

## データモデル（主要フィールド）

| フィールド | 用途 | 例 |
|------------|------|----|
| `uid` | リポジトリ全体で一意な 6 桁 ID | `"000123"` |
| `category` | 質問が属するカテゴリ（slug） | `access_control` |
| `order` | **カテゴリ内** 表示順（4 桁・飛び番推奨） | `1070` |
| `text_ja` / `text_en` | 質問文（日・英） | — |
| `depends_on` | 先行する `uid` の配列（カテゴリ跨ぎ可） | `["000045"]` |
| その他 | `type`, `tags`, `version` など | 任意 |

カテゴリそのものの順序や表示名は **`categories.yaml`** で一元管理します。

---

## 参加方法 ✍️

### 🔧 既存質問の修正

1. **[docs/INDEX.md](docs/INDEX.md)** を開き、該当行の ✏️ をクリック  
2. GitHub上で該当YAMLファイルが開かれるので「Edit this file」をクリック  
3. 質問文や設定を修正  
4. **Propose changes → Create Pull Request**  

### ➕ 新規質問の追加

1. **[questions/](questions/)** ディレクトリを開く  
2. **Add file → Create new file** をクリック  
3. ファイル名を `000XXX.yml` 形式で入力（例：`000010.yml`）  
4. 以下のテンプレートに従ってYAMLを記述：

```yaml
uid: '000010'
category: access_control  # categories.yamlに存在するキー
order: 100               # カテゴリ内での表示順（4桁推奨）
text_ja: あなたの質問文をここに記載してください
text_en: Your question text here (optional)
type: text               # text, select, number など
depends_on: []           # 依存する質問のuid配列（例：['000001']）
tags: []                 # 任意のタグ（例：[audit, compliance]）
version: '2025-01-15'    # 作成日
```

5. **Propose new file → Create Pull Request**  

### 📋 共通手順

4. CI が Lint と INDEX 再生成を行い、ステータスが表示されます  
5. レビュー後 **Merge** されると main ブランチに即反映されます

### PR チェックリスト

- `uid` は 6 桁数値で重複なし  
- `category` は `categories.yaml` に存在  
- `order` はカテゴリ内で重複なし & 4 桁推奨  
- `depends_on` の `uid` が存在し、循環がない  
- 変更理由（背景）が PR 説明に記載されている

---

## CI / 自動生成フロー

| ステップ | ツール | 成果 |
|----------|--------|------|
| Lint / スキーマ検証 | PyYAML | 構造エラーの検知 |
| INDEX ビルド | `scripts/build_index.py` | `docs/INDEX.md` を再生成 |
| (任意) Excel 出力 | openpyxl | `artifacts/questionnaire.xlsx` |

`main` への push ／ PR 毎に実行され、  
変更があれば bot が `chore: auto-update index` をコミットします。

---

## ロードマップ 🗺

  - [ ] GitHub Issue/PR テンプレートの作成
- [ ] GitHub Pages (MkDocs + DataTables) で検索 UI  
- [ ] Excel / CSV エクスポート  
- [ ] プロファイル別サブセット（SaaS / Finance など）  
- [ ] 依存関係グラフの自動可視化（mermaid 出力）

---

## ライセンス

- **質問テキスト・カテゴリ説明**: Creative Commons **CC-BY-4.0**  
- **スクリプト・CI 定義**: MIT License  

詳細は [`LICENSE`](LICENSE) を参照してください。

---

## 謝辞

xxxx
