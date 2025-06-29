# CSV/Excelからの質問項目インポートガイド

このガイドでは、スプレッドシート（CSV/Excel）を使って質問項目を効率的に登録する方法を説明します。

## 概要

大量の質問項目を手動でYAMLファイルに入力する代わりに、スプレッドシートで作成してから自動変換できます。

## 手順

### 1. テンプレートファイルを使用する

プロジェクトルートにある `template.csv` をコピーして使用してください。

```bash
cp template.csv my_questions.csv
```

### 2. CSVファイルの列の説明

| 列名 | 必須 | 説明 | 例 |
|------|------|------|-----|
| category | ✅ | カテゴリキー | access_control, data_control |
| order | ✅ | カテゴリ内での順序 | 10, 20, 30 |
| text_ja | ✅ | 日本語の質問文 | 多要素認証を必須にしていますか？ |
| text_en | | 英語の質問文 | Do you require MFA? |
| type | | 質問タイプ | text (デフォルト) |
| depends_on | | 依存する質問のUID | 000001,000002 (カンマ区切り) |
| tags | | タグ | security,mfa (カンマ区切り) |
| version | | バージョン | 2025-06-24 (デフォルト: 今日の日付) |

### 3. スプレッドシートで編集

**Google スプレッドシート、Excel、LibreOffice Calc** などで編集できます：

1. CSVファイルを開く
2. 各行に質問項目を入力
3. CSVとして保存

### 4. YAMLファイルに変換

CSVファイルを作成したら、以下のコマンドで変換します：

```bash
python scripts/csv_to_yaml.py my_questions.csv
```

### 5. インデックスを更新

新しい質問項目が追加されたら、インデックスを更新します：

```bash
python scripts/build_index.py
```

## 利用可能なカテゴリ

現在利用可能なカテゴリは `categories.yaml` で確認できます：

- `access_control`: アクセス制御
- `data_control`: データ管理

## 注意事項

- **UID は自動生成されます** - 手動で指定する必要はありません
- **空の行はスキップされます** - categoryまたはtext_jaが空の場合
- **既存ファイルは上書きされません** - 新しいUIDが自動生成されます
- **依存関係やタグは複数指定可能** - カンマ区切りで入力してください
- **カテゴリ検証が行われます** - `categories.yaml`に定義されていないカテゴリがあるとエラーになります

## 例

```csv
category,order,text_ja,text_en,type,depends_on,tags,version
access_control,10,多要素認証を必須にしていますか？,Do you require MFA?,text,,security mfa,2025-06-24
access_control,20,パスワードポリシーを設定していますか？,Do you have password policies?,text,,security password,2025-06-24
data_control,10,データのバックアップを取っていますか？,Do you backup your data?,text,,backup,2025-06-24
```

## トラブルシューティング

### エラー: ファイルが見つかりません
```bash
# ファイルパスを確認してください
ls -la my_questions.csv
```

### エラー: 未定義カテゴリが含まれています
```
エラー: 以下の未定義カテゴリが含まれています:
  - security_policy
  - compliance
```

このエラーが発生した場合：

1. **既存カテゴリを使用する**: `categories.yaml`で定義済みのカテゴリに変更
2. **新しいカテゴリを追加する**: `categories.yaml`に新しいカテゴリを追加してから変換

#### 新しいカテゴリの追加方法
```yaml
# categories.yamlに追加
- key: security_policy
  order: 30
  name_ja: セキュリティポリシー
  name_en: Security Policy
  description: セキュリティポリシーに関する管理項目。
```

### 文字化け
CSVファイルをUTF-8エンコーディングで保存してください。 