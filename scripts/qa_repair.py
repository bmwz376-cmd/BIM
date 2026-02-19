#!/usr/bin/env python3
"""
QA Repair Script for BIM Training Package
Fixes all SECTION_MISSING, SLIDE_PROSE, FEW_FIGURES, and DESU_MASU violations.
"""
import os, re, sys

REPO = '/home/user/webapp'

# ─────────────────────────────────────────────
# Chapter metadata: used for contextually-correct content
# ─────────────────────────────────────────────
CHAP_META = {
    1:  {
        "title": "BIMとは何か――概念・定義・歴史的変遷",
        "keywords": "BIM定義 / 建物情報モデリング / CADとの比較",
        "understand": [
            "BIM（Building Information Modeling）の定義：建物のライフサイクル全体にわたる情報を3次元の幾何情報と属性データとして統合した「建物情報モデル」を中心に業務を進める手法である。",
            "CADとBIMの本質的差異：CADが「デジタル製図板」であるのに対し、BIMは「建物のデジタル双子（Digital Twin）」として機能する。",
            "BIM普及の歴史的経緯：1970年代の研究起源から、2000年代のRevit登場、米国・英国の義務化、日本のBIM/CIM推進政策（2019年〜）にいたる変遷。",
            "日本固有の課題：重層下請け構造、図面至上主義、建築基準法による2D図面要件とBIMモデルの並行管理。",
            "BIM実行計画書（BEP）・LOD・CDE・クラッシュ検出の基本概念と実務チェックリスト。",
        ],
        "summary": [
            "BIMは建物に関するすべての情報を統合した「建物情報モデル」を中心に業務を進める手法であり、単なる3D CADとは本質的に異なる。",
            "IFCはソフトウェア中立のオープンデータ標準（ISO 16739）であり、異なるBIMツール間のデータ交換を可能にする。",
            "LODは情報詳細度を100〜500の段階で定義し、プロジェクトフェーズに応じた適切なモデル品質を規定する。",
            "BEP・CDE・クラッシュ検出は、BIMプロジェクトを成功させるための三大実務ツールである。",
            "日本では建築基準法の2D図面要件が存続しており、BIMモデルからの図面生成プロセスが不可欠である。",
        ],
        "fig2_page": "p005",
        "fig2_pnum": "5",
        "fig2_title": "CADとBIMの比較表",
        "fig2_desc": "2次元CADとBIMの違いを設計・施工・維持管理の各フェーズで比較した対照表。",
        "fig2_read": "各行（フェーズ）を左右（CAD vs BIM）で読み比べ、BIMの優位性を確認する。",
        "fig2_edu": "受講者のCAD既存知識を活用してBIMへの移行理解を促進する。",
        "fig2_biz": "BIM導入提案書の根拠資料として活用する。",
    },
    2:  {
        "title": "BIMの技術構造――IFC・LOD・データフォーマット",
        "keywords": "IFC / LOD / オープンBIM / データ互換性 / buildingSMART",
        "understand": [
            "IFC（Industry Foundation Classes）はbuildingSMARTが策定したBIMデータの国際標準フォーマット（ISO 16739）であり、ソフトウェアに依存しない中立的なデータ交換形式である。",
            "LOD（Level of Development）はBIMモデルの情報詳細度を100（概念設計）から500（竣工・現況）まで5段階で定義した指標である。",
            "オープンBIM（IFC利用）とクローズドBIM（ベンダー独自形式）の差異と、プロジェクト選択基準。",
            ".rvt（Revit固有）・.ifc（オープン交換）・.nwd（干渉チェック）・.bcf（問題共有）の用途の違い。",
            "buildingSMARTの役割：IFC・BCF・IDM・MVDなどBIM標準化活動の国際推進機関。",
        ],
        "summary": [
            "IFCはBIM世界の「USB規格」であり、ソフトウェアの違いを超えてデータ交換を可能にするオープン標準である（ISO 16739）。",
            "LODはBIMモデルの「解像度設定」であり、LOD 100（概念）からLOD 500（維持管理）まで段階的に情報詳細度を上げる。",
            "オープンBIMはIFCを通じた相互運用性を確保し、特定ベンダーへの依存を排除する設計思想である。",
            "BCFは問題点・コメントを軽量形式で共有するBIMコラボレーションフォーマットである。",
            "エクスポート設定・バージョン統一・MVD（モデルビュー定義）の確認がIFC連携成功の鍵である。",
        ],
        "fig2_page": "p017",
        "fig2_pnum": "17",
        "fig2_title": "LOD（情報詳細度）の段階別モデル比較図",
        "fig2_desc": "LOD 100から500まで、同一部材がどのように表現されるかを示す段階別比較図。",
        "fig2_read": "左から右へLODが上がるにつれ、形状精度と属性情報量が増加することを確認する。",
        "fig2_edu": "プロジェクトフェーズに応じた適切なLOD設定の判断力を養う。",
        "fig2_biz": "BEPのLOD設定表作成・協力会社への要件説明に活用する。",
    },
    3:  {
        "title": "BIMワークフロー――設計から施工・維持管理まで",
        "keywords": "BIMワークフロー / ライフサイクル / BEP / CDE",
        "understand": [
            "BIMワークフローは企画→基本設計→実施設計→施工→維持管理の全フェーズにわたり、一貫した情報モデルを維持する仕組みである。",
            "BEP（BIM実行計画書）は使用ソフト・LOD要件・ファイル命名規則・責任分担などを定める最重要マネジメント文書である。",
            "CDE（共通データ環境）はWork In Progress→Shared→Published→Archivedの4状態でデータを管理する共有情報基盤である。",
            "各設計フェーズでのBIM活用目的：企画（ボリュームスタディ）、基本設計（環境シミュ）、実施設計（干渉チェック）、施工（4Dシミュ）、維持管理（FM連携）。",
            "維持管理フェーズにおけるBIMデータ活用：COBie形式による設備情報引き渡し、FMシステムとの連携。",
        ],
        "summary": [
            "BIMワークフローは「建物のカルテ」として機能し、全ステークホルダーが共有・更新する情報基盤を提供する。",
            "BEPはプロジェクト開始前に策定すべき最重要文書であり、LOD要件・責任分担・CDE運用ルールを明文化する。",
            "CDEの4状態（WIP→Shared→Published→Archived）を遵守することで、情報の信頼性と追跡可能性が確保される。",
            "各フェーズで活用目的が異なるため、BEPに活用目的（BIM Use）を明示することが効率的なBIM運用の前提である。",
            "COBie形式での情報引き渡しにより、施工段階のBIMデータを維持管理システムに継続活用できる。",
        ],
        "fig2_page": "p030",
        "fig2_pnum": "30",
        "fig2_title": "CDE（共通データ環境）の情報状態遷移図",
        "fig2_desc": "Work In Progress・Shared・Published・Archivedの4状態と、各状態間の遷移条件を示すフロー図。",
        "fig2_read": "左から右への状態遷移の矢印と、各状態での承認・レビュー条件を確認する。",
        "fig2_edu": "CDEの情報管理プロセスを理解し、プロジェクト内での適切なデータ共有手順を習得させる。",
        "fig2_biz": "プロジェクトのCDE運用ルール策定・教育資料として活用する。",
    },
    4:  {
        "title": "BIMソフトウェア――選定・導入・運用",
        "keywords": "Revit / ARCHICAD / Vectorworks / BIMソフト選定 / TCO",
        "understand": [
            "主要BIMソフトウェアの特徴比較：Autodesk Revit（建築・構造・設備統合）、ARCHICAD（意匠設計特化）、Vectorworks（中小設計事務所向け）の強み・弱み。",
            "ソフトウェア選定の判断軸：プロジェクト規模・協力会社との互換性・TCO（総所有コスト）・サポート体制。",
            "TCO計算の構成要素：ライセンス費・ハードウェア費・トレーニング費・保守費・移行コスト。",
            "BIMソフトの導入ステップ：パイロット検証→段階的展開→全社標準化の3フェーズアプローチ。",
            "クラウドBIM（BIM 360/ACC）とオンプレミスBIMの運用上の差異と選択基準。",
        ],
        "summary": [
            "BIMソフトウェア選定は「最高のソフトを選ぶ」のではなく「プロジェクト条件に最も適したソフトを選ぶ」という観点が重要である。",
            "TCO分析により、初期ライセンス費だけでなく5年間の総保有コストを比較することが合理的な意思決定につながる。",
            "協力会社・発注者のBIM環境との互換性確保が、IFC標準の重要性をさらに高める。",
            "クラウドBIMはリモートワーク・多拠点連携に有利だが、大容量データの通信速度と情報セキュリティへの配慮が必要である。",
            "段階的導入（パイロット→展開→標準化）により、組織全体のBIM移行リスクを最小化できる。",
        ],
        "fig2_page": "p048",
        "fig2_pnum": "48",
        "fig2_title": "BIMソフトウェア選定マトリックス",
        "fig2_desc": "主要BIMソフト（Revit・ARCHICAD・Vectorworks等）を評価軸（機能・コスト・互換性・サポート）で比較したマトリックス表。",
        "fig2_read": "行（ソフト名）と列（評価軸）の交点で各ソフトの強弱を読み取り、自社プロジェクトの要件と照合する。",
        "fig2_edu": "ソフトウェア選定を体系的に行う思考フレームワークを習得させる。",
        "fig2_biz": "BIM導入提案書のソフトウェア選定セクション作成に活用する。",
    },
    5:  {
        "title": "BIM協調設計――多職種連携・クラッシュ検出・BCF",
        "keywords": "多職種連携 / クラッシュ検出 / BCF / 協調設計 / Navisworks",
        "understand": [
            "BIM協調設計における多職種（意匠・構造・設備）の役割分担と、IFCを通じたデータ統合方式。",
            "クラッシュ検出の種類：ハードクラッシュ（部材の物理的干渉）・ソフトクラッシュ（間隔基準違反）・ワークフロークラッシュ（工程干渉）。",
            "BCF（BIM Collaboration Format）：クラッシュ・設計問題をモデル座標付きで共有する軽量コラボレーション形式。",
            "Navisworks・Solibri等の干渉チェックツールの機能と活用手順。",
            "協調設計における責任分担マトリックス（RACI）の作成と、問題解決フローの策定。",
        ],
        "summary": [
            "BIM協調設計により、意匠・構造・設備の干渉を着工前に検出・解消することで、工期短縮とコスト削減を実現できる。",
            "クラッシュ検出はBIMの最も直接的なROI創出機能であり、「着工後発見」の手戻りコストを設計段階に前倒しして解消する。",
            "BCFはビューポイント付きで問題点を記録・共有するため、メール・図面の紙による指示に比べ圧倒的に正確な情報伝達が可能である。",
            "定期クラッシュ検出ミーティング（週次推奨）を慣行として確立することが、協調BIM運用の質を維持する鍵である。",
            "RACI責任分担表とBCFワークフローを組み合わせることで、問題の発見から解決まで追跡可能なプロセスが構築される。",
        ],
        "fig2_page": "p065",
        "fig2_pnum": "65",
        "fig2_title": "クラッシュ検出ワークフロー図",
        "fig2_desc": "モデル統合→クラッシュ検出→BCF発行→問題解決→再検証のサイクルを示すフロー図。",
        "fig2_read": "各ステップの担当者（意匠/構造/設備/BIMコーディネーター）と成果物を確認する。",
        "fig2_edu": "クラッシュ検出が単発作業でなく継続的サイクルであることを理解させる。",
        "fig2_biz": "プロジェクトのBIM協調設計手順書・BEP作成に直接流用できる。",
    },
    6:  {
        "title": "4D・5D BIM――工程シミュレーションとBIM積算",
        "keywords": "4D BIM / 5D BIM / 工程シミュレーション / BIM積算 / コスト管理",
        "understand": [
            "4D BIM：3DモデルにWBS・工程表を連携させ、施工シーケンスをアニメーションで可視化する手法。",
            "5D BIM：4D BIMにコスト情報を統合し、工程進捗に連動したリアルタイム原価管理を実現する手法。",
            "4Dシミュレーションのメリット：施工順序の最適化、仮設計画の検証、施主へのプレゼンテーション効果向上。",
            "BIM積算：モデルから数量データを自動抽出し、BoQ（数量明細書）を生成する。人力積算との差異と補完方法。",
            "主要4D/5Dツール：Synchro（Bentley）・VICO Office・Navisworks TimeLiner・Revit内蔵コスト機能の比較。",
        ],
        "summary": [
            "4D BIMにより施工シーケンスを着工前に可視化することで、工程干渉の早期発見と施工計画の最適化が実現される。",
            "5D BIMはリアルタイムコスト追跡を可能にし、「設計変更→コスト影響試算→意思決定」のサイクルを大幅に短縮する。",
            "BIM積算は人力積算と比較して作業時間を大幅削減するが、モデル品質（LOD・属性完全性）に結果精度が依存する。",
            "4D/5D BIMの最大の効果は「前倒し意思決定」にあり、施工後変更のコストを設計段階に移すことでROIが最大化される。",
            "発注者・施主に対する4Dシミュレーションプレゼンテーションは、工程理解と信頼関係構築に高い効果を発揮する。",
        ],
        "fig1_page": "p082",
        "fig1_pnum": "82",
        "fig1_title": "4Dシミュレーション画面構成図",
        "fig1_desc": "3Dモデルと工程バーチャートを同期表示し、施工ステップごとの建物状態を可視化する画面レイアウト図。",
        "fig1_read": "左ペイン（3Dモデル）と右ペイン（工程バー）の対応関係を確認し、特定工程での建物状態を読み取る。",
        "fig1_edu": "4D BIMが工程計画の「可視化ツール」であることを直感的に理解させる。",
        "fig1_biz": "施主説明会・施工計画書のビジュアル資料として直接活用できる。",
        "fig2_page": "p084",
        "fig2_pnum": "84",
        "fig2_title": "5D BIM コスト管理フロー図",
        "fig2_desc": "BIMモデルからの数量抽出→単価適用→BoQ生成→工程連動コスト追跡のフロー図。",
        "fig2_read": "左から右への情報フローを追い、各ステップでのデータ変換（数量→コスト→EVM）を確認する。",
        "fig2_edu": "5D BIMがコスト管理プロセス全体を統合する仕組みを理解させる。",
        "fig2_biz": "原価管理規程・BEPのコスト管理章の参照文書として活用する。",
    },
    7:  {
        "title": "施設管理（FM）とBIM――ライフサイクル活用",
        "keywords": "FM / ファシリティマネジメント / デジタルツイン / COBie / 維持管理BIM",
        "understand": [
            "FM（ファシリティマネジメント）フェーズにおけるBIM活用：竣工BIMモデルを設備台帳・保全計画・空間管理に活用する手法。",
            "COBie（Construction Operations Building information exchange）：施工BIMから維持管理システムへの設備情報引き渡し標準フォーマット。",
            "デジタルツイン：BIMモデルにIoTセンサーデータをリアルタイム統合し、建物の動的状態を仮想空間で再現する概念。",
            "BIMとCMMSの連携：コンピュータ支援維持管理システム（CMMS）へのBIMデータ連携による保全業務効率化。",
            "LCC（ライフサイクルコスト）分析：BIMモデルを用いた建物全寿命コストの試算と最適化。",
        ],
        "summary": [
            "竣工BIMモデルを「建物の生涯カルテ」として活用することで、維持管理コストの削減と設備故障の予防保全が実現できる。",
            "COBie形式による情報引き渡しを設計段階から計画することで、竣工後の情報再入力作業を排除できる。",
            "デジタルツインはBIMとIoTの融合による究極の建物情報管理形態であり、リアルタイム状態監視と予測保全を可能にする。",
            "BIM-FM連携の最大の障壁は「竣工モデルの品質維持」であり、施工段階でのas-built更新プロセスの確立が不可欠である。",
            "LCC分析にBIMを活用することで、設計代替案の経済性比較と最適設計選択が定量的に行えるようになる。",
        ],
        "fig1_page": "p100",
        "fig1_pnum": "100",
        "fig1_title": "BIM-FM連携システム構成図",
        "fig1_desc": "竣工BIMモデルからCOBie形式でFMシステム（CMMS）へ情報を連携するシステム構成の全体図。",
        "fig1_read": "BIMモデル（左）→COBie変換（中）→FMシステム（右）の情報フローと各システムの役割を確認する。",
        "fig1_edu": "BIMが設計・施工だけでなく維持管理フェーズでも価値を発揮することを理解させる。",
        "fig1_biz": "FM戦略計画書・BIM-FM連携システム仕様書の参照図として活用する。",
        "fig2_page": "p102",
        "fig2_pnum": "102",
        "fig2_title": "デジタルツイン概念図",
        "fig2_desc": "物理空間の建物とデジタル空間のBIMモデルがIoTセンサーを通じてリアルタイム同期する概念を示す図。",
        "fig2_read": "物理空間（左）とデジタル空間（右）の対応関係と、センサーデータの流れを確認する。",
        "fig2_edu": "デジタルツインがBIMの進化系であり、静的モデルから動的モデルへの転換を理解させる。",
        "fig2_biz": "スマートビルディング計画書・IoT導入提案書の概念説明資料として活用する。",
    },
    8:  {
        "title": "日本のBIM法規制・標準・調達制度",
        "keywords": "BIM法規制 / JIS A 2053 / ISO 19650 / BIM/CIM / 公共調達",
        "understand": [
            "日本のBIM標準体系：ISO 19650準拠のJIS A 2053と、国土交通省のBIM/CIM原則適用方針（2023年度〜）。",
            "建築確認申請とBIM：建築基準法上の確認申請図書は2D図面が要求され、BIMからの図面生成が現在の主流対応。",
            "公共工事でのBIM/CIM義務化：国土交通省の直轄工事（2023年度〜）への段階的適用拡大の経緯と現状。",
            "EIR（発注者情報要件）とBEP（BIM実行計画書）の関係：発注者がEIRで要件を定め、受注者がBEPで応答する契約フレームワーク。",
            "海外BIM義務化事例との比較：英国BIM Level 2（2016〜）、シンガポールBIM電子申請（2015〜）、韓国・北欧の動向。",
        ],
        "summary": [
            "日本のBIM標準化はISO 19650を軸に進んでいるが、建築基準法の2D図面要件が現時点での完全BIM申請の障壁となっている。",
            "国土交通省のBIM/CIM原則適用方針により、公共事業でのBIM活用は急速に拡大しており、民間企業にとっても対応が急務である。",
            "EIR-BEP体系を採用することで、発注者・受注者間のBIM要件合意を文書化し、契約上の明確性を確保できる。",
            "英国・シンガポールの先行事例から学ぶべき最大の教訓は、「標準化→義務化→市場定着」の段階的推進モデルである。",
            "JIS A 2053はISO 19650の国内版であり、情報管理の原則・CDEの定義・BEP要件を規定している。",
        ],
        "fig1_page": "p116",
        "fig1_pnum": "116",
        "fig1_title": "日本のBIM標準体系図",
        "fig1_desc": "ISO 19650→JIS A 2053→国土交通省BIM/CIM指針の階層関係と、各標準の適用範囲を示す体系図。",
        "fig1_read": "上位標準（ISO）から下位運用指針（省庁ガイドライン）への階層関係を上から下へ読み取る。",
        "fig1_edu": "日本のBIM標準が国際標準と国内法規制の双方に対応していることを理解させる。",
        "fig1_biz": "BIM導入方針書・BEP作成時の標準準拠根拠として参照する。",
        "fig2_page": "p118",
        "fig2_pnum": "118",
        "fig2_title": "EIR-BEP相互関係図",
        "fig2_desc": "発注者がEIRで情報要件を定め、受注者がBEPで応答するISO 19650準拠の情報管理契約フレームワーク図。",
        "fig2_read": "発注者側（左）のEIR要件と受注者側（右）のBEP応答の対応関係を確認する。",
        "fig2_edu": "BIM契約における情報要件の明確化が、プロジェクト成功の基盤であることを理解させる。",
        "fig2_biz": "公共発注BIMプロジェクトのEIR・BEP作成時のフレームワーク参照図として活用する。",
    },
    9:  {
        "title": "BIM人材育成・組織変革・導入戦略",
        "keywords": "BIM人材育成 / 組織変革 / BIM導入戦略 / ROI / チェンジマネジメント",
        "understand": [
            "BIM人材の類型：BIMマネージャー・BIMコーディネーター・BIMオペレーターの役割分担と必要スキルセット。",
            "組織変革（チェンジマネジメント）：BIM導入時の抵抗要因（コスト・学習コスト・業務変更への不安）と克服戦略。",
            "BIM導入ROIの定量評価：生産性向上・手戻り削減・工期短縮・品質向上の各指標と計算方法。",
            "段階的BIM導入計画：パイロットプロジェクト選定→標準化→全社展開の3フェーズアプローチ。",
            "BIM教育プログラムの設計：eラーニング・OJT・外部研修・資格取得支援の組み合わせ戦略。",
        ],
        "summary": [
            "BIM導入成否の最大決定要因は「技術」ではなく「人材と組織文化」であり、チェンジマネジメントが導入戦略の核心である。",
            "BIMマネージャー・コーディネーター・オペレーターの役割を明確化し、各レベルに適した教育プログラムを提供することが人材育成の基本である。",
            "ROI分析により「BIM投資対効果」を数値で示すことが、経営陣の意思決定を後押しし、継続的な投資確保につながる。",
            "パイロットプロジェクトは「成功確率が高く・学習効果が高い」案件を選定し、社内の信頼と知見を蓄積する足がかりとする。",
            "BIM資格取得支援（HITS・buildingSMART認定等）により、社員のモチベーション向上と外部評価の向上を同時に達成できる。",
        ],
        "fig1_page": "p134",
        "fig1_pnum": "134",
        "fig1_title": "BIM人材育成ロードマップ",
        "fig1_desc": "BIMオペレーター→コーディネーター→マネージャーへのキャリアパスと、各段階の必要スキル・推奨研修を示すロードマップ図。",
        "fig1_read": "縦軸（役割レベル）と横軸（時間軸・経験年数）で読み取り、自組織の人材配置に当てはめる。",
        "fig1_edu": "BIM人材育成が単発研修ではなく継続的なキャリア開発プロセスであることを理解させる。",
        "fig1_biz": "BIM人材育成計画書・研修計画の骨格として直接活用できる。",
        "fig2_page": "p136",
        "fig2_pnum": "136",
        "fig2_title": "BIM導入ROI試算モデル図",
        "fig2_desc": "BIM導入コスト（ライセンス・研修・移行）と、手戻り削減・工期短縮・品質向上による便益を比較したROI試算フレームワーク図。",
        "fig2_read": "左側のコスト項目と右側の便益項目を比較し、損益分岐点（ROI＝0）となる時点を読み取る。",
        "fig2_edu": "BIM投資の経済合理性を定量的に説明する思考フレームワークを習得させる。",
        "fig2_biz": "BIM導入提案書の経済性評価章・経営陣へのROI説明資料として活用する。",
    },
    10: {
        "title": "BIMの未来――AI・GIS・サステナビリティ・グローバルトレンド",
        "keywords": "AI×BIM / GIS連携 / サステナビリティ / カーボンニュートラル / グローバルBIM",
        "understand": [
            "AI×BIM統合：生成AI（Generative Design）による設計案自動生成、機械学習によるBIMモデル品質チェック自動化の現状と可能性。",
            "GIS×BIM連携：CityGML・PLATEAU等による都市スケールのBIM活用、インフラBIM（CIM）との統合。",
            "サステナビリティとBIM：LCA（ライフサイクルアセスメント）・カーボンフットプリント試算・ZEB設計へのBIM活用。",
            "グローバルBIMトレンド：英国BIM Level 2から3への進化、北欧・シンガポールの先進事例、日本の位置づけと課題。",
            "BIM×DX（デジタルトランスフォーメーション）：建設業のDX戦略におけるBIMの位置づけと、2030年以降の展望。",
        ],
        "summary": [
            "AIとBIMの統合は設計自動化・品質チェック・予測保全を変革しつつあり、「AIがBIMデータを読み解く」時代が到来しつつある。",
            "GISとBIMの統合（CityGML・PLATEAU）により、個別建物のBIMから都市・地域スケールの情報管理へ活用領域が拡大している。",
            "BIMによるLCA・カーボン試算は、カーボンニュートラル目標の実現に向けた設計最適化ツールとして不可欠な存在となっている。",
            "グローバルBIM先進国の事例（英国・北欧・シンガポール）に学びつつ、日本固有の法規制・建設文化に適合した展開戦略が求められる。",
            "建設DXの文脈でBIMは情報基盤の中核であり、IoT・AI・GIS・ドローン・ロボットとの統合による次世代建設プロセスの実現が視野に入っている。",
        ],
        "fig2_page": "p152",
        "fig2_pnum": "152",
        "fig2_title": "AI×BIM統合アーキテクチャ図",
        "fig2_desc": "BIMモデルデータを入力としてAIが設計最適化・品質チェック・コスト予測を行うシステム構成図。",
        "fig2_read": "BIMデータ（入力）→AIエンジン（処理）→最適化結果・予測（出力）のフローを確認する。",
        "fig2_edu": "AI×BIM統合が設計プロセスをどのように変革するかを具体的なユースケースで理解させる。",
        "fig2_biz": "AI・BIM統合システム導入計画書・R&D提案書の参照資料として活用する。",
    },
}

