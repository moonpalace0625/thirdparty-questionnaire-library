#!/usr/bin/env python3
"""
CSVファイルからYAMLファイルを生成するスクリプト

使用方法:
python scripts/csv_to_yaml.py input.csv

CSVファイルの列:
- category: カテゴリキー (例: access_control)
- order: 順序 (例: 10)
- text_ja: 日本語の質問文
- text_en: 英語の質問文 (空でも可)
- type: タイプ (例: text)
- depends_on: 依存関係 (カンマ区切りで複数指定可、空でも可)
- tags: タグ (カンマ区切りで複数指定可、空でも可)
- version: バージョン (例: 2025-06-24)
"""

import csv
import yaml
import pathlib
import sys
from datetime import datetime

def get_next_uid(questions_dir):
    """次のUIDを生成する"""
    existing_files = list(questions_dir.glob('*.yml'))
    if not existing_files:
        return '000001'
    
    # 既存のファイルから最大のUIDを取得
    max_uid = 0
    for file in existing_files:
        try:
            uid_str = file.stem
            uid_num = int(uid_str)
            max_uid = max(max_uid, uid_num)
        except ValueError:
            continue
    
    return f"{max_uid + 1:06d}"

def parse_list_field(value):
    """カンマ区切りの文字列をリストに変換"""
    if not value or value.strip() == '':
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

def csv_to_yaml(csv_file_path):
    """CSVファイルをYAMLファイルに変換"""
    base_dir = pathlib.Path(__file__).resolve().parents[1]
    questions_dir = base_dir / 'questions'
    questions_dir.mkdir(exist_ok=True)
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # 必須フィールドのチェック
            if not row.get('category') or not row.get('text_ja'):
                print(f"警告: カテゴリまたは日本語テキストが空の行をスキップします: {row}")
                continue
            
            # 次のUIDを生成
            uid = get_next_uid(questions_dir)
            
            # YAMLデータを構築
            yaml_data = {
                'uid': uid,
                'category': row['category'].strip(),
                'order': int(row['order']) if row['order'].strip() else 10,
                'text_ja': row['text_ja'].strip(),
                'text_en': row.get('text_en', '').strip(),
                'type': row.get('type', 'text').strip(),
                'depends_on': parse_list_field(row.get('depends_on', '')),
                'tags': parse_list_field(row.get('tags', '')),
                'version': row.get('version', datetime.now().strftime('%Y-%m-%d')).strip()
            }
            
            # YAMLファイルに保存
            yaml_file_path = questions_dir / f"{uid}.yml"
            with open(yaml_file_path, 'w', encoding='utf-8') as yamlfile:
                yaml.dump(yaml_data, yamlfile, 
                         default_flow_style=False, 
                         allow_unicode=True, 
                         sort_keys=False)
            
            print(f"作成しました: {yaml_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python scripts/csv_to_yaml.py input.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not pathlib.Path(csv_file).exists():
        print(f"エラー: ファイルが見つかりません: {csv_file}")
        sys.exit(1)
    
    csv_to_yaml(csv_file)
    print("変換完了!") 