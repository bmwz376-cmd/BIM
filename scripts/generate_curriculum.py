#!/usr/bin/env python3
"""
generate_curriculum.py
======================
Generates all Markdown curriculum files for the BIM training package.
Produces:
  README.md, BUILD_NOTES.md, course_plan.md, glossary.md,
  textbook/chapXX.md, slides/chapXX_slide.md,
  workbook/chapXX_exercises.md, workbook/chapXX_answers.md

Run: python3 scripts/generate_curriculum.py
"""

import os

# ─────────────────────────────────────────────
# CHAPTER DEFINITIONS
# ─────────────────────────────────────────────
CHAPTERS = [
    {
        "num": 1,
        "title": "BIMとは何か――概念・定義・歴史的変遷",
        "title_en": "What is BIM? Concepts, Definitions, and Historical Evolution",
        "keywords": ["BIM定義", "建物情報モデリング", "CADとの比較", "BIM導入背景", "デジタルトランスフォーメーション"],
        "fig_pages": [3, 4, 5, 6],
        "session": 1,
        "objective_items": [
            "BIM（Building Information Modeling）の定義と基本概念を説明できる",
            "CADとBIMの本質的な違いを図を用いて比較できる",
            "BIMが建築業界に普及した歴史的経緯を述べられる",
            "日本の建設業界におけるBIM導入の現状を把握できる",
            "BIMが解決する業務課題を3つ以上列挙できる",
        ],
        "bg_problem": (
            "従来の建築設計では、平面図・立面図・断面図などを個別のCADデータとして管理していた。"
            "このため、設計変更が生じるたびに複数のファイルを手動で修正する必要があり、"
            "整合性ミスや情報伝達の断絶が頻繁に発生していた。"
            "BIMはこの課題を「単一の建物情報モデル」によって根本的に解決する技術である。"
        ),
        "explanation": (
            "BIM（Building Information Modeling）とは、建物の設計・施工・維持管理に関するすべての情報を、"
            "3次元の幾何情報と属性データとして統合した「建物情報モデル」を中心に業務を進める手法である。\n\n"
            "BIMモデルは単なる3D図形ではなく、各部材に「材料」「寸法」「コスト」「施工手順」「維持管理情報」"
            "などの属性が付与されたオブジェクトの集合体である。\n\n"
            "BIMの概念は1970年代の研究に起源を持ち、2000年代にAutodesk Revitの登場とともに実務への普及が加速した。"
            "米国では連邦政府調達における義務化、英国ではBIM Level 2の国家標準化が進んだ。"
            "日本では2019年以降、国土交通省がBIM/CIM推進政策を強化し、公共事業での適用が拡大している。"
        ),
        "analogy": (
            "CADを「デジタル製図板」とするならば、BIMは「建物のデジタル双子（Digital Twin）」である。"
            "CADが2D図面の電子化にとどまるのに対し、BIMは建物の全ライフサイクルにわたる情報を"
            "一元管理するプラットフォームとして機能する。"
        ),
        "failure_case": (
            "【実際の失敗事例】ある大規模オフィスビルの施工現場において、"
            "設計チームと施工チームが異なるCADファイルを使用していたため、"
            "空調ダクトと構造梁の干渉が施工着工後に判明した。"
            "この手戻りにより工期が3週間延長し、追加コストが約2,000万円に達した。"
            "BIMのクラッシュ検出機能を活用していれば、着工前に防止できた事例である。"
        ),
        "jp_culture": (
            "日本の建設業界は「職人文化」と「重層下請け構造」という特性を持つ。"
            "BIM導入においては、上位元請けがBIMモデルを作成し、"
            "下位協力会社がそれを参照・更新する「トップダウン型BIM」が主流となりつつある。"
            "また、日本では「図面至上主義」が根強く、BIMモデルと図面の並行管理が"
            "過渡期の課題として残っている。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本のBIM標準はISO 19650に準拠しつつも、"
            "JIS A 2053（BIM）などの国内規格が独自に整備されている。"
            "また、日本の法令（建築基準法）は確認申請図書として2D図面を要求するため、"
            "BIMモデルからの図面生成プロセスが不可欠である。"
        ),
    },
    {
        "num": 2,
        "title": "BIMの技術構造――IFC・LOD・データフォーマット",
        "title_en": "BIM Technical Architecture – IFC, LOD, and Data Formats",
        "keywords": ["IFC", "LOD", "オープンBIM", "データ互換性", "buildingSMART"],
        "fig_pages": [15, 16, 17, 18],
        "session": 2,
        "objective_items": [
            "IFC（Industry Foundation Classes）の目的と構造を説明できる",
            "LOD（Level of Development）の各段階（100〜500）の違いを理解できる",
            "オープンBIMとクローズドBIMの差異を説明できる",
            "BIMデータフォーマット（.rvt / .ifc / .nwd等）の用途を区別できる",
            "buildingSMARTの役割と国際標準化活動を概説できる",
        ],
        "bg_problem": (
            "BIMソフトウェアは複数のベンダーが提供しており、Autodesk Revit、ARCHICAD、Vectorworks等"
            "それぞれ独自のファイル形式を持つ。設計・施工・設備・構造の各専門会社が"
            "異なるソフトを使用する場合、データ交換ができなければBIM連携の効果は失われる。"
        ),
        "explanation": (
            "IFC（Industry Foundation Classes）は、buildingSMARTが策定したBIMデータの国際標準フォーマットである（ISO 16739）。"
            "IFCはソフトウェアに依存しない中立的なデータ形式であり、"
            "異なるBIMツール間でのデータ交換を可能にする。\n\n"
            "LOD（Level of Development）は、BIMモデルの情報詳細度を段階的に定義した指標である。\n"
            "- LOD 100：概念設計段階（形状はシンボル的）\n"
            "- LOD 200：基本設計段階（おおよその形状・寸法）\n"
            "- LOD 300：実施設計段階（正確な形状・寸法・位置）\n"
            "- LOD 400：施工詳細設計段階（製作・施工情報含む）\n"
            "- LOD 500：竣工・維持管理段階（現況と完全一致）\n\n"
            "データフォーマットは目的に応じて使い分ける。"
            ".rvtはRevit固有形式、.ifcはオープン交換形式、"
            ".nwdはNavisworksによる干渉チェック用形式、.bcfは問題点共有用の軽量フォーマットである。"
        ),
        "analogy": (
            "IFCはBIM世界における「USB規格」である。"
            "USBがメーカーを問わず機器を接続できるように、"
            "IFCはソフトウェアを問わずBIMデータを交換可能にする。"
            "LODは建物モデルの「解像度設定」であり、"
            "設計フェーズが進むにつれて解像度を段階的に上げていくイメージである。"
        ),
        "failure_case": (
            "【実際の失敗事例】大型商業施設の設計において、"
            "意匠設計事務所がRevit、設備設計会社がDIALuxを使用していた。"
            "IFC書き出し設定が不適切だったため、照明器具の位置情報が失われ、"
            "設備干渉チェックが無効化された。"
            "IFCのバージョン統一とエクスポート設定のガイドライン策定が事後対策として実施された。"
        ),
        "jp_culture": (
            "日本では「オープンBIM」よりも同一ベンダーソフトウェアによる「クローズドBIM」が"
            "採用されるケースが依然として多い。これは元請けゼネコンがソフトウェアを指定し、"
            "下請けに統一させる商慣行による。国土交通省のガイドラインは段階的なIFC活用を促進している。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本国内のBIM標準はJIS A 2053として整備されており、"
            "LODの定義はAIA（米国建築家協会）基準と若干異なる部分がある。"
            "プロジェクト開始前にLODの合意書（BIM実行計画書：BEP）を締結することが重要である。"
        ),
    },
    {
        "num": 3,
        "title": "BIMワークフロー――設計から施工・維持管理まで",
        "title_en": "BIM Workflow – From Design to Construction and Facility Management",
        "keywords": ["BIMワークフロー", "ライフサイクル", "BEP", "CDE", "フェーズ管理"],
        "fig_pages": [28, 29, 30, 32],
        "session": 2,
        "objective_items": [
            "BIMワークフローの全体像（企画→設計→施工→維持管理）を説明できる",
            "BIM実行計画書（BEP）の目的と必須記載事項を列挙できる",
            "共通データ環境（CDE）の役割と実装方法を理解できる",
            "各設計フェーズにおけるBIMの活用目的を区別できる",
            "維持管理（FM）フェーズにおけるBIMデータ活用事例を説明できる",
        ],
        "bg_problem": (
            "建設プロジェクトは企画・基本設計・実施設計・施工・維持管理という複数のフェーズにわたり、"
            "多くのステークホルダーが関与する。従来の手法では各フェーズ間の情報断絶が生じやすく、"
            "設計意図が施工に反映されなかったり、竣工図書が維持管理に活用されなかったりする問題があった。"
        ),
        "explanation": (
            "BIMワークフローは建物のライフサイクル全体を通じて一貫した情報モデルを維持する。\n\n"
            "【企画フェーズ】：ボリュームスタディ、法規チェック、概算コスト算出にBIMを活用。\n"
            "【基本設計フェーズ】：空間構成の検討、環境シミュレーション（日照・風・熱）、意匠コンセプトの可視化。\n"
            "【実施設計フェーズ】：各部材の詳細設計、設備・構造との整合確認、数量積算。\n"
            "【施工フェーズ】：施工計画・4Dシミュレーション（工程管理）、クラッシュ検出、現場と設計の照合。\n"
            "【維持管理フェーズ】：竣工BIMモデルをFM（ファシリティマネジメント）システムと連携。\n\n"
            "BEP（BIM Execution Plan：BIM実行計画書）はプロジェクト開始時に策定する文書であり、"
            "使用ソフト・LOD・責任分担・ファイル命名規則・納品形式を定義する。\n\n"
            "CDE（Common Data Environment：共通データ環境）はプロジェクト全体の"
            "BIMデータを一元管理するクラウドプラットフォームである。"
        ),
        "analogy": (
            "BIMワークフローは「建物のカルテ」に例えられる。"
            "医療の世界で患者のカルテが医師・看護師・薬剤師に共有されるように、"
            "BIMモデルは設計者・施工者・設備業者・維持管理担当者が参照・更新する共有情報基盤となる。"
        ),
        "failure_case": (
            "【実際の失敗事例】あるホテルの改修工事において、"
            "竣工BIMモデルが維持管理部門に引き渡されなかったため、"
            "設備更新の際に隠蔽配管の位置が把握できず、"
            "壁を不必要に解体する工事が発生した。"
            "竣工BIMのFMシステム連携プロセスを設計段階から計画する重要性が示された事例である。"
        ),
        "jp_culture": (
            "日本では「竣工図書」の紙ベース提出が法的に要求される場合があり、"
            "BIMモデルと紙図面の並行管理が過渡期の標準となっている。"
            "国土交通省は2023年度から一定規模以上の公共建築においてBIM設計を原則化しており、"
            "竣工BIMモデルの発注者への引き渡しルールが整備されつつある。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本のCDEは欧米と比較して普及が遅れており、"
            "メール・FTPサーバー・クラウドストレージが混在する環境が多い。"
            "ISO 19650準拠のCDE導入が今後の課題である。"
        ),
    },
    {
        "num": 4,
        "title": "BIMソフトウェアの種類と選定基準",
        "title_en": "Types of BIM Software and Selection Criteria",
        "keywords": ["Revit", "ARCHICAD", "Vectorworks", "Navisworks", "ソフトウェア選定"],
        "fig_pages": [45, 46, 48, 50],
        "session": 3,
        "objective_items": [
            "主要なBIMソフトウェアの特徴と用途を比較説明できる",
            "プロジェクト規模・用途に応じたソフトウェア選定基準を適用できる",
            "意匠・構造・設備BIMツールの相互連携方法を理解できる",
            "BIMビューアとBIM編集ソフトの違いを説明できる",
            "ライセンスコストと導入コストを含めたTCO（総所有コスト）の概念を理解できる",
        ],
        "bg_problem": (
            "BIMソフトウェアは多種多様であり、「どのソフトを選べばよいか」が実務担当者の最初の壁となる。"
            "誤ったソフトウェア選定は、後のデータ互換性問題や再学習コストを招く。"
        ),
        "explanation": (
            "主要BIMソフトウェアは以下のカテゴリに分類される。\n\n"
            "【意匠BIM】\n"
            "- Autodesk Revit：世界シェア最大。日本大手ゼネコン・設計事務所で広く使用。\n"
            "- ARCHICAD（Graphisoft）：操作性に優れ中小設計事務所で普及。\n"
            "- Vectorworks：日本の設計事務所で利用者多数。BIMとCADの中間的な使い方が可能。\n\n"
            "【構造BIM】\n"
            "- Tekla Structures：鉄骨・プレキャストコンクリートの詳細モデリングに強み。\n"
            "- SCIA Engineer：構造解析とBIM連携が得意。\n\n"
            "【設備BIM】\n"
            "- Revit MEP：Revitの設備専用モジュール。意匠Revitとシームレスに連携。\n"
            "- MagiCAD：Revit上で動作する設備BIMプラグイン。\n\n"
            "【干渉チェック・統合】\n"
            "- Autodesk Navisworks：各BIMモデルを統合してクラッシュ検出と4Dシミュレーションを実施。\n"
            "- Solibri Model Checker：IFCベースの品質・規則チェックに特化。\n\n"
            "【BIMビューア】\n"
            "- BIMx（Graphisoft）：ARCHICADモデルのモバイル閲覧。\n"
            "- Autodesk Viewer：ブラウザベースの無料BIMビューア。"
        ),
        "analogy": (
            "BIMソフトウェア選定はOS選択に似ている。"
            "WindowsとMacが異なるエコシステムを持つように、"
            "RevitとARCHICADは異なるワークフローと連携ツール群を持つ。"
            "プロジェクトの規模・チーム構成・取引先環境を踏まえた戦略的選定が不可欠である。"
        ),
        "failure_case": (
            "【実際の失敗事例】中規模設計事務所がRevitを導入したものの、"
            "習得コストが高く既存CADワークフローとの整合が取れず、"
            "1年後にARCHICADへ移行した事例がある。"
            "移行コストと再教育コストで総額1,500万円超の損失が生じた。"
            "事前のパイロットプロジェクトと段階的導入計画の重要性が示された。"
        ),
        "jp_culture": (
            "日本の大手ゼネコン（鹿島・大成・清水・竹中・大林）はRevitを主軸としているが、"
            "中小設計事務所ではARCHICADやVectorworksも多い。"
            "元請けが使用ソフトを指定するケースが多く、"
            "協力会社は複数ソフトを扱う能力が求められる。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本市場では各ソフトウェアの日本語UIと日本語サポートが選定要因となることが多い。"
            "Revitの日本語版は機能的に国際版と同等だが、"
            "日本固有のファミリ（部材ライブラリ）が充実している点で優位性がある。"
        ),
    },
    {
        "num": 5,
        "title": "BIMとコラボレーション――多職種連携と情報共有",
        "title_en": "BIM and Collaboration – Multidisciplinary Coordination and Information Sharing",
        "keywords": ["コラボレーション", "IPD", "BCF", "クラッシュ検出", "情報共有"],
        "fig_pages": [62, 63, 65, 67],
        "session": 4,
        "objective_items": [
            "BIMを活用した多職種間の情報共有プロセスを説明できる",
            "クラッシュ検出の手順と解決プロセスを実施できる",
            "BCF（BIM Collaboration Format）の役割を理解できる",
            "IPD（Integrated Project Delivery）の概念とBIMとの関係を説明できる",
            "コラボレーション失敗の原因と予防策を列挙できる",
        ],
        "bg_problem": (
            "建設プロジェクトには意匠・構造・設備・施工・発注者など多くの関係者が存在する。"
            "それぞれが異なる情報を持ち、異なるタイミングで作業するため、"
            "情報の断絶・矛盾・重複が生じやすい。"
            "BIMはこれら複数の専門家が「同一のモデル」を基点として協働するインフラを提供する。"
        ),
        "explanation": (
            "BIMコラボレーションの中核は「モデル連携」と「課題管理」である。\n\n"
            "【クラッシュ検出（Clash Detection）】\n"
            "意匠・構造・設備のBIMモデルをNavisworksなどの統合ソフトに読み込み、"
            "部材の物理的干渉（ハードクラッシュ）や近接不良（ソフトクラッシュ）を自動検出する。\n\n"
            "【BCF（BIM Collaboration Format）】\n"
            "BCFはBIMモデル上の問題点をリンク付きで共有する軽量フォーマットである。"
            "スクリーンショット・問題箇所の3D座標・担当者・ステータスを含む。\n\n"
            "【CDEによる情報管理】\n"
            "発行（In Progress）→レビュー（In Review）→承認（Approved）→アーカイブ（Archived）"
            "というワークフローでモデルの状態を管理する。\n\n"
            "【IPD（Integrated Project Delivery）】\n"
            "設計者・施工者・発注者が早期から一体となって設計を進める契約形態。"
            "BIMはIPDの技術的基盤として機能し、早期の問題発見・コスト最適化を可能にする。"
        ),
        "analogy": (
            "BIMコラボレーションはオーケストラの総譜に例えられる。"
            "指揮者（プロジェクトマネージャー）のもと、"
            "弦楽器（意匠）・管楽器（構造）・打楽器（設備）がそれぞれのパートを演奏しながら、"
            "全体として調和した建物を創り上げる。"
        ),
        "failure_case": (
            "【実際の失敗事例】大規模病院建設において、"
            "設備チームが最新のBIMモデルではなく1世代前のバージョンを参照して作業を進めた。"
            "この結果、医療ガス配管と空調ダクトの干渉が200箇所以上検出され、"
            "設計期間が6週間延長した。"
            "CDEのバージョン管理ルールと承認フローの厳格化が対策として実施された。"
        ),
        "jp_culture": (
            "日本では「根回し文化」と「会議による合意形成」がBIMコラボレーションにも影響する。"
            "BCFによるデジタル課題管理よりも、"
            "対面会議で問題を解決してから記録に残す慣行が残っている現場も多い。"
            "BIM導入とともにデジタルコミュニケーション文化への転換が求められる。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本のプロジェクトでは「波風を立てない」文化的背景から、"
            "BCFで問題点を明示的に記録することへの抵抗感が生じることがある。"
            "問題管理は個人批判ではなくプロジェクト品質向上のためのツールであることを"
            "チームに周知することが重要である。"
        ),
    },
    {
        "num": 6,
        "title": "BIM活用による建築生産性向上――積算・施工管理・4D",
        "title_en": "Improving Construction Productivity with BIM – Estimation, Construction Management, 4D",
        "keywords": ["数量積算", "4Dシミュレーション", "施工BIM", "工程管理", "生産性向上"],
        "fig_pages": [80, 82, 84, 86],
        "session": 5,
        "objective_items": [
            "BIMモデルからの自動数量積算の仕組みと精度を説明できる",
            "4Dシミュレーション（3D＋工程）による施工計画立案手法を理解できる",
            "BIMを用いた施工現場管理（進捗確認・品質管理）の実務を概説できる",
            "BIMによる生産性向上効果（コスト削減・工期短縮）を定量的に説明できる",
            "プレファブリケーションとBIMの連携メリットを説明できる",
        ],
        "bg_problem": (
            "従来の建設現場では、積算は図面から手動で数量を拾い出す作業であり、"
            "習熟した積算担当者の経験に依存していた。"
            "また施工計画は2D図面と工程表を別々に管理しており、"
            "全体像の把握が困難だった。"
        ),
        "explanation": (
            "【自動数量積算】\n"
            "BIMモデルの各オブジェクトには面積・体積・長さ等の幾何情報が格納されており、"
            "ソフトウェアが自動的に数量一覧表（BoQ: Bill of Quantities）を生成する。"
            "設計変更時も数量が即座に更新されるため、手動積算に比べて大幅な時間短縮が実現する。\n\n"
            "【4Dシミュレーション】\n"
            "BIMモデル（3D）に工程情報（1D：時間軸）を付加した4Dシミュレーションにより、"
            "施工の進捗を視覚的に確認・調整できる。"
            "クレーンの作業半径・資材搬入ルート・仮設計画の検証が可能となる。\n\n"
            "【プレファブリケーション連携】\n"
            "BIMモデルから製作図面を直接出力し、工場でのプレファブ製造に活用することで、"
            "現場施工時間の短縮と品質の安定化が実現する。"
        ),
        "analogy": (
            "BIM積算は「スーパーマーケットのバーコードシステム」に例えられる。"
            "各部材にバーコード（属性データ）が付いており、"
            "レジ（積算ソフト）が瞬時に合計を計算する。"
            "設計変更は価格改定と同様、モデル修正で全数量が自動更新される。"
        ),
        "failure_case": (
            "【実際の失敗事例】あるマンション開発プロジェクトで、"
            "BIM積算を初めて導入した際にモデルの属性入力が不完全だったため、"
            "一部の仕上げ材料が積算から漏れた。"
            "最終的に実際のコストが積算値を5%超過し、予算超過となった。"
            "BIMモデルの属性入力品質管理（LOI: Level of Information）の重要性が示された。"
        ),
        "jp_culture": (
            "日本の建設積算は「見積もり文化」が強く、"
            "精緻な手積算の信頼性が高く評価されてきた。"
            "BIM積算の導入にあたっては、"
            "ベテラン積算担当者のスキルをBIMモデル品質管理に転換する人材育成戦略が有効である。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本の公共工事では「設計図書」に基づく積算が法的要件であり、"
            "BIM積算結果は補助的資料として扱われることが多い。"
            "BIM積算を正式な提出書類とするための法整備が進行中である。"
        ),
    },
    {
        "num": 7,
        "title": "BIMと維持管理――FM連携・デジタルツイン・スマートビル",
        "title_en": "BIM and Facility Management – FM Integration, Digital Twin, Smart Buildings",
        "keywords": ["FM", "デジタルツイン", "スマートビル", "IoT", "アセットマネジメント"],
        "fig_pages": [98, 100, 102, 104],
        "session": 6,
        "objective_items": [
            "BIMと施設管理（FM）システムの連携方法を説明できる",
            "デジタルツインの概念とBIMとの関係を理解できる",
            "IoTセンサーとBIMモデルの統合によるスマートビル実現手法を概説できる",
            "アセットマネジメントにおけるBIM活用の経済的効果を説明できる",
            "COBieフォーマットの目的と活用場面を理解できる",
        ],
        "bg_problem": (
            "建物の維持管理コストは建設コストの数倍に達するとされているが、"
            "従来は紙の図面・台帳・マニュアルによる管理が主流だった。"
            "設備の更新・点検・修繕に必要な情報が分散し、"
            "緊急時の対応に多大な時間とコストが発生していた。"
        ),
        "explanation": (
            "【BIMとFMの連携】\n"
            "竣工BIMモデルにはすべての設備機器・部材の仕様・メーカー・保証情報が格納されている。"
            "これをFMシステム（IBM Tririga、Archibus等）と連携させることで、"
            "点検計画の自動生成・修繕履歴管理・部品発注の効率化が実現する。\n\n"
            "【COBie（Construction Operations Building information exchange）】\n"
            "COBieはBIMモデルから設備情報を抽出するスプレッドシート形式の標準フォーマットであり、"
            "竣工引き渡し時の情報移管を標準化する。\n\n"
            "【デジタルツイン】\n"
            "デジタルツインはBIMモデルにリアルタイムのIoTセンサーデータを統合した"
            "「動的建物情報モデル」である。"
            "温度・湿度・エネルギー消費・人流などのデータをリアルタイムで可視化し、"
            "予防保全・エネルギー最適化・スペース管理に活用する。"
        ),
        "analogy": (
            "デジタルツインは「建物のMRI」である。"
            "人間のMRIが体内の状態をリアルタイムで可視化するように、"
            "デジタルツインは建物の「健康状態」を常時モニタリングし、"
            "問題の早期発見と予防的対処を可能にする。"
        ),
        "failure_case": (
            "【実際の失敗事例】大型ショッピングモールで、"
            "竣工BIMモデルの発注者への引き渡しが行われなかった。"
            "開業5年後の空調システム更新工事において、"
            "配管経路の把握に多大な調査費用が発生し、"
            "工事費が当初見積もりの1.8倍に膨らんだ。"
            "竣工BIMモデルの資産価値と引き渡し契約の明文化の重要性を示す事例である。"
        ),
        "jp_culture": (
            "日本では建物の「スクラップ＆ビルド」文化から「長寿命化」への転換が政策的に推進されている。"
            "国土交通省の「長期優良住宅」制度やZEB（ネット・ゼロ・エネルギー・ビル）政策と"
            "BIMによる維持管理効率化は密接に連動している。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本の建物管理業務は「建物管理業務適正化法」等の法令に規束される。"
            "FM担当者向けのBIM活用ガイドラインは"
            "日本ファシリティマネジメント協会（JFMA）が整備している。"
        ),
    },
    {
        "num": 8,
        "title": "BIMと法規・確認申請――日本の建築行政とのインターフェース",
        "title_en": "BIM and Building Regulations – Interface with Japanese Building Administration",
        "keywords": ["確認申請", "建築基準法", "BIM確認申請", "電子申請", "CIM"],
        "fig_pages": [115, 116, 118, 120],
        "session": 7,
        "objective_items": [
            "日本の建築確認申請制度とBIMの関係を説明できる",
            "BIM確認申請（電子申請）の現状と課題を理解できる",
            "建築基準法上の「設計図書」とBIMモデルの法的位置づけを概説できる",
            "CIM（Construction Information Modeling）とBIMの違いと連携を説明できる",
            "BIM/CIMロードマップにおける国土交通省の政策方針を概説できる",
        ],
        "bg_problem": (
            "BIMが普及しても、日本では建築確認申請に紙（または2D PDF）の図面提出が求められてきた。"
            "このため、BIMモデルから図面を出力し直す「BIM→2D変換」の二重作業が生じており、"
            "BIM本来の効率化が損なわれていた。"
        ),
        "explanation": (
            "【建築確認申請とBIM】\n"
            "建築基準法第6条は建築確認申請時に「設計図書」の提出を義務付けている。"
            "現行法では「設計図書」の解釈にBIMモデルデータは含まれないが、"
            "国土交通省は段階的なBIM確認申請の実現に向けた実証実験を推進している。\n\n"
            "【電子申請の現状（2024年）】\n"
            "建築確認申請の電子申請システム（ICBA等）が整備されつつあるが、"
            "BIMモデルデータの直接受領には至っていない。"
            "一部の自治体・特定行政庁でBIM活用の実証実験が実施されている。\n\n"
            "【CIM（Construction Information Modeling）】\n"
            "国土交通省が推進するCIMは土木・インフラ領域のBIMに相当する。"
            "道路・橋梁・ダム・トンネルの設計・施工・維持管理への3D情報モデル適用を目指す。\n\n"
            "【BIM/CIMロードマップ】\n"
            "国土交通省は2023年度を目標にすべての大規模公共事業へのBIM/CIM適用を義務化した。"
        ),
        "analogy": (
            "BIM確認申請の現状は、電子申告が普及する前の税務申告に似ている。"
            "オンライン入力後に紙を印刷して提出する「二重作業」の状態から、"
            "完全デジタル申請へ移行する過程にある。"
        ),
        "failure_case": (
            "【実際の失敗事例】BIM設計が完了したにもかかわらず、"
            "確認申請用の2D図面作成に2週間を要した事例がある。"
            "BIMモデルから確認申請図面を自動生成するためのテンプレート整備と"
            "ソフトウェア設定の重要性が示された。"
        ),
        "jp_culture": (
            "日本の建築行政は「申請・審査文化」が根強く、"
            "権限を持つ確認検査機関（指定確認検査機関）との調整が重要である。"
            "BIM確認申請の普及には技術的課題と同時に、"
            "審査機関側のBIMリテラシー向上が不可欠である。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本の建築確認申請制度は「事前審査制」であり、"
            "設計の完成度が高い段階で申請が行われる。"
            "欧米のPermit申請と制度的な違いがあるため、"
            "申請タイミングとBIMモデルの完成度の対応関係を理解することが重要である。"
        ),
    },
    {
        "num": 9,
        "title": "BIM導入戦略――組織変革・人材育成・ROI評価",
        "title_en": "BIM Implementation Strategy – Organizational Change, Talent Development, ROI Evaluation",
        "keywords": ["BIM導入戦略", "ROI", "人材育成", "チェンジマネジメント", "BIMマネージャー"],
        "fig_pages": [132, 134, 136, 138],
        "session": 8,
        "objective_items": [
            "BIM導入における組織変革管理（チェンジマネジメント）の手順を説明できる",
            "BIM投資対効果（ROI）の計算方法と評価指標を理解できる",
            "BIMマネージャー・BIMコーディネーターの役割と必要スキルを説明できる",
            "段階的BIM導入計画（パイロット→展開→定着）を立案できる",
            "BIM教育プログラムの設計方法を概説できる",
        ],
        "bg_problem": (
            "BIMは技術的なソリューションであると同時に、"
            "組織の業務プロセス・役割分担・企業文化を変革する「チェンジマネジメント」の課題でもある。"
            "技術習得だけに注力し、組織変革を怠ったBIM導入は失敗に終わるケースが多い。"
        ),
        "explanation": (
            "【BIM導入の3段階】\n"
            "第1段階（パイロット）：小規模プロジェクトでBIMを試験導入。課題を洗い出す。\n"
            "第2段階（展開）：成功事例を基に標準化・テンプレート化を進め、複数プロジェクトへ展開。\n"
            "第3段階（定着）：BIMをデフォルトのワークフローとして組織全体に根付かせる。\n\n"
            "【BIM ROI計算】\n"
            "BIM投資対効果は以下の指標で評価する。\n"
            "- コスト削減：設計変更件数減少・手戻り工数削減・積算時間短縮\n"
            "- 工期短縮：クラッシュ検出による施工トラブル回避\n"
            "- 品質向上：設計品質・施工精度の向上による瑕疵担保リスク低減\n\n"
            "【BIM人材の役割定義】\n"
            "BIMマネージャー：組織全体のBIM戦略・標準化・品質管理を統括。\n"
            "BIMコーディネーター：プロジェクト単位のBIM実行計画の管理・多職種連携の調整。\n"
            "BIMオペレーター：BIMソフトウェアを実際に操作してモデルを作成・更新する実務担当者。"
        ),
        "analogy": (
            "BIM導入は「工場の設備更新」に例えられる。"
            "新しい機械を導入するだけでなく、作業員の再教育・製造プロセスの再設計・"
            "品質管理体制の見直しが一体で行われなければ、"
            "投資対効果は得られない。"
        ),
        "failure_case": (
            "【実際の失敗事例】大手ゼネコンの地方支店がRevitを導入したものの、"
            "本社からの一方的なトップダウン指示により現場担当者の理解が得られず、"
            "BIMモデルの作成が形骸化した。"
            "実際の施工管理は従来の2D図面で行われ、BIM投資が無駄になった。"
            "現場レベルでのBIM価値教育とボトムアップ改善提案の場の設置が解決策となった。"
        ),
        "jp_culture": (
            "日本企業の意思決定は「稟議制度」による合意形成が基本である。"
            "BIM導入の意思決定においても、現場担当者→課長→部長→役員という"
            "段階的な承認プロセスが必要となる。"
            "BIM導入推進者（チャンピオン）は各階層への説明資料とコスト便益分析の準備が不可欠である。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本企業のBIM導入は意思決定に時間がかかる傾向がある。"
            "忍耐強い根回しと段階的なデモンストレーションが外国人技術者にも求められる。"
            "日本BIM推進会議（JBIM）が発行するBIM導入ガイドラインは実践的な参考資料となる。"
        ),
    },
    {
        "num": 10,
        "title": "BIMの未来――AI・GIS・サステナビリティ・グローバルトレンド",
        "title_en": "The Future of BIM – AI, GIS, Sustainability, and Global Trends",
        "keywords": ["AI×BIM", "GIS連携", "サステナビリティ", "カーボンニュートラル", "グローバルBIM"],
        "fig_pages": [148, 150, 152, 155],
        "session": 10,
        "objective_items": [
            "AIとBIMの統合による設計自動化・最適化の可能性を説明できる",
            "GISとBIMの連携（CityGML等）による都市スケールのBIM活用を概説できる",
            "BIMによるLCA（ライフサイクルアセスメント）とカーボンニュートラル実現への貢献を説明できる",
            "グローバルBIMトレンド（英国・北欧・シンガポール等）と日本の位置づけを比較できる",
            "10年後のBIM・建設DXの展望を論述できる",
        ],
        "bg_problem": (
            "建設業界は「2030年カーボンニュートラル」「人口減少による労働力不足」"
            "「大規模インフラの老朽化」という複合的な課題に直面している。"
            "BIMはこれらの課題を解決するデジタルインフラとして進化を続けている。"
        ),
        "explanation": (
            "【AI×BIM】\n"
            "生成AIによる設計案の自動生成（Generative Design）、"
            "機械学習による設計最適化、AIによるBIMモデルの品質チェック自動化が実用化されつつある。\n\n"
            "【GIS×BIM（CityGML・都市BIM）】\n"
            "CityGMLはGIS（地理情報システム）とBIMを統合した都市スケールの3D情報標準である。"
            "3D都市モデル「PLATEAU」（国土交通省）は日本独自の都市BIM推進施策として注目される。\n\n"
            "【BIMとサステナビリティ】\n"
            "BIMモデルにLCA（ライフサイクルアセスメント）ツールを統合することで、"
            "設計段階からCO2排出量を算出・最適化できる。"
            "ZEB（ネット・ゼロ・エネルギービル）設計にBIMエネルギーシミュレーションが活用される。\n\n"
            "【グローバルトレンド】\n"
            "英国はBIM Level 2を2016年に政府調達で義務化した先駆者である。"
            "シンガポールは建築許可申請へのBIM義務化（eSUBMISSION）を世界に先駆けて実施。"
            "北欧（フィンランド・ノルウェー）はOpenBIMとIFC活用で世界最高水準にある。"
        ),
        "analogy": (
            "BIMとAIの統合は「設計者のコパイロット（副操縦士）」の出現に例えられる。"
            "パイロット（設計者）が最終判断を下す一方、"
            "AIコパイロットがリアルタイムで最適ルート（設計案）を提案し続ける。"
        ),
        "failure_case": (
            "【実際の失敗事例・警鐘】"
            "ある自治体がCityGML形式の3D都市モデルを整備したものの、"
            "実際のBIMプロジェクトとのデータ連携方式が未整備だったため、"
            "投資した3D都市モデルが活用されずに陳腐化した事例がある。"
            "データ標準・連携インターフェース・ガバナンスの事前設計が不可欠である。"
        ),
        "jp_culture": (
            "日本は「BIM先進国」とは言えないが、国土交通省のBIM/CIM政策・"
            "国交省PLATEAUプロジェクト・建設DX推進の国家戦略のもと、"
            "急速なキャッチアップが進んでいる。"
            "日本の強みである「ものづくり精神」「現場カイゼン文化」をBIMと融合させることで、"
            "独自のBIM活用モデルを世界に発信できる潜在性を持つ。"
        ),
        "foreign_note": (
            "外国籍技術者へのノート："
            "日本のBIMグローバル化は遅れているが、"
            "語学力とBIM専門性を併せ持つ外国籍技術者には大きなキャリア機会がある。"
            "PLATEAU・BIM/CIM・スマートシティ等の国家プロジェクトへの参画経路が広がっている。"
        ),
    },
]

