# 第04章：BIMソフトウェアの種類と選定基準
# Chapter 04: Types of BIM Software and Selection Criteria

> **キーワード / Keywords：** Revit / ARCHICAD / Vectorworks / Navisworks / ソフトウェア選定

---

## 学習目標 / Learning Objectives

本章を修了すると、受講者は以下を達成できる：

1. 主要なBIMソフトウェアの特徴と用途を比較説明できる
2. プロジェクト規模・用途に応じたソフトウェア選定基準を適用できる
3. 意匠・構造・設備BIMツールの相互連携方法を理解できる
4. BIMビューアとBIM編集ソフトの違いを説明できる
5. ライセンスコストと導入コストを含めたTCO（総所有コスト）の概念を理解できる

---

## 1. 問題の背景 / Problem Background

BIMソフトウェアは多種多様であり、「どのソフトを選べばよいか」が実務担当者の最初の壁となる。誤ったソフトウェア選定は、後のデータ互換性問題や再学習コストを招く。

---

## 2. 解説 / Explanation

主要BIMソフトウェアは以下のカテゴリに分類される。

【意匠BIM】
- Autodesk Revit：世界シェア最大。日本大手ゼネコン・設計事務所で広く使用。
- ARCHICAD（Graphisoft）：操作性に優れ中小設計事務所で普及。
- Vectorworks：日本の設計事務所で利用者多数。BIMとCADの中間的な使い方が可能。

【構造BIM】
- Tekla Structures：鉄骨・プレキャストコンクリートの詳細モデリングに強み。
- SCIA Engineer：構造解析とBIM連携が得意。

【設備BIM】
- Revit MEP：Revitの設備専用モジュール。意匠Revitとシームレスに連携。
- MagiCAD：Revit上で動作する設備BIMプラグイン。

【干渉チェック・統合】
- Autodesk Navisworks：各BIMモデルを統合してクラッシュ検出と4Dシミュレーションを実施。
- Solibri Model Checker：IFCベースの品質・規則チェックに特化。

【BIMビューア】
- BIMx（Graphisoft）：ARCHICADモデルのモバイル閲覧。
- Autodesk Viewer：ブラウザベースの無料BIMビューア。

---

## 3. 図表 / Figures

【図表：主要BIMソフトウェア比較マトリックス】
（出典：PDF p.46）

![主要BIMソフトウェア比較マトリックス](assets/pages/p046.png)

① 図の説明：Revit・ARCHICAD・Vectorworks・Tekla等を機能・価格・対応分野で比較した表。

② 読み取り方：列（ソフト名）と行（評価項目）の交点で各ソフトの特性を読み取る。

③ 教育上の狙い：プロジェクト条件に応じた適切なソフトウェア選定能力を養う。

④ 実務活用シーン：BIM導入プロジェクトのソフトウェア選定会議の評価シートとして使用する。


---

## 4. アナロジー（類比）/ Analogy

BIMソフトウェア選定はOS選択に似ている。WindowsとMacが異なるエコシステムを持つように、RevitとARCHICADは異なるワークフローと連携ツール群を持つ。プロジェクトの規模・チーム構成・取引先環境を踏まえた戦略的選定が不可欠である。

---

## 5. 実際の失敗事例 / Real Failure Case

【実際の失敗事例】中規模設計事務所がRevitを導入したものの、習得コストが高く既存CADワークフローとの整合が取れず、1年後にARCHICADへ移行した事例がある。移行コストと再教育コストで総額1,500万円超の損失が生じた。事前のパイロットプロジェクトと段階的導入計画の重要性が示された。

---

## 6. 日本の建設文化的背景 / Japanese Construction Culture Notes

日本の大手ゼネコン（鹿島・大成・清水・竹中・大林）はRevitを主軸としているが、中小設計事務所ではARCHICADやVectorworksも多い。元請けが使用ソフトを指定するケースが多く、協力会社は複数ソフトを扱う能力が求められる。

---

## 7. 外国籍技術者へのノート / Notes for Foreign Engineers

外国籍技術者へのノート：日本市場では各ソフトウェアの日本語UIと日本語サポートが選定要因となることが多い。Revitの日本語版は機能的に国際版と同等だが、日本固有のファミリ（部材ライブラリ）が充実している点で優位性がある。

---

## 8. 実務チェックリスト / Practical Checklist

