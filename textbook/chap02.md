# 第02章：BIMの技術構造――IFC・LOD・データフォーマット
# Chapter 02: BIM Technical Architecture – IFC, LOD, and Data Formats

> **キーワード / Keywords：** IFC / LOD / オープンBIM / データ互換性 / buildingSMART

---

## 学習目標 / Learning Objectives

本章を修了すると、受講者は以下を達成できる：

1. IFC（Industry Foundation Classes）の目的と構造を説明できる
2. LOD（Level of Development）の各段階（100〜500）の違いを理解できる
3. オープンBIMとクローズドBIMの差異を説明できる
4. BIMデータフォーマット（.rvt / .ifc / .nwd等）の用途を区別できる
5. buildingSMARTの役割と国際標準化活動を概説できる


## この章で理解すべきこと / Key Concepts to Master

本章を学習する前に、以下の問いを念頭に置くこと：

**1.** IFC（Industry Foundation Classes）はbuildingSMARTが策定したBIMデータの国際標準フォーマット（ISO 16739）であり、ソフトウェアに依存しない中立的なデータ交換形式である。

**2.** LOD（Level of Development）はBIMモデルの情報詳細度を100（概念設計）から500（竣工・現況）まで5段階で定義した指標である。

**3.** オープンBIM（IFC利用）とクローズドBIM（ベンダー独自形式）の差異と、プロジェクト選択基準。

**4.** .rvt（Revit固有）・.ifc（オープン交換）・.nwd（干渉チェック）・.bcf（問題共有）の用途の違い。

**5.** buildingSMARTの役割：IFC・BCF・IDM・MVDなどBIM標準化活動の国際推進機関。


---

## 1. 問題の背景 / Problem Background

BIMソフトウェアは複数のベンダーが提供しており、Autodesk Revit、ARCHICAD、Vectorworks等それぞれ独自のファイル形式を持つ。設計・施工・設備・構造の各専門会社が異なるソフトを使用する場合、データ交換ができなければBIM連携の効果は失われる。

---

## 2. 解説 / Explanation

IFC（Industry Foundation Classes）は、buildingSMARTが策定したBIMデータの国際標準フォーマットである（ISO 16739）。IFCはソフトウェアに依存しない中立的なデータ形式であり、異なるBIMツール間でのデータ交換を可能にする。

LOD（Level of Development）は、BIMモデルの情報詳細度を段階的に定義した指標である。
- LOD 100：概念設計段階（形状はシンボル的）
- LOD 200：基本設計段階（おおよその形状・寸法）
- LOD 300：実施設計段階（正確な形状・寸法・位置）
- LOD 400：施工詳細設計段階（製作・施工情報含む）
- LOD 500：竣工・維持管理段階（現況と完全一致）

データフォーマットは目的に応じて使い分ける。.rvtはRevit固有形式、.ifcはオープン交換形式、.nwdはNavisworksによる干渉チェック用形式、.bcfは問題点共有用の軽量フォーマットである。

---

## 3. 図表 / Figures

【図表：IFCデータ構造の階層図】
（出典：PDF p.16）

![IFCデータ構造の階層図](assets/pages/p016.png)

① 図の説明：IFCのオブジェクト階層（プロジェクト→サイト→建物→フロア→スペース→要素）を示す図。

② 読み取り方：ツリー構造の上位から下位へ、IFCエンティティの包含関係を読む。

③ 教育上の狙い：IFCが単なるファイル形式ではなくデータモデルであることを理解させる。

④ 実務活用シーン：IFCエクスポート設定の確認・トラブルシューティングに使用する。


【図表：LOD（情報詳細度）の段階別モデル比較図】
（出典：PDF p.17）

![LOD（情報詳細度）の段階別モデル比較図](assets/pages/p017.png)

① 図の説明：LOD 100から500まで、同一部材がどのように表現されるかを示す段階別比較図。

② 読み取り方：左から右に詳細度が増すにつれてモデルの形状と属性が豊富になることを確認する。

③ 教育上の狙い：プロジェクトフェーズに応じた適切なLOD設定の判断力を養う。

④ 実務活用シーン：BEP（BIM実行計画書）のLOD設定表作成時の参照基準。


---

## 4. アナロジー（類比）/ Analogy

IFCはBIM世界における「USB規格」である。USBがメーカーを問わず機器を接続できるように、IFCはソフトウェアを問わずBIMデータを交換可能にする。LODは建物モデルの「解像度設定」であり、設計フェーズが進むにつれて解像度を段階的に上げていくイメージである。

---

## 5. 実際の失敗事例 / Real Failure Case

【実際の失敗事例】大型商業施設の設計において、意匠設計事務所がRevit、設備設計会社がDIALuxを使用していた。IFC書き出し設定が不適切だったため、照明器具の位置情報が失われ、設備干渉チェックが無効化された。IFCのバージョン統一とエクスポート設定のガイドライン策定が事後対策として実施された。

---

## 6. 日本の建設文化的背景 / Japanese Construction Culture Notes

日本では「オープンBIM」よりも同一ベンダーソフトウェアによる「クローズドBIM」が採用されるケースが依然として多い。これは元請けゼネコンがソフトウェアを指定し、下請けに統一させる商慣行による。国土交通省のガイドラインは段階的なIFC活用を促進している。

---

## 7. 外国籍技術者へのノート / Notes for Foreign Engineers

外国籍技術者へのノート：日本国内のBIM標準はJIS A 2053として整備されており、LODの定義はAIA（米国建築家協会）基準と若干異なる部分がある。プロジェクト開始前にLODの合意書（BIM実行計画書：BEP）を締結することが重要である。

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

本章では第02章の主要概念を体系的に学習した。
BIM実務において本章の知識を適切に運用するためには、
理論的理解と実務経験の組み合わせが不可欠である。

次章では本章の知識をさらに発展させた応用概念を学ぶ。


---

## 要点まとめ / Key Takeaways

**1.** IFCはBIM世界の「USB規格」であり、ソフトウェアの違いを超えてデータ交換を可能にするオープン標準である（ISO 16739）。

**2.** LODはBIMモデルの「解像度設定」であり、LOD 100（概念）からLOD 500（維持管理）まで段階的に情報詳細度を上げる。

**3.** オープンBIMはIFCを通じた相互運用性を確保し、特定ベンダーへの依存を排除する設計思想である。

**4.** BCFは問題点・コメントを軽量形式で共有するBIMコラボレーションフォーマットである。

**5.** エクスポート設定・バージョン統一・MVD（モデルビュー定義）の確認がIFC連携成功の鍵である。


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