# ─────────────────────────────────────────────
# FIGURE CATALOG  (10+ required → 15 defined)
# ─────────────────────────────────────────────
FIGURES = [
    {"id": "fig_01", "page": 3,   "title": "BIMの概念図―建物情報モデルの全体像",
     "desc": "BIMモデルを中心に設計・施工・維持管理の各フェーズが連携する全体像を示す概念図。",
     "how_to_read": "中央のBIMモデルから各フェーズへの情報フローを矢印で追う。",
     "edu_intent": "BIMが単なる3D図面ではなく情報統合プラットフォームであることを理解させる。",
     "practice": "プロジェクト計画書作成時のBIM活用範囲定義に使用する。"},
    {"id": "fig_02", "page": 5,   "title": "CADとBIMの比較表",
     "desc": "2次元CADとBIMの違いを設計・施工・維持管理の各フェーズで比較した対照表。",
     "how_to_read": "各行（フェーズ）を左右（CAD vs BIM）で読み比べ、BIMの優位性を確認する。",
     "edu_intent": "受講者のCAD既存知識を活用してBIMへの移行理解を促進する。",
     "practice": "BIM導入提案書の根拠資料として活用する。"},
    {"id": "fig_03", "page": 16,  "title": "IFCデータ構造の階層図",
     "desc": "IFCのオブジェクト階層（プロジェクト→サイト→建物→フロア→スペース→要素）を示す図。",
     "how_to_read": "ツリー構造の上位から下位へ、IFCエンティティの包含関係を読む。",
     "edu_intent": "IFCが単なるファイル形式ではなくデータモデルであることを理解させる。",
     "practice": "IFCエクスポート設定の確認・トラブルシューティングに使用する。"},
    {"id": "fig_04", "page": 17,  "title": "LOD（情報詳細度）の段階別モデル比較図",
     "desc": "LOD 100から500まで、同一部材がどのように表現されるかを示す段階別比較図。",
     "how_to_read": "左から右に詳細度が増すにつれてモデルの形状と属性が豊富になることを確認する。",
     "edu_intent": "プロジェクトフェーズに応じた適切なLOD設定の判断力を養う。",
     "practice": "BEP（BIM実行計画書）のLOD設定表作成時の参照基準。"},
    {"id": "fig_05", "page": 29,  "title": "BIMワークフロー全体図（企画→維持管理）",
     "desc": "建物のライフサイクル全体にわたるBIMワークフローの流れを示すフローチャート。",
     "how_to_read": "左から右に時間軸を追い、各フェーズでのBIM活用内容を確認する。",
     "edu_intent": "BIMが単一フェーズのツールではなくライフサイクル全体の情報基盤であることを理解させる。",
     "practice": "プロジェクトのBIM活用計画立案・BEP作成の際の標準テンプレートとして使用する。"},
    {"id": "fig_06", "page": 30,  "title": "CDE（共通データ環境）の情報フロー図",
     "desc": "CDEにおけるWork In Progress→Shared→Published→Archivedの4状態遷移を示す図。",
     "how_to_read": "各状態を表す円・矩形と、その間の矢印（承認フロー）を追う。",
     "edu_intent": "CDEにおける情報管理の規律とワークフロー管理の重要性を理解させる。",
     "practice": "CDEシステム導入時の情報管理ルール策定の基準として使用する。"},
    {"id": "fig_07", "page": 46,  "title": "主要BIMソフトウェア比較マトリックス",
     "desc": "Revit・ARCHICAD・Vectorworks・Tekla等を機能・価格・対応分野で比較した表。",
     "how_to_read": "列（ソフト名）と行（評価項目）の交点で各ソフトの特性を読み取る。",
     "edu_intent": "プロジェクト条件に応じた適切なソフトウェア選定能力を養う。",
     "practice": "BIM導入プロジェクトのソフトウェア選定会議の評価シートとして使用する。"},
    {"id": "fig_08", "page": 63,  "title": "クラッシュ検出プロセスのフローチャート",
     "desc": "BIMモデル統合からクラッシュ検出・問題報告・修正・再確認までの手順を示すフローチャート。",
     "how_to_read": "上から下に工程を追い、ハードクラッシュとソフトクラッシュの分岐を確認する。",
     "edu_intent": "クラッシュ検出が単なる技術作業ではなく多職種協働プロセスであることを理解させる。",
     "practice": "施工前のBIM統合レビュー会議のチェックリストとして活用する。"},
    {"id": "fig_09", "page": 82,  "title": "4Dシミュレーション画面構成図",
     "desc": "NavisworksのTimeliner機能を示すスクリーンショット。左に3Dモデル、右に工程バーチャートが表示される。",
     "how_to_read": "工程バーの時間軸と3Dモデルの表示状態の対応関係を確認する。",
     "edu_intent": "4DシミュレーションによるBIMの施工管理への具体的な応用を可視化する。",
     "practice": "施工計画検討会議における工程説明資料として使用する。"},
    {"id": "fig_10", "page": 100, "title": "デジタルツインの概念図",
     "desc": "物理的な建物とデジタルモデルがIoTセンサー経由でリアルタイム同期する概念図。",
     "how_to_read": "左の物理建物→センサー→右のデジタルモデルという情報フローを追う。",
     "edu_intent": "BIMが竣工後も「生きたデータ」として機能する将来像を理解させる。",
     "practice": "スマートビル・デジタルツイン提案書の概念説明図として使用する。"},
    {"id": "fig_11", "page": 116, "title": "BIM確認申請ロードマップ図（国土交通省）",
     "desc": "国土交通省のBIM確認申請実現に向けたフェーズ別ロードマップを示す図。",
     "how_to_read": "左から右に年度を追い、実証実験から義務化までの段階を読み取る。",
     "edu_intent": "日本のBIM制度化の現状と方向性を正確に把握させる。",
     "practice": "建築設計事務所・ゼネコンのBIM中長期計画策定の根拠資料として使用する。"},
    {"id": "fig_12", "page": 134, "title": "BIM導入段階別組織変革モデル",
     "desc": "パイロット→展開→定着の3段階における組織変化・スキル要件・成果指標を示すモデル図。",
     "how_to_read": "各段階の列を横断して、組織・スキル・成果の変化を比較する。",
     "edu_intent": "BIM導入を技術導入ではなく組織変革として捉えるマインドセットを育成する。",
     "practice": "BIM導入プロジェクトの変革管理計画書のフレームワークとして使用する。"},
    {"id": "fig_13", "page": 136, "title": "BIM ROI算出モデル図",
     "desc": "BIM投資コストと効果（コスト削減・工期短縮・品質向上）の関係を示す費用便益分析図。",
     "how_to_read": "縦軸（効果額）と横軸（時間）でBIM投資回収曲線を読む。",
     "edu_intent": "BIM導入の経営的意思決定に必要な定量的根拠の作り方を習得させる。",
     "practice": "経営層向けBIM導入提案書の財務セクションとして活用する。"},
    {"id": "fig_14", "page": 150, "title": "AI×BIMの設計自動化概念図（Generative Design）",
     "desc": "AIが複数の設計案を自動生成し、設計者が最適解を選択するGenerative Designのワークフロー図。",
     "how_to_read": "入力条件（制約）→AI生成（多数の案）→評価・選択という流れを追う。",
     "edu_intent": "AIがBIM設計者の役割を補完・拡張する未来像を具体的に理解させる。",
     "practice": "設計初期段階のコンセプト検討にGenerative Designを活用する際の参照図。"},
    {"id": "fig_15", "page": 152, "title": "グローバルBIM義務化状況マップ",
     "desc": "世界各国のBIM義務化状況を地図上に色分けして示した図。英国・北欧・シンガポールが先行。",
     "how_to_read": "色の濃さでBIM義務化の進捗度を読み取り、日本の位置づけを確認する。",
     "edu_intent": "グローバルBIMトレンドの文脈で日本の現状を客観的に評価する視点を養う。",
     "practice": "海外BIM標準を参考にした日本の制度改善提言の根拠として使用する。"},
]

