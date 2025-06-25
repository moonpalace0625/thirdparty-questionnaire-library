#!/usr/bin/env python3
"""
ExcelファイルからYAMLファイルを生成するスクリプト

使用方法:
python scripts/excel_to_yaml.py input.xlsx [sheet_name]

必要なライブラリ:
pip install openpyxl pandas

Excelファイルの列はCSVと同じ形式:
- category: カテゴリキー (例: access_control)
- order: 順序 (例: 10)
- text_ja: 日本語の質問文
- text_en: 英語の質問文 (空でも可)
- type: タイプ (例: text)
- depends_on: 依存関係 (カンマ区切りで複数指定可、空でも可)
- tags: タグ (カンマ区切りで複数指定可、空でも可)
- version: バージョン (例: 2025-06-24)
"""

import pandas as pd
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
    if pd.isna(value) or str(value).strip() == '':
        return []
    return [item.strip() for item in str(value).split(',') if item.strip()]

def excel_to_yaml(excel_file_path, sheet_name=None):
    """ExcelファイルをYAMLファイルに変換"""
    base_dir = pathlib.Path(__file__).resolve().parents[1]
    questions_dir = base_dir / 'questions'
    questions_dir.mkdir(exist_ok=True)
    
    try:
        # Excelファイルを読み込み
        if sheet_name:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(excel_file_path)
        
        print(f"読み込み完了: {len(df)} 行の質問項目")
        
        for index, row in df.iterrows():
            # NaNを空文字列に変換
            row = row.fillna('')
            
            # 必須フィールドのチェック
            if not row.get('category') or not row.get('text_ja'):
                print(f"警告: カテゴリまたは日本語テキストが空の行をスキップします: 行 {index + 2}")
                continue
            
            # 次のUIDを生成
            uid = get_next_uid(questions_dir)
            
            # YAMLデータを構築
            yaml_data = {
                'uid': uid,
                'category': str(row['category']).strip(),
                'order': int(row['order']) if str(row['order']).strip() and str(row['order']).strip() != 'nan' else 10,
                'text_ja': str(row['text_ja']).strip(),
                'text_en': str(row.get('text_en', '')).strip(),
                'type': str(row.get('type', 'text')).strip(),
                'depends_on': parse_list_field(row.get('depends_on', '')),
                'tags': parse_list_field(row.get('tags', '')),
                'version': str(row.get('version', datetime.now().strftime('%Y-%m-%d'))).strip()
            }
            
            # YAMLファイルに保存
            yaml_file_path = questions_dir / f"{uid}.yml"
            with open(yaml_file_path, 'w', encoding='utf-8') as yamlfile:
                yaml.dump(yaml_data, yamlfile, 
                         default_flow_style=False, 
                         allow_unicode=True, 
                         sort_keys=False)
            
            print(f"作成しました: {yaml_file_path} - {yaml_data['text_ja'][:50]}...")
    
    except Exception as e:
        print(f"エラー: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python scripts/excel_to_yaml.py input.xlsx [sheet_name]")
        print("例: python scripts/excel_to_yaml.py questions.xlsx")
        print("例: python scripts/excel_to_yaml.py questions.xlsx 'Sheet1'")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not pathlib.Path(excel_file).exists():
        print(f"エラー: ファイルが見つかりません: {excel_file}")
        sys.exit(1)
    
    try:
        import openpyxl
    except ImportError:
        print("エラー: openpyxl ライブラリが必要です")
        print("インストール: pip install openpyxl pandas")
        sys.exit(1)
    
    excel_to_yaml(excel_file, sheet_name)
    print("変換完了!") 