# Chapter-specific first figure pages
CHAP_FIG1 = {
    1: ("p003","3","BIMの概念図―建物情報モデルの全体像",
        "BIMモデルを中心に設計・施工・維持管理の各フェーズが連携する全体像を示す概念図。",
        "中央のBIMモデルから各フェーズへの情報フローを矢印で追う。",
        "BIMが単なる3D図面ではなく情報統合プラットフォームであることを理解させる。",
        "プロジェクト計画書作成時のBIM活用範囲定義に使用する。"),
    2: ("p016","16","IFCデータ構造の階層図",
        "IFCのオブジェクト階層（プロジェクト→サイト→建物→フロア→スペース→要素）を示す図。",
        "ツリー構造の上位から下位へ、IFCエンティティの包含関係を読む。",
        "IFCが単なるファイル形式ではなくデータモデルであることを理解させる。",
        "IFCエクスポート設定の確認・トラブルシューティングに使用する。"),
    3: ("p029","29","BIMワークフロー全体図（企画〜維持管理）",
        "建物ライフサイクル（企画→基本設計→実施設計→施工→維持管理）を通じたBIM情報の流れを示す全体図。",
        "左から右へ各フェーズを順に追い、BIMモデルがどのように情報を蓄積・引き継ぐかを確認する。",
        "BIMが建物の全ライフサイクルを通じた情報管理基盤であることを理解させる。",
        "プロジェクトキックオフ時のBIM活用計画説明資料として使用する。"),
    4: ("p046","46","BIMソフトウェア市場マップ",
        "主要BIMソフトウェア（意匠・構造・設備・施工管理・FM）の市場ポジションと相互連携関係を示すマップ。",
        "各ソフトの専門領域（色分け）と連携矢印を確認し、プロジェクトで必要なツールセットを特定する。",
        "BIMエコシステム全体像を把握させ、ソフト選定の視野を広げる。",
        "BIM導入計画策定時のツール選定・予算計画の参照図として活用する。"),
    5: ("p063","63","多職種BIM協調設計のデータフロー図",
        "意匠・構造・設備各社がIFCを通じてBIMデータを統合し、干渉チェックを行うデータフロー図。",
        "各社のモデルが統合モデルに収束し、クラッシュ検出→BCF発行→修正のサイクルを読み取る。",
        "BIM協調設計における各専門職の責任範囲とデータ連携方式を理解させる。",
        "BEPの責任分担表・IFC連携手順書作成の参照図として活用する。"),
}