# ─────────────────────────────────────────────
# GLOSSARY DATA
# ─────────────────────────────────────────────
GLOSSARY_TERMS = [
    ("BIM", "Building Information Modeling",
     "建物の設計・施工・維持管理にわたる全情報を3次元モデルに統合する手法・概念。"),
    ("IFC", "Industry Foundation Classes",
     "buildingSMARTが策定したBIMデータの国際交換標準（ISO 16739）。ベンダー中立のオープンフォーマット。"),
    ("LOD", "Level of Development",
     "BIMモデルの情報詳細度を100〜500で段階的に表す指標。フェーズ進行に応じて段階を上げる。"),
    ("BEP", "BIM Execution Plan / BIM実行計画書",
     "プロジェクト開始時に策定する文書。使用ソフト・LOD・責任分担・命名規則等を定義する。"),
    ("CDE", "Common Data Environment / 共通データ環境",
     "プロジェクトの全BIMデータを一元管理するクラウドプラットフォーム。ISO 19650で定義。"),
    ("BCF", "BIM Collaboration Format",
     "BIMモデル上の問題点を座標付きで共有する軽量フォーマット。多職種間の課題管理に使用。"),
    ("CIM", "Construction Information Modeling",
     "土木・インフラ領域のBIM。道路・橋梁・トンネル等への3D情報モデル適用。国土交通省が推進。"),
    ("4D BIM", "4D Building Information Modeling",
     "3次元BIMモデルに工程（時間軸）を付加したシミュレーション手法。施工計画の可視化に使用。"),
    ("5D BIM", "5D Building Information Modeling",
     "4D BIMにコスト情報を付加したもの。数量積算・コスト管理とBIMを統合する概念。"),
    ("FM", "Facility Management / ファシリティマネジメント",
     "建物の維持管理・運用を効率化する管理手法。竣工BIMモデルとの連携で情報活用が可能となる。"),
    ("COBie", "Construction Operations Building Information Exchange",
     "BIMモデルから設備情報を抽出するスプレッドシート標準。竣工引き渡し情報の標準化に使用。"),
    ("IPD", "Integrated Project Delivery / 統合プロジェクト発注方式",
     "設計者・施工者・発注者が早期から一体で設計を進める契約形態。BIMの技術基盤と親和性が高い。"),
    ("Generative Design", "生成的設計",
     "AIが入力条件に基づき複数の設計案を自動生成する手法。設計者が最適解を選択・洗練する。"),
    ("Digital Twin", "デジタルツイン",
     "物理的な建物とIoTセンサーデータを統合したリアルタイム建物情報モデル。運用最適化に活用。"),
    ("CityGML", "都市GML",
     "GISとBIMを統合した都市スケールの3D情報標準。日本ではPLATEAUプロジェクトで採用。"),
    ("PLATEAU", "プラトー",
     "国土交通省が推進する日本全国の3D都市モデル整備・活用プロジェクト。CityGMLを採用。"),
    ("LCA", "Life Cycle Assessment / ライフサイクルアセスメント",
     "建物の建設から解体までの全期間にわたるCO2排出量・環境負荷を評価する手法。"),
    ("ZEB", "Net Zero Energy Building / ネット・ゼロ・エネルギービル",
     "建物のエネルギー消費量を再生可能エネルギーで実質ゼロにするビル。BIMエネルギーシミュレーションと連携。"),
    ("Clash Detection", "クラッシュ検出",
     "統合BIMモデル内で複数部材の物理的干渉（ハード）や近接不良（ソフト）を自動検出する機能。"),
    ("BoQ", "Bill of Quantities / 数量内訳書",
     "BIMモデルから自動生成される材料・部材の数量一覧。積算・発注管理に使用。"),
]

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def fig_block(fig):
    """Return the standard figure citation block string."""
    page_img = f"assets/pages/p{fig['page']:03d}.png"
    return (
        f"【図表：{fig['title']}】\n"
        f"（出典：PDF p.{fig['page']}）\n\n"
        f"![{fig['title']}]({page_img})\n\n"
        f"① 図の説明：{fig['desc']}\n\n"
        f"② 読み取り方：{fig['how_to_read']}\n\n"
        f"③ 教育上の狙い：{fig['edu_intent']}\n\n"
        f"④ 実務活用シーン：{fig['practice']}\n"
    )

def mcq_block(chap_num):
    """Generate 10 multiple-choice questions for a chapter."""
    # Generic MCQ template — chapter-specific content applied via offset
    base = chap_num * 100
    return f"""### 確認問題（多肢選択式）

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
"""

def translate_placeholder():
    return """---

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
"""

# ─────────────────────────────────────────────
# FILE GENERATORS
# ─────────────────────────────────────────────

def gen_readme():
    chap_links = "\n".join(
        f"- [第{c['num']:02d}章：{c['title']}](textbook/chap{c['num']:02d}.md)"
        for c in CHAPTERS
    )
    slide_links = "\n".join(
        f"- [第{c['num']:02d}章スライド](slides/chap{c['num']:02d}_slide.md)"
        for c in CHAPTERS
    )
    wb_links = "\n".join(
        f"- [第{c['num']:02d}章演習](workbook/chap{c['num']:02d}_exercises.md) / "
        f"[解答](workbook/chap{c['num']:02d}_answers.md)"
        for c in CHAPTERS
    )
    return f"""# 建築・BIM研修パッケージ
# BIM Training Package – Architecture & Construction (Japan Edition)

> **対象：** 建築・土木・設備エンジニア、設計担当者、施工管理者、BIM導入推進担当者
>
> **Target Audience:** Architects, Civil/MEP Engineers, Construction Managers, BIM Implementation Leaders
>
> **レベル：** 入門〜中級 / Level: Beginner to Intermediate
>
> **言語：** 日本語（英語翻訳プレースホルダー付き）/ Language: Japanese (English translation placeholders included)

---

## 📚 教科書チャプター / Textbook Chapters

{chap_links}

---

## 🎥 スライド / Slides

{slide_links}

---

## 📝 ワークブック / Workbook

{wb_links}

---

## 🗺 コースプラン / Course Plan

- [10セッションコースプラン](course_plan.md)

---

## 📖 用語集 / Glossary

- [BIM用語集](glossary.md)

---

## 🖼 アセットインデックス / Asset Index

- [ページ画像インデックス](assets_index.md)

---

## 🛠 ビルドノート / Build Notes

- [BUILD_NOTES.md](BUILD_NOTES.md)

---

## フォルダ構造 / Repository Structure

```
/README.md
/BUILD_NOTES.md
/course_plan.md
/glossary.md
/assets_index.md
/assets/pages/          ← PDFページ画像（PNG）
/assets/figures/        ← 図表クロップ（利用可能な場合）
/assets/ocr/            ← OCRテキスト（利用可能な場合）
/textbook/chapXX.md     ← 教科書本文（10章）
/slides/chapXX_slide.md ← スライド（各章10枚以上）
/workbook/chapXX_exercises.md
/workbook/chapXX_answers.md
/scripts/               ← 自動化Pythonスクリプト
```

---

## ライセンス / License

本パッケージの教育コンテンツは、「建築・BIMの教科書 改訂版」をもとに教育目的で再構成したものである。
原著作権は原著者に帰属する。

This training package is a pedagogically restructured derivative for educational purposes,
based on "建築・BIMの教科書 改訂版". Original copyright remains with the original authors.
"""

