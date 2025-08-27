# ポモドーロタイマーWebアプリ アーキテクチャ案

## 1. 概要

本アプリはFlask（Python）をバックエンド、HTML/CSS/JavaScriptをフロントエンドとしたWebベースのポモドーロタイマーです。添付UIモックのようなモダンなデザインと、進捗管理機能を備えます。

---

## 2. 構成

### ディレクトリ構成例

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                # Flaskアプリ本体
├── services/             # バックエンドロジック分離用
│   └── progress_manager.py
├── templates/
│   └── index.html        # メインページ
├── static/
│   ├── css/
│   │   └── style.css     # スタイルシート
│   └── js/
│       ├── timer.js      # タイマーのロジック
│       └── timer.test.js # JSロジックのテスト
├── data/                 # 進捗データ保存用（必要なら）
│   └── progress.json
├── tests/                # Pythonユニットテスト
│   ├── test_app.py
│   └── test_progress_manager.py
└── ...（既存ファイル）
```

---

## 3. バックエンド（Flask/Python）

- タイマーや進捗管理のロジックは`services/`配下に分離し、Flaskルートから独立させる。
- `/`：トップページ（index.htmlを返す）
- `/api/progress`：進捗データの取得・保存API（GET/POST）
- 進捗データはファイル（例：JSON）またはDBで管理。依存性注入でテスト時はモックやインメモリ実装も可能に。
- APIレスポンスは一貫したJSON形式。
- テスト用設定ファイルや環境変数で挙動を切り替えやすくする。

---

## 4. フロントエンド（HTML/CSS/JavaScript）

- タイマーのカウントダウン・UI更新はJSで実装。
- タイマーや進捗計算などのロジックは関数として分離し、UI操作部分と分ける。
- fetch/AJAXのAPI通信はラッパー関数にまとめ、テスト時はモックしやすくする。
- Jest等でJSロジックのユニットテストを実施。
- UIは添付画像のような円形プログレスバーやグラデーションをCSS/JSで実装。

---

## 5. ユニットテスト容易化の工夫

- ロジックとUI/ルーティングの分離
- 依存性注入・モック化しやすい設計
- 一貫したAPI設計
- テスト用ディレクトリ・設定の用意
- Python: pytest/unittest、JavaScript: Jest/Mocha などを利用

---

## 6. 実装ステップ例

1. Flaskの最小構成でindex.htmlを表示
2. HTML/CSSでUIモックを再現
3. JSでタイマー・円形プログレスバー実装
4. 進捗データのAPI設計・実装
5. 進捗データの保存・取得ロジック追加
6. 必要に応じてユーザー管理や永続化を拡張

---

## 7. 補足

- タイマー自体はクライアントサイドで管理し、進捗データのみサーバーで管理することでシンプルかつ拡張性の高い設計とする。
- 今後の拡張（ユーザー管理、DB化など）も見据えた構成。