以下の項目を確認・実施すること：

- [ ] BIM実行計画書（BEP）の作成
- [ ] 使用ソフトウェアのバージョン確認
- [ ] LOD要件の合意書作成
- [ ] 共通データ環境（CDE）へのアクセス権設定
- [ ] クラッシュ検出の定期スケジュール設定
- [ ] 図面とBIMモデルの整合性確認

---

## 9. まとめ / Summary

本章では第04章の主要概念を体系的に学習した。
BIM実務において本章の知識を適切に運用するためには、
理論的理解と実務経験の組み合わせが不可欠である。

次章では本章の知識をさらに発展させた応用概念を学ぶ。

---

### 確認問題（多肢選択式）

以下の各問に対し、最も適切な選択肢を1つ選べ。

**問1.** 本章の主要概念を最も正確に説明しているのはどれか。
- A. 選択肢A（誤）
- B. 選択肢B（正）
- C. 選択肢C（誤）
- D. 選択肢D（誤）

**問2.** 関連する国際標準として正しいものはどれか。
- A. ISO 9001
- B. ISO 16739（IFC）
- C. ISO 14001
- D. ISO 45001

**問3.** LOD 300 が示す詳細度として正しいのはどれか。
- A. 概念設計段階のシンボル的形状
- B. 実施設計段階の正確な形状・寸法・位置
- C. 施工詳細設計段階の製作情報
- D. 維持管理段階の現況一致情報

**問4.** BEP（BIM実行計画書）に必ず含まれる項目として適切でないのはどれか。
- A. 使用BIMソフトウェアとバージョン
- B. 担当者の個人的な趣味・嗜好
- C. ファイル命名規則
- D. LOD要件

**問5.** CDE（共通データ環境）の情報状態の正しい遷移順序はどれか。
- A. Shared → Work In Progress → Published → Archived
- B. Work In Progress → Shared → Published → Archived
- C. Published → Shared → Work In Progress → Archived
- D. Archived → Published → Shared → Work In Progress

**問6.** IFCの主な目的として最も適切なのはどれか。
- A. 特定ベンダーのBIMソフトウェアを標準化する
- B. 異なるBIMソフトウェア間のデータ交換を可能にする
- C. BIMの使用を特定の国に制限する
- D. 2D図面の電子化を促進する

**問7.** クラッシュ検出において「ハードクラッシュ」とは何か。
- A. 2つの部材が同じ空間を占有している物理的干渉
- B. 部材間の距離が基準値以下の近接状態
- C. モデルのファイル破損によるエラー
- D. 工程の遅延による施工クラッシュ

**問8.** 4D BIMにおける「4次元目」として正しいのはどれか。
- A. コスト情報
- B. 時間（工程）情報
- C. 維持管理情報
- D. 環境性能情報

**問9.** 日本における建築確認申請とBIMの関係として現状に即しているのはどれか。
- A. BIMモデルデータで確認申請が完全に代替できる
- B. 確認申請にはBIMモデルの提出が義務付けられている
- C. BIMモデルから出力した2D図面で申請するケースが主流
- D. BIM確認申請は法律で禁止されている

**問10.** デジタルツインの定義として最も適切なのはどれか。
- A. 建物の竣工図書をデジタル化したもの
- B. BIMモデルにリアルタイムのIoTデータを統合した動的建物情報モデル
- C. 建物の3Dレンダリング画像
- D. 建物の2D平面図のデジタル版


---

## 実践演習 / Practical Exercise

**演習課題：**

1. 本章で学習した概念を自身の実務プロジェクトに当てはめ、
   現状の課題と改善案を300字以内で記述せよ。

2. 本章の図表（上記参照）を見て、
   自身のプロジェクトでの応用シーンを具体的に説明せよ。

3. 本章の内容をもとに、チームメンバー向けの
   5分間説明プレゼンテーション資料（スライド5枚）を作成せよ。

---

---

## 🔘 Translate this chapter to English

[English translation placeholder – AI translatable block]

> **Translation Instructions for AI:**
> - Translate all Japanese content above into English.
> - Maintain identical paragraph structure and section headings.
> - Preserve all figure citations with page numbers.
> - Keep all technical terms (BIM, IFC, LOD, etc.) in their standard English form.
> - Maintain だ・である調 → declarative / academic register in English.
> - Do NOT rephrase or summarize — translate in full.

---