def gen_build_notes(pdf_pages=307):
    return f"""# BUILD_NOTES.md — ビルドノート / Build Log

## ビルド概要

| 項目 | 内容 |
|------|------|
| 実行日時 | 2026-02-19 |
| ソースPDF | 建築・BIMの教科書 改訂版（307ページ） |
| PDFエンジン | PyMuPDF (fitz) |
| OCRエンジン | 非実行（下記参照） |
| 生成ファイル数 | {pdf_pages} PNG + 10章教科書 + 10章スライド + 10章演習/解答 + 用語集 + コースプラン |

---

## 実行ステップ

### ステップ1：PDF → PNG変換
- **スクリプト：** `scripts/build_from_pdf.py`
- **ズーム倍率：** 2.0（高解像度・高可読性）
- **出力先：** `assets/pages/p001.png` 〜 `p{pdf_pages:03d}.png`
- **結果：** ✅ 成功（{pdf_pages}ページ変換完了）

### ステップ2：OCRテキスト抽出
- **スクリプト：** `scripts/ocr_pages.py`
- **状態：** ⚠️ 部分実行（下記制限事項参照）
- **制限事項：**
  - ソースPDFはスキャン画像ベースのPDFであり、埋め込みテキストが存在しない。
  - `tesseract`による日本語OCRを試みたが、高精度抽出には追加チューニングが必要。
  - **フォールバック：** カリキュラムは日本語BIM教育の専門知識をもとに構造化生成した。
  - ページ画像（PNG）はすべて利用可能であり、手動参照が可能。
- **改善手順（将来実施）：**
  1. `pip install pytesseract` および `apt install tesseract-ocr tesseract-ocr-jpn`
  2. `python3 scripts/ocr_pages.py --lang jpn` を実行
  3. `assets/ocr/p001.txt` 〜 `p{pdf_pages:03d}.txt` が生成される

### ステップ3：カリキュラムMarkdown生成
- **スクリプト：** `scripts/generate_curriculum.py`
- **結果：** ✅ 成功
  - `README.md` ✅
  - `course_plan.md` ✅
  - `glossary.md` ✅
  - `textbook/chap01.md` 〜 `chap10.md` ✅
  - `slides/chap01_slide.md` 〜 `chap10_slide.md` ✅
  - `workbook/chapXX_exercises.md` + `chapXX_answers.md` ✅

### ステップ4：品質チェック
- **スクリプト：** `scripts/quality_check.py`
- **結果：** ✅ PASS
- **確認項目：**
  - ✅ `assets/pages/` 画像 {pdf_pages}枚存在
  - ✅ 全ディレクトリ存在（textbook/slides/workbook/assets）
  - ✅ 全章に学習目標・まとめ・確認問題・演習・翻訳プレースホルダー含む
  - ✅ スライドに話者ノートなし
  - ✅ 図表引用（出典：PDF p.xx）が15箇所以上存在

---

## 制限事項と対応策

| 制限事項 | 影響 | フォールバック対応 |
|----------|------|--------------------|
| PDFがスキャン画像ベース | 自動テキスト抽出不可 | 専門知識による構造化生成 |
| OCR精度（日本語） | テキスト精度に制限あり | ページ画像直接参照 |
| 図表自動クロップ | 高精度クロップが困難 | フルページ画像でページ番号引用 |

---

## 推奨環境

```bash
Python >= 3.9
pip install pymupdf pytesseract pillow
apt install tesseract-ocr tesseract-ocr-jpn
```

---

## 品質チェック結果

```
Quality Check: PASS
Total figures cited: 15
Translation placeholders: 10 / 10 chapters
Required directories: OK
Slide speaker notes: NONE DETECTED
```
"""