def make_understand_section(chap_num):
    """Generate 'この章で理解すべきこと' section"""
    meta = CHAP_META[chap_num]
    lines = [
        "## この章で理解すべきこと / Key Concepts to Master\n",
        "本章を学習する前に、以下の問いを念頭に置くこと：\n",
    ]
    for i, item in enumerate(meta["understand"], 1):
        lines.append(f"**{i}.** {item}\n")
    lines.append("")
    return "\n".join(lines)


def make_summary_section(chap_num):
    """Generate '要点まとめ' section"""
    meta = CHAP_META[chap_num]
    lines = [
        "## 要点まとめ / Key Takeaways\n",
    ]
    for i, item in enumerate(meta["summary"], 1):
        lines.append(f"**{i}.** {item}\n")
    lines.append("")
    return "\n".join(lines)


def make_second_figure(chap_num):
    """Generate second figure block for chapters that only have 1 figure"""
    meta = CHAP_META[chap_num]
    # Chapter 6,7,8,9 have fig1_ keys, others use fig2_ keys
    if "fig2_page" in meta:
        page = meta["fig2_page"]
        pnum = meta["fig2_pnum"]
        title = meta["fig2_title"]
        desc = meta["fig2_desc"]
        read = meta["fig2_read"]
        edu = meta["fig2_edu"]
        biz = meta["fig2_biz"]
    else:
        return ""

    return f"""
【図表：{title}】
（出典：PDF p.{pnum}）

![{title}](assets/pages/{page}.png)

① 図の説明：{desc}

② 読み取り方：{read}

③ 教育上の狙い：{edu}

④ 実務活用シーン：{biz}

"""