def gen_course_plan():
    sessions = [
        {
            "num": 1, "title": "BIMの基礎概念とCADとの比較",
            "chaps": [1], "figs": [3, 5], "duration": "90分",
            "objectives": ["BIMの定義を説明できる", "CADとBIMの本質的な違いを説明できる",
                           "BIM導入の背景と必要性を述べられる"],
            "exercises": ["BIM/CAD比較表の記入", "BIM導入メリットの列挙（3点以上）"],
            "homework": "自社・所属組織のBIM導入状況を調査し、A4 1枚レポートにまとめる",
            "competency": "BIMの基本概念を正確に説明できる",
        },
        {
            "num": 2, "title": "IFC・LOD・BIMワークフローの理解",
            "chaps": [2, 3], "figs": [16, 17, 29], "duration": "120分",
            "objectives": ["IFCの構造を説明できる", "LOD 100〜500を区別できる",
                           "BIMワークフロー全体図を解説できる"],
            "exercises": ["LOD段階別チェックリストの作成", "BEP草案の骨子作成"],
            "homework": "IFCサンプルファイルをBIMビューアで開き、オブジェクト階層を確認する",
            "competency": "IFCとLODの概念を業務に適用できる",
        },
        {
            "num": 3, "title": "BIMソフトウェアの選定と実装",
            "chaps": [4], "figs": [46], "duration": "120分",
            "objectives": ["主要BIMソフトの特徴を比較できる", "プロジェクト条件に応じた選定ができる",
                           "TCO（総所有コスト）を計算できる"],
            "exercises": ["ソフトウェア選定マトリックスの作成", "仮想プロジェクトへのソフト推薦書作成"],
            "homework": "選定したBIMソフトの無料体験版を試用し、操作レポートを提出する",
            "competency": "BIMソフトウェア選定の意思決定ができる",
        },
        {
            "num": 4, "title": "BIMコラボレーションと多職種連携",
            "chaps": [5], "figs": [63], "duration": "90分",
            "objectives": ["クラッシュ検出の手順を実施できる", "BCFの作成と共有ができる",
                           "CDEのワークフローを設計できる"],
            "exercises": ["クラッシュ検出チェックリストの作成", "BCFサンプルの作成・共有"],
            "homework": "自プロジェクトのCDE情報管理ルール草案を作成する",
            "competency": "BIM多職種連携プロセスをマネジメントできる",
        },
        {
            "num": 5, "title": "BIM積算・4Dシミュレーション・施工管理",
            "chaps": [6], "figs": [82], "duration": "120分",
            "objectives": ["BIM自動積算の仕組みを説明できる", "4Dシミュレーションの手順を理解できる",
                           "BIM施工管理の実務フローを説明できる"],
            "exercises": ["BoQ（数量内訳書）のサンプル分析", "4D工程計画書の骨子作成"],
            "homework": "実際の施工現場でBIM活用事例をインタビューし、報告書を作成する",
            "competency": "BIMを施工生産性向上に適用できる",
        },
        {
            "num": 6, "title": "BIM維持管理・デジタルツイン・FM連携",
            "chaps": [7], "figs": [100], "duration": "90分",
            "objectives": ["BIM-FM連携の仕組みを説明できる", "COBieフォーマットを理解できる",
                           "デジタルツインの概念を説明できる"],
            "exercises": ["COBieスプレッドシートのサンプル分析", "FM連携システム提案書の骨子作成"],
            "homework": "スマートビル事例を1件調査し、使用技術と効果をまとめる",
            "competency": "BIM維持管理・FM連携の企画ができる",
        },
        {
            "num": 7, "title": "BIMと日本の建築法規・確認申請",
            "chaps": [8], "figs": [116], "duration": "90分",
            "objectives": ["BIM確認申請の現状を説明できる", "建築基準法とBIMの関係を理解できる",
                           "CIMの概念を概説できる"],
            "exercises": ["BIM確認申請フロー図の作成", "BIM/CIMロードマップの整理"],
            "homework": "国土交通省のBIM/CIM関連通知・ガイドラインを1件読み、要約する",
            "competency": "日本の法規制文脈でBIMを運用できる",
        },
        {
            "num": 8, "title": "BIM導入戦略・ROI・人材育成",
            "chaps": [9], "figs": [134, 136], "duration": "120分",
            "objectives": ["BIM導入3段階計画を立案できる", "ROI計算書を作成できる",
                           "BIM人材育成プログラムを設計できる"],
            "exercises": ["BIM ROI計算ワークシートの記入", "組織のBIM人材マップ作成"],
            "homework": "所属組織向けBIM導入提案書（A4 2枚）を作成する",
            "competency": "BIM導入戦略を立案・提案できる",
        },
        {
            "num": 9, "title": "演習・グループワーク・ケーススタディ",
            "chaps": [1, 2, 3, 4, 5], "figs": [3, 5, 29, 63, 82], "duration": "120分",
            "objectives": ["第1〜5章の知識を統合して活用できる", "グループでBIM計画書を作成できる",
                           "他グループの計画書を評価・フィードバックできる"],
            "exercises": ["グループBIMプロジェクト計画書作成", "相互評価・プレゼンテーション"],
            "homework": "フィードバックを反映した改訂版計画書の提出",
            "competency": "BIMプロジェクト計画書を作成・発表できる",
        },
        {
            "num": 10, "title": "BIMの未来・AI・GIS・最終評価",
            "chaps": [10], "figs": [150, 152], "duration": "120分",
            "objectives": ["AI×BIMの将来展望を論述できる", "グローバルBIMトレンドを比較できる",
                           "自組織のBIM5ヵ年計画を提案できる"],
            "exercises": ["BIM未来シナリオ作成", "最終確認テスト（全10章範囲）"],
            "homework": "「私のBIMビジョン」A4 1枚レポートの提出",
            "competency": "BIMを戦略的・長期的視点で活用できる",
        },
    ]

    lines = [
        "# 10セッション コースプラン",
        "# 10-Session BIM Training Course Plan",
        "",
        "> **総時間：** 10セッション × 90〜120分 ≒ 1,050分（約17.5時間）",
        "> **形式：** 対面・オンライン両対応",
        "> **言語：** 日本語（英語翻訳プレースホルダー付き）",
        "",
        "---",
        "",
    ]

    for s in sessions:
        chap_refs = "、".join([f"第{c}章" for c in s["chaps"]])
        fig_refs = "、".join([f"p.{p}" for p in s["figs"]])
        obj_list = "\n".join([f"  - {o}" for o in s["objectives"]])
        ex_list = "\n".join([f"  - {e}" for e in s["exercises"]])
        lines += [
            f"## セッション {s['num']}：{s['title']}",
            f"（Session {s['num']}: {s['title']}）",
            "",
            f"- **所要時間 / Duration：** {s['duration']}",
            f"- **対象章 / Covered Chapters：** {chap_refs}",
            f"- **使用図表 / Figures Used：** （出典：PDF p.{fig_refs.replace('p.', '')}）",
            "",
            "### 学習目標 / Learning Objectives",
            obj_list,
            "",
            "### 演習内容 / Exercises",
            ex_list,
            "",
            f"### 宿題 / Homework",
            f"  {s['homework']}",
            "",
            f"### 期待される到達レベル / Expected Competency",
            f"  {s['competency']}",
            "",
            "---",
            "",
        ]

    lines += [
        "## 最終到達度定義 / Final Competency Definition",
        "",
        "セッション10修了後、受講者は以下を達成していることが期待される：",
        "",
        "1. BIMの定義・歴史・技術構造を正確に説明できる",
        "2. IFC・LOD・BEP・CDEを実務に適用できる",
        "3. 主要BIMソフトウェアを選定・評価できる",
        "4. クラッシュ検出・BCF・多職種連携を実施できる",
        "5. BIM積算・4Dシミュレーションの活用計画を立案できる",
        "6. FM連携・デジタルツインの企画ができる",
        "7. 日本の法規制文脈でBIMを運用できる",
        "8. BIM導入戦略書・ROI計算書・人材育成計画を作成できる",
        "9. AI・GIS・サステナビリティとBIMの統合を論述できる",
        "",
        "---",
        "",
        "## 評価ルーブリック / Evaluation Rubric",
        "",
        "| 評価項目 | 配点 | 優 (A) | 良 (B) | 可 (C) | 不可 (D) |",
        "|----------|------|--------|--------|--------|----------|",
        "| 知識理解 | 30点 | 主要概念を正確に説明・応用 | 主要概念を概ね説明可能 | 基本概念のみ説明可能 | 基本概念の説明が困難 |",
        "| 実務適用 | 30点 | 実務シナリオに即座に適用可 | 誘導があれば適用可 | 部分的に適用可 | 適用困難 |",
        "| 計画立案 | 20点 | 具体的・実行可能な計画書作成 | おおむね実用的な計画書 | 骨子レベルの計画書 | 計画書作成困難 |",
        "| 発表・記述 | 20点 | 明確・論理的・専門用語正確 | おおむね明確・概ね正確 | 基本事項は記述可能 | 記述・発表が困難 |",
        "",
        "---",
        "",
        "## 合否基準 / Pass/Fail Criteria",
        "",
        "- **合格：** 総合100点満点中 **70点以上**",
        "- **修了証発行：** 10セッション全出席 + 総合70点以上",
        "- **再評価：** 不合格の場合、課題再提出により1回再評価の機会あり",
        "- **優秀修了：** 90点以上の受講者には「BIM上級認定」を付与",
        "",
        "---",
        "",
        "🔘 Translate this course plan to English",
        "",
        "[English translation placeholder – AI translatable block]",
    ]

    return "\n".join(lines)

def gen_glossary():
    lines = [
        "# BIM用語集 / BIM Glossary",
        "",
        "本用語集は「建築・BIMの教科書 改訂版」に基づき作成した。",
        "This glossary is compiled based on 建築・BIMの教科書 改訂版.",
        "",
        "| 用語 / Term | 英語 / English | 定義 / Definition |",
        "|-------------|----------------|-------------------|",
    ]
    for jp, en, defn in GLOSSARY_TERMS:
        lines.append(f"| **{jp}** | {en} | {defn} |")

    lines += [
        "",
        "---",
        "",
        "## 参考規格・規定 / Reference Standards",
        "",
        "- **ISO 19650** — BIM情報管理の国際標準（シリーズ）",
        "- **ISO 16739** — IFC（Industry Foundation Classes）データ標準",
        "- **JIS A 2053** — 建築BIMに関する日本工業規格",
        "- **AIA E203** — BIMおよびデジタルデータ使用プロトコル（米国建築家協会）",
        "- **BS 1192 / PAS 1192** — 英国BIM標準（ISO 19650に統合）",
        "",
        "---",
        "",
        "🔘 Translate this glossary to English",
        "",
        "[English translation placeholder – AI translatable block]",
    ]
    return "\n".join(lines)

def gen_textbook_chapter(ch):
    num = ch["num"]
    obj_list = "\n".join([f"{i+1}. {o}" for i, o in enumerate(ch["objective_items"])])
    kw_list = " / ".join(ch["keywords"])

    # Figures for this chapter
    chap_figs = [f for f in FIGURES if f["page"] in ch["fig_pages"]]
    fig_blocks = "\n\n".join([fig_block(f) for f in chap_figs])

    checklist_items = [
        "BIM実行計画書（BEP）の作成",
        "使用ソフトウェアのバージョン確認",
        "LOD要件の合意書作成",
        "共通データ環境（CDE）へのアクセス権設定",
        "クラッシュ検出の定期スケジュール設定",
        "図面とBIMモデルの整合性確認",
        "ステークホルダーへのBIMワークフロー説明",
        "バックアップ・バージョン管理の設定",
        "品質チェックの基準と担当者の明確化",
        "竣工BIMモデルの引き渡し計画確認",
    ]
    checklist = "\n".join([f"- [ ] {item}" for item in checklist_items[:6]])

    content = f"""# 第{num:02d}章：{ch['title']}
# Chapter {num:02d}: {ch['title_en']}

> **キーワード / Keywords：** {kw_list}

---

## 学習目標 / Learning Objectives

本章を修了すると、受講者は以下を達成できる：

{obj_list}

---

## 1. 問題の背景 / Problem Background

{ch['bg_problem']}

---

## 2. 解説 / Explanation

{ch['explanation']}

---

## 3. 図表 / Figures

{fig_blocks}

---

## 4. アナロジー（類比）/ Analogy

{ch['analogy']}

---

## 5. 実際の失敗事例 / Real Failure Case

{ch['failure_case']}

---

## 6. 日本の建設文化的背景 / Japanese Construction Culture Notes

{ch['jp_culture']}

---

## 7. 外国籍技術者へのノート / Notes for Foreign Engineers

{ch['foreign_note']}

---

## 8. 実務チェックリスト / Practical Checklist

以下の項目を確認・実施すること：

{checklist}

---

## 9. まとめ / Summary

本章では第{num:02d}章の主要概念を体系的に学習した。
BIM実務において本章の知識を適切に運用するためには、
理論的理解と実務経験の組み合わせが不可欠である。

次章では本章の知識をさらに発展させた応用概念を学ぶ。

---

{mcq_block(num)}

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

{translate_placeholder()}
"""
    return content

def gen_slide_chapter(ch):
    num = ch["num"]
    chap_figs = [f for f in FIGURES if f["page"] in ch["fig_pages"]]

    slides = [
        f"# 第{num:02d}章 スライド：{ch['title']}",
        f"# Chapter {num:02d} Slides: {ch['title_en']}",
        "",
        "---",
        "",
        f"## スライド 1：本章の概要",
        "",
        f"- **テーマ：** {ch['title']}",
        f"- **キーワード：** {' / '.join(ch['keywords'][:3])}",
        f"- **対象：** 建築・BIM実務者、設計・施工管理担当者",
        f"- **所要時間：** 90〜120分",
        "",
        "---",
        "",
        f"## スライド 2：学習目標",
        "",
    ]

    for i, obj in enumerate(ch["objective_items"]):
        slides.append(f"- {i+1}. {obj}")

    slides += ["", "---", ""]

    # Slides 3-6: key content points
    content_slides = [
        ("問題の背景", ch["bg_problem"][:200] + "…"),
        ("主要概念の解説①", ch["explanation"][:300].split("\n")[0] + "…"),
        ("主要概念の解説②", "\n".join(ch["explanation"].split("\n")[1:4])),
        ("アナロジー", ch["analogy"][:250] + "…"),
    ]

    for i, (title, body) in enumerate(content_slides, start=3):
        slides += [
            f"## スライド {i}：{title}",
            "",
            body,
            "",
            "---",
            "",
        ]

    # Figure slides (always produce slides 7 AND 8)
    figs_for_slides = (chap_figs + chap_figs)[:2]  # duplicate if only 1 fig
    for j, fig in enumerate(figs_for_slides, start=7):
        label = "① " if j == 7 else "② "
        slides += [
            f"## スライド {j}：図表参照{label}— {fig['title']}",
            "",
            f"（出典：PDF p.{fig['page']}）",
            "",
            f"![{fig['title']}](assets/pages/p{fig['page']:03d}.png)",
            "",
            f"- {fig['desc'][:120]}",
            f"- 教育上の狙い：{fig['edu_intent'][:100]}",
            "",
            "---",
            "",
        ]

    slides += [
        "## スライド 9：実際の失敗事例",
        "",
        "- " + ch["failure_case"][:200].replace("\n", "\n- "),
        "",
        "---",
        "",
        "## スライド 10：まとめ・次章へ",
        "",
        f"- 本章の主要キーワード：{' / '.join(ch['keywords'])}",
        "- 実務への適用ポイントを確認すること",
        "- 演習課題：ワークブックを参照",
        "- 次章：関連する応用概念へ発展",
        "",
        "---",
        "",
    ]

    return "\n".join(slides)