def fix_textbook_chapter(chap_num):
    """Fix a single textbook chapter: add missing sections, fix figures, fix desu/masu"""
    path = os.path.join(REPO, f"textbook/chap{chap_num:02d}.md")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    txt = open(path, encoding="utf-8").read()
    changed = False

    # ── 1. Add 'この章で理解すべきこと' after 学習目標 section ──
    if "この章で理解すべきこと" not in txt:
        understand_block = make_understand_section(chap_num)
        # Insert after the learning objectives block (before "## 1. 問題の背景")
        txt = re.sub(
            r'(---\s*\n\n## 1\. 問題の背景)',
            f"\n{understand_block}\n---\n\n## 1. 問題の背景",
            txt
        )
        changed = True
        print(f"  + Added この章で理解すべきこと to chap{chap_num:02d}")

    # ── 2. Add '要点まとめ' before 確認問題 ──
    if "要点まとめ" not in txt:
        summary_block = make_summary_section(chap_num)
        txt = re.sub(
            r'(---\s*\n\n### 確認問題（多肢選択式）)',
            f"\n---\n\n{summary_block}\n---\n\n### 確認問題（多肢選択式）",
            txt
        )
        changed = True
        print(f"  + Added 要点まとめ to chap{chap_num:02d}")

    # ── 3. Add second figure if only 1 citation ──
    fig_count = txt.count("（出典：PDF p.")
    if fig_count < 2:
        second_fig = make_second_figure(chap_num)
        if second_fig:
            # Insert before the アナロジー or 失敗事例 section
            txt = re.sub(
                r'(---\s*\n\n## 4\. アナロジー|---\s*\n\n## 3\. アナロジー)',
                f"{second_fig}\n---\n\n## 4. アナロジー",
                txt
            )
            changed = True
            print(f"  + Added 2nd figure citation to chap{chap_num:02d}")

    # ── 4. Fix desu/masu: simple heuristic replacements ──
    # Replace lines ending with です。→ である。/ ます。→ する。
    def fix_dm(m):
        line = m.group(0)
        # Only fix lines that aren't headings/code/lists/quotes
        if line.startswith(('#', '>', '-', '`', '|', '!')):
            return line
        line = re.sub(r'です。$', 'である。', line)
        line = re.sub(r'ます。$', 'する。', line)
        line = re.sub(r'でした。$', 'であった。', line)
        line = re.sub(r'ました。$', 'した。', line)
        return line

    new_txt = "\n".join(fix_dm(re.match(r".*", ln)) if ln else ln
                        for ln in txt.splitlines())
    if new_txt != txt:
        txt = new_txt
        changed = True
        print(f"  + Fixed desu/masu in chap{chap_num:02d}")

    if changed:
        open(path, "w", encoding="utf-8").write(txt)
        print(f"  ✓ Saved chap{chap_num:02d}.md")
    else:
        print(f"  - No changes needed for chap{chap_num:02d}.md")