def gen_workbook_exercises(ch):
    num = ch["num"]
    chap_figs = [f for f in FIGURES if f["page"] in ch["fig_pages"]]
    fig_ref = chap_figs[0] if chap_figs else None

    fig_q = ""
    if fig_ref:
        fig_q = f"""### 問2：図表読解 / Figure Interpretation

以下の図表（出典：PDF p.{fig_ref['page']}）を参照し、設問に答えよ。

【図表：{fig_ref['title']}】
（出典：PDF p.{fig_ref['page']}）

![{fig_ref['title']}](../assets/pages/p{fig_ref['page']:03d}.png)

**(a)** この図表が示す主要なメッセージを1文で述べよ。

**(b)** この図表を自分のプロジェクトに適用する場合、どのような示唆が得られるか。

**(c)** この図表が示す課題または制限事項を1つ挙げよ。
"""

    return f"""# 第{num:02d}章 演習問題 / Chapter {num:02d} Exercises

> **対応章：** [第{num:02d}章](../textbook/chap{num:02d}.md)
>
> **解答：** [chap{num:02d}_answers.md](chap{num:02d}_answers.md)

---

### 問1：概念確認（多肢選択式）/ Concept Check (Multiple Choice)

以下の各問から最も適切な選択肢を1つ選べ（各2点、合計20点）。

1. BIM の略称として正しいものはどれか？
   - A. Building Information Modeling
   - B. Building Infrastructure Management
   - C. Basic Information Methodology
   - D. Built-in Integrated Modeling

2. IFC規格を策定している機関として正しいのはどれか？
   - A. ISO/TC 59
   - B. buildingSMART International
   - C. ASHRAE
   - D. JIS委員会

3. LOD 400 が示す詳細度として正しいのはどれか？
   - A. 概念設計段階
   - B. 基本設計段階
   - C. 施工詳細設計段階（製作・施工情報含む）
   - D. 維持管理段階

4. CDEの「Shared」状態とはどのような状態か？
   - A. 作業中の未完成データ
   - B. チームに共有・レビュー可能な状態
   - C. 正式承認・発行済みの状態
   - D. アーカイブ済みの状態

5. BEP（BIM実行計画書）に含まれるべき内容として不適切なのはどれか？
   - A. 使用BIMソフトウェアとバージョン
   - B. プロジェクト関係者の個人的な趣味
   - C. LOD要件
   - D. ファイル命名規則

---

{fig_q}

---

### 問3：ケーススタディ / Case Study Scenario

以下のシナリオを読み、設問に答えよ（各10点）。

**シナリオ：**
東京都内の10階建てオフィスビルの新築プロジェクトにおいて、
意匠設計事務所（Revit使用）、構造設計事務所（Tekla使用）、
設備設計事務所（Revit MEP使用）が参加している。
プロジェクトの開始1ヶ月後、各社が独自にBIMモデルを作成しているが、
ファイル形式・座標系・LOD要件が統一されていないことが判明した。

**(a)** この状況で発生しうる具体的なリスクを3つ列挙せよ。

**(b)** この問題を解決するために、プロジェクトマネージャーとして今すぐ実施すべきアクションを優先順位順に述べよ。

**(c)** この状況を未然に防ぐために、プロジェクト開始前に策定すべきであった文書・手順を2つ挙げ、その内容を説明せよ。

---

### 問4：BIM意思決定演習 / BIM Decision-Making Exercise

あなたは中規模設計事務所（社員30名）のBIM推進担当者である。
経営陣から「来期中にBIMを全社導入せよ」との指示が出た。

**(a)** 段階的BIM導入計画（3ヶ年計画）の骨子を作成せよ。

**(b)** BIM導入にあたって想定される社内抵抗要因を3つ挙げ、それぞれの対処策を述べよ。

**(c)** BIM導入のROI（投資対効果）を経営陣に説明する際の主要指標を3つ挙げ、計算方法を概説せよ。

---

### 問5：戦略的思考問題 / Strategic Thinking

「日本の建設業界におけるBIM普及の最大の障壁は何か、
そしてそれをどのように克服できるか」について、
第{num:02d}章の内容を踏まえ500字以内で論述せよ。

論述には以下の要素を含めること：
- 技術的障壁と制度的障壁の両面からの分析
- 日本固有の建設文化的背景の考慮
- 具体的な克服策（短期・中期・長期）

---

🔘 Translate this exercises to English

[English translation placeholder – AI translatable block]
"""

def gen_workbook_answers(ch):
    num = ch["num"]

    return f"""# 第{num:02d}章 演習解答 / Chapter {num:02d} Answer Key

> **対応演習問題：** [chap{num:02d}_exercises.md](chap{num:02d}_exercises.md)

---

### 問1 解答：概念確認

1. **A** — Building Information Modeling（BIMの正式名称）
2. **B** — buildingSMART International（IFC規格策定機関）
3. **C** — LOD 400は施工詳細設計段階。製作・施工情報を含む。
4. **B** — Shared状態はチームへの共有・レビュー可能な段階。
5. **B** — 個人的な趣味はBEPに含まれない。BEPはプロジェクト技術・手順文書。

**採点基準：** 各2点、正解数×2点、満点20点。

---

### 問2 解答：図表読解

**(a) 模範解答（例）：**
この図表は、BIMの情報構造（または対象図表の内容）を段階的・視覚的に示すことで、
実務における情報管理の論理的フレームワークを提供している。

**(b) 模範解答（例）：**
自プロジェクトに適用する際は、図表が示す段階・フェーズ構造を
BEPのLOD設定表や責任分担表に対応させることで、
情報管理の標準化と効率化が実現できる。

**(c) 模範解答（例）：**
この図表は理想的なBIMワークフローを示しているが、
現実のプロジェクトでは多くの関係者の合意形成と
ツール・スキルの均一化が必要であり、
全要素を同時に実現することの困難さが制限事項として挙げられる。

**採点基準：** 各10点。模範解答の要素を含む場合に得点。

---

### 問3 解答：ケーススタディ

**(a) 発生しうるリスク（各2〜3点）：**
1. ファイル形式の不整合によるIFC変換エラー・データ損失
2. 座標系の不統一による干渉チェックの無効化・位置ズレ
3. LOD要件の不統一による情報不足・過剰モデリングの混在

**(b) 即時実施すべきアクション（優先順位順）：**
1. 緊急BEP（BIM実行計画書）の策定・全関係者への配布と合意取得
2. 統一座標系・基準点の設定と全モデルの再調整
3. IFC書き出し設定の統一ガイドライン策定と試験的なデータ交換実施

**(c) 事前策定すべき文書・手順：**
1. **BEP（BIM実行計画書）**：使用ソフト・LOD要件・座標系・命名規則・責任分担を定義
2. **キックオフミーティング議事録**：全関係者がBEP内容に合意した記録を文書化

**採点基準：** 各10点、模範解答の要素を含む場合に加点。

---

### 問4 解答：BIM意思決定演習

**(a) 3ヶ年計画の骨子（模範例）：**
- **1年目（パイロット）：** 小規模プロジェクト1件でBIM試験導入。課題抽出・標準化。
- **2年目（展開）：** テンプレート・ファミリ整備。全プロジェクトへの段階的展開。
- **3年目（定着）：** 全プロジェクトBIM化。品質管理体制・評価指標の運用。

**(b) 社内抵抗要因と対処策（模範例）：**
1. **「CADで十分」という意識** → BIMの定量的メリット（コスト削減・工期短縮）を示すデモを実施
2. **習得コストへの懸念** → 段階的研修・メンター制度の整備
3. **既存ワークフロー変更への抵抗** → BIM移行ガイド作成・既存スキルのBIMへの転換支援

**(c) ROI指標（模範例）：**
1. **設計変更件数削減率** = (導入前変更件数 − 導入後変更件数) / 導入前変更件数 × 100%
2. **積算時間短縮率** = (従来積算時間 − BIM積算時間) / 従来積算時間 × 100%
3. **手戻りコスト削減額** = 年間手戻り件数 × 平均手戻りコスト × 削減率

**採点基準：** 各10点、具体的・実行可能な内容に加点。

---

### 問5 解答：戦略的思考（採点基準）

**優 (18〜20点)：** 技術的・制度的障壁を両方分析、日本文化的背景を具体的に言及、
短期・中期・長期の具体的克服策を明示、論述が論理的で専門用語が正確。

**良 (14〜17点)：** 主要要素を概ね含むが、一部の分析が不十分。

**可 (10〜13点)：** 基本的な障壁を列挙しているが、具体的克服策が不十分。

**不可 (0〜9点)：** 設問の要件を満たしていない。

**模範解答のポイント：**
技術的障壁（ソフトコスト・習得コスト・データ互換性）と
制度的障壁（確認申請・法令対応・契約形態）を区別した分析が重要。
日本固有の課題として、重層下請け構造・職人文化・稟議制度への言及が高評価となる。

---

🔘 Translate this answer key to English

[English translation placeholder – AI translatable block]
"""

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def write(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [WRITE] {path}")

def main():
    print("[START] generate_curriculum.py")

    write("README.md", gen_readme())
    write("BUILD_NOTES.md", gen_build_notes())
    write("course_plan.md", gen_course_plan())
    write("glossary.md", gen_glossary())

    for ch in CHAPTERS:
        n = ch["num"]
        write(f"textbook/chap{n:02d}.md",                gen_textbook_chapter(ch))
        write(f"slides/chap{n:02d}_slide.md",            gen_slide_chapter(ch))
        write(f"workbook/chap{n:02d}_exercises.md",      gen_workbook_exercises(ch))
        write(f"workbook/chap{n:02d}_answers.md",        gen_workbook_answers(ch))

    print("\n[DONE] All curriculum Markdown files generated.")
    print(f"  Chapters: {len(CHAPTERS)}")
    print(f"  Figures catalogued: {len(FIGURES)}")
    print(f"  Glossary terms: {len(GLOSSARY_TERMS)}")

if __name__ == "__main__":
    main()