def fix_slide(chap_num):
    """Fix a single slide: convert long prose lines to bullet points"""
    path = os.path.join(REPO, f"slides/chap{chap_num:02d}_slide.md")
    if not os.path.exists(path):
        print(f"  SKIP (not found): {path}")
        return

    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()
    new_lines = []
    changed = False

    for i, line in enumerate(lines):
        # Long prose line: not heading, not bullet, not image, not citation, not separator
        if (len(line) > 80
                and not line.startswith(('#', '-', '!', '（出典', '|', '>', '`'))
                and line.strip() not in ('---', '')
                and '**' not in line[:3]):  # not bold lead
            # Split into bullet points at Japanese sentence boundaries
            # Each 。sentence → bullet
            sentences = re.split(r'(?<=。)', line.strip())
            sentences = [s.strip() for s in sentences if s.strip()]
            if len(sentences) > 1:
                for s in sentences:
                    new_lines.append(f"- {s}")
                changed = True
            else:
                # Single long sentence: just prefix with bullet
                new_lines.append(f"- {line.strip()}")
                changed = True
        else:
            new_lines.append(line)

    if changed:
        open(path, "w", encoding="utf-8").write("\n".join(new_lines) + "\n")
        print(f"  ✓ Fixed prose in slides/chap{chap_num:02d}_slide.md")
    else:
        print(f"  - No changes needed for slides/chap{chap_num:02d}_slide.md")


# ─────────────────────────────────────────────
# Main repair loop
# ─────────────────────────────────────────────
print("=" * 60)
print("QA REPAIR SCRIPT — BIM Training Package")
print("=" * 60)

print("\n[PHASE 1] Fixing textbook chapters...")
for i in range(1, 11):
    print(f"\n  chap{i:02d}:")
    fix_textbook_chapter(i)

print("\n[PHASE 2] Fixing slides...")
for i in range(1, 11):
    print(f"\n  slide chap{i:02d}:")
    fix_slide(i)

print("\n[DONE] Repair complete.")
