import os
import sys
from bidict import bidict

card_version_dict = bidict({"0xFFFF": "4", "0x5210": "5", "0x6013": "6 AA", "0x7012": "7 AAX", "0x8015": "8 Infinity"})
prefectures = ["北海道", "青森県", "岩手県", "宮城県", "福島県", "山形県", "秋田県", "茨城県", "栃木県", "群馬県", "千葉県", "埼玉県", "東京都", "神奈川県", "山梨県", "新潟県", "長野県", "富山県", "石川県", "愛知県", "静岡県", "岐阜県", "三重県", "福井県", "大阪府", "京都府", "奈良県", "滋賀県", "和歌山県", "兵庫県", "広島県", "鳥取県", "島根県", "岡山県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県", "中国/上海 CHN", "香港 HKG", "韓国 SKR", "マレーシア MYS", "シンガポール SGP", "台湾 TWN", "インドネシア IDN", "フィリピン PHL", "タイ THAI", "アメリカ合衆国 USA"]
avatar_gender_list = ["Male", "Female"]
bgm_volume_list = ["Low", "Normal", "High"]
make_list = ["Toyota", "Nissan", "Honda", "Mazda", "Subaru", "Mitsubishi", "Suzuki", "Initial D", "Complete"]
model_dict = {"Toyota": ["TRUENO GT-APEX (AE86)", "LEVIN GT-APEX (AE86)", "LEVIN SR (AE85)", "86 GT (ZN6)", "MR2 G-Limited (SW20)", "MR-S (ZZW30)", "ALTEZZA RS200 (SXE10)", "SUPRA RZ (JZA80)", "PRIUS (ZVW30)", "SPRINTER TRUENO 2door GT-APEX (AE86)", "CELICA GT-FOUR (ST205)"],
                   "Nissan": ["SKYLINE GT-R (BNR32)", "SKYLINE GT-R (BNR34)", "SILVIA K's (S13)", "Silvia Q's (S14)", "Silvia spec-R (S15)", "180SX TYPE II (RPS13)", "FAIRLADY Z (Z33)", "GT-R NISMO (R35)", "GT-R (R35)", "SKYLINE 25GT TURBO (ER34)"],
                   "Honda": ["Civic SiR・II (EG6)", "CIVIC TYPE R (EK9)", "INTEGRA TYPE R (DC2)", "S2000 (AP1)", "NSX (NA1)"],
                   "Mazda": ["RX-7 ∞III (FC3S)", "RX-7 Type R (FD3S)", "RX-7 Type RS (FD3S)", "RX-8 Type S (SE3P)", "ROADSTER (NA6CE)", "ROADSTER RS (NB8C)"],
                   "Subaru": ["IMPREZA STi Ver.V (GC8)", "IMPREZA STi (GDBA)", "IMPREZA STI (GDBF)", "BRZ S (ZC6)"],
                   "Mitsubishi": ["LANCER Evolution III (CE9A)", "LANCER EVOLUTION IV (CN9A)", "LANCER Evolution VII (CT9A)", "LANCER Evolution IX (CT9A)", "LANCER EVOLUTION X (CZ4A)", "LANCER GSR EVOLUTION VI T.M.EDITION (CP9A)", "LANCER RS EVOLUTION V (CP9A)"],
                   "Suzuki": ["Cappuccino (EA11R)"],
                   "Initial D": ["SILEIGHTY", "TRUENO 2door GT-APEX (AE86)"],
                   "Complete": ["G-FORCE SUPRA (JZA80-kai)", "MONSTER CIVIC R (EK9)", "NSX-R GT (NA2)", "RE Amemiya Genki-7 (FD3S)", "S2000 GT1 (AP1)", "ROADSTER C-SPEC (NA8C Kai)"]}
car_prefectures = ["札幌", "函館", "旭川", "室蘭", "釧路", "帯広", "北見", "青森", "八戸", "岩手", "宮城", "仙台", "福島", "いわき", "会津", "山形", "庄内", "秋田", "水戸", "土浦", "つくば", "栃木", "宇都宮", "とちぎ", "那須", "群馬", "高崎", "千葉", "野田", "習志野", "袖ヶ浦", "成田", "柏", "大宮", "熊谷", "春日部", "所沢", "川越", "品川", "足立", "練馬", "多摩", "八王子", "横浜", "川崎", "相模", "湘南", "山梨", "新潟", "長岡", "長野", "松本", "諏訪", "富山", "石川", "金沢", "名古屋", "三河", "尾張小牧", "豊橋", "豊田", "岡崎", "一宮", "静岡", "沼津", "浜松", "伊豆", "岐阜", "飛騨", "三重", "鈴鹿", "福井", "大阪", "なにわ", "和泉", "堺", "京都", "奈良", "滋賀", "和歌山", "神戸", "姫路", "広島", "福山", "鳥取", "島根", "岡山", "倉敷", "山口", "下関", "徳島", "香川", "愛媛", "高知", "福岡", "北九州", "筑豊", "久留米", "佐賀", "長崎", "佐世保", "熊本", "大分", "宮崎", "鹿児島", "沖縄", "富士山"]
car_hirigana = ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と", "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ", "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り", "る", "れ", "ろ", "わ", "を", "ん", "が", "ぎ", "ぐ", "げ", "ご", "ざ", "じ", "ず", "ぜ", "ぞ", "だ", "ぢ", "づ", "で", "ど", "ば", "び", "ぶ", "べ", "ぼ", "ぱ", "ぴ", "ぷ", "ぺ", "ぽ", "さ"]
courses = ["Lake Akina (CCW)", "Lake Akina (CW)", "Myogi (DH)", "Myogi (UH)", "Akagi (DH)", "Akagi (UH)", "Akina (DH)", "Akina (UH)", "Irohazaka (DH)", "Irohazaka (UH)", "Tsukuba (DH)", "Tsukuba (UH)", "Happogahara (OB)", "Happogahara (IB)", "Nagao (DH)", "Nagao (UH)", "Tsubaki Line (DH)", "Tsubaki Line (UH)", "Nanagamari (DH)", "Nanagamari (UH)", "Sadamine (DH)", "Sadamine (UH)", "Tsuchisaka (OB)", "Tsuchisaka (IB)", "Akina Snow (DH)", "Akina Snow (UH)", "Hakone (DH)", "Hakone (UH)", "Momiji Line (DH)", "Momiji Line (UH)", "Usui (CCW)", "Usui (CW)"]
cup_list = ["None", "Paper Cup", "Orange Juice", "Tea Cup"]
tachometer_list = ["Infinity", "Formula", "Future", "Double X Cross", "InitialD5", "InitialD Ver. 3", "Classic", "Sidebar", "Single", "Wide"]
aura_list = ["None", "Scorching Hot", "Whirlwind", "Lightning", "Evil Spirit", "Overlord", "Wings"]
class_list = ["E3", "E2", "E1", "D3", "D2", "D1", "C3", "C2", "C1", "B3", "B2", "B1", "A3", "A2", "A1", "S3", "S2", "S1", "SS3", "SS2", "SS1", "Infinity"]
title_list = ["世界最速左周（湖）", "世界最速左周（碓）", "世界最速のダウンヒラー（妙）", "世界最速のダウンヒラー（赤）", "世界最速のダウンヒラー（秋）", "世界最速のダウンヒラー（い）", "世界最速のダウンヒラー（箱）", "世界最速のダウンヒラー（筑）", "世界最速のダウンヒラー（定）", "世界最速のダウンヒラー（土）", "世界最速のダウンヒラー（も）", "世界最速のダウンヒラー（八）", "世界最速のダウンヒラー（七）", "世界最速のダウンヒラー（长）", "世界最速のダウンヒラー（椿）", "世界最速のダウンヒラー（雪）", "世界最速右周（湖）", "世界最速右周（碓）", "世界最速のヒルクライマー（妙）", "世界最速のヒルクライマー（赤）", "世界最速のヒルクライマー（秋）", "世界最速のヒルクライマー（い）", "世界最速のヒルクライマー（箱）", "世界最速のヒルクライマー（筑）", "世界最速のヒルクライマー（定）", "世界最速のヒルクライマー（土）", "世界最速のヒルクライマー（も）", "世界最速のヒルクライマー（八）", "世界最速のヒルクライマー（七）", "世界最速のヒルクライマー（长）", "世界最速のヒルクライマー（椿）", "世界最速のヒルクライマー（雪）", "頭文字D7やってました", "経験高い走り屋", "熟练の走り屋", "精炼の走り屋", "超练の走り屋", "神练の走り屋", "疾风迅雷", "ブルジョワジー", "巨万の富を蓄えし者", "威风堂々", "ACE KILLER", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "走り屋デビュー", "コーナー3コで失神事件", "秋名山最速", "荷重移動の極み", "関八州に挑む", "めいっぱいヤバイモード", "雨は別に苦手じゃないし", "ＴＡパフォーマー", "孤高のスピリッツ", "オキテ破りの地元走り", "全国区になぐりこみだあ！！", "気まぐれなジョーカー", "サヨナラの儀式", "無敵の戦闘機", "モチベーションの勝負", "とっぽい走り屋", "ワンハンドステア", "ドリフトぐらい朝めし前", "しりふりダンス", "唯一無二の存在", "無（ゼロ）の心", "超天然素材", "峠の職人", "白銀を制する者", "不敗神話のR", "峠のキング", "いろは坂の皇帝（エンペラー）", "400馬力のターボパワー", "東堂塾の精神", "ブラインドアタック", "公道世界一のクルマ ", "峠の神様", "正確無比なコントロール", "驚愕の速度域", "スプリントのプロ", "超常現象のような奇跡", "かおり", "秋名の亡霊", "空翔ける天馬", "全国対戦デビュー", "新進気鋭", "バトル巧者", "バトルプロフェッショナル", "ストリートのカリスマ", "戦神", "不敗神話", "サクッと3連勝！", "10連勝王", "奇蹟の50連勝", "伝説の100連勝", "ホーム負けなし", "好敵手", "チャレンジャー", "友と共に頂へ", "宿命のライバル", "未体験ゾーン", "今までで最高のノリ", "神経すり減らしたアタック", "壮絶　赤城おろし！！", "伝説のスーパーテクニシャン", "地元スペシャルのラインどり", "ギリギリの領域", "ナチュラルな瞬発力", "天啓のようなひらめき", "必殺多角形ブレーキング！！", "フタのない側溝の攻略法", "奇想天外な忍者戦法", "想像を絶するパフォーマンス", "奇跡のハイペース", "珠玉の芸術", "上州名物カラッ風", "タイムアタックマニア", "究極の完成形", "神の領域", "俺にも友はいる", "友達が多い走り屋", "顔が広い走り屋", "仲間の集う走り屋", "永遠の絆", "全国タッグ対戦デビュー", "切札(エース)は俺だ", "双璧の竜", "盟友と連ねる勝利", "良きタッグ", "同調(シンクロ)するタッグ", "共鳴しあう走り屋魂", "究極のダブルエース", "伝説の関東最速タッグ", "頭文字D8インフィニティ", "新車シェイクダウン", "長距離ドライバー", "東京大阪間走った", "ザ・サウザンド", "日本縦断", "アメリカ往復！？", "地球一周旅行", "秋名の走り屋", "いろは坂の走り屋", "もみじラインの走り屋", "碓冰の走り屋", "七曲の走り屋", "秋名（雪）の走り屋", "秋名湖の走り屋", "赤城の走り屋", "筑波の走り屋", "长尾の走り屋", "椿线の走り屋", "定峰の走り屋", "土坂の走り屋", "箱根の走り屋", "八方原の走り屋", "秒义の走り屋", "秋名の达人", "いろは坂の达人", "もみじラインの达人", "碓冰の达人", "七曲の达人", "秋名（雪）の达人", "秋名湖の达人", "赤城の达人", "筑波の达人", "长尾の达人", "椿线の达人", "定峰の达人", "土坂の达人", "箱根の达人", "八方原の达人", "秒义の达人", "秋名のスペシャリスト", "いろは坂のスペシャリスト", "もみじラインのスペシャリスト", "碓冰のスペシャリスト", "七曲のスペシャリスト", "秋名（雪）のスペシャリスト", "秋名湖のスペシャリスト", "赤城のスペシャリスト", "筑波のスペシャリスト", "长尾のスペシャリスト", "椿线のスペシャリスト", "定峰のスペシャリスト", "土坂のスペシャリスト", "箱根のスペシャリスト", "八方原のスペシャリスト", "秒义のスペシャリスト", "秋名の生ける传说", "いろは坂の生ける传说", "もみじラインの生ける传说", "碓冰の生ける传说", "七曲の生ける传说", "秋名（雪）の生ける传说", "秋名湖の生ける传说", "赤城の生ける传说", "筑波の生ける传说", "长尾の生ける传说", "椿线の生ける传说", "定峰の生ける传说", "土坂の生ける传说", "箱根の生ける传说", "八方原の生ける传说", "秒义の生ける传说", "峠の生ける传说", "ガレージフルコンプリート", "自慢の愛車", "限界突破！", "EX FULL SPEC マニア", "EX FULL SPEC 職人", "類稀なるメカニック", "至高のマシンチューナー", "ハチロクマイスター", "GT-Rマイスター", "インプレッサマイスター", "ランエボマイスター", "4WDマイスター", "FFマイスター", "MRマイスター", "FRマイスター", "ロータリーマイスター", "めくるめく高回転の戦慄き", "志ありて凛しく艶ありて昴むる", "スリーダイヤの槍騎兵", "雄々 しく気高き太陽と雲一文字", "地上にきらめく六連星", "交錯する円環の理に導かれし者", "山椒は小粒でもぴりりと辛い", "異形の使い魔", "TA最速の走り屋チーム", "VS最強の走り屋チーム", "Top of Top", "チーム最速のアタッカー", "人德を示す者", "カリスマに集う走り屋たち", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "銀河最速の座を得しもの", "地上最速の座を得しもの", "目に映らめ領域のもの", "車と峠に愛されしもの", "神速の走り屋", "光速の走り屋", "音速の走り屋", "峠に愛された走り屋", "ACE DRIVER", "明鏡止水", "イニDクイズ正解者", "カリスマプロデューサー", "東堂塾塾生", "ドリフトキング", "頭文字Dファン", "みんなのアニキ", "鬼教官", "伝説の峠職人", "地球最速の座を得しもの", "極速之王", "紫電一閃", "破竹之勢", "Dの遺伝子の継承者", "SEGAスピードスターズ", "獅子奮迅", "Dの願いをかなえし者", "虚空に轟く天雷", "暗晦を駆ける流星", "最速伝说の创造神", "宵闇を翔ける闪光", "峠に舞い戾る不死鸟", "最速と謳われしもの", "超速制御の贵公子", "限界知らずの走り屋根性", "最速伝说を紡ぐ者", "赫奕たる零の领域", "走り屋魂の煌めき", "燦然と辉く峠の王者", "禁断の速度を解き放て", "峠の最终兵器", "全ての峠を統べし皇", "天地に瞬間を刻む者", "永久不滅の疾風", "天下無双", "眠れる獅子", "一陣の風", "真·天下最速", "疾风する猛き咆哮", "无限の可能性", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "10段階アクセルマワーク", "1セク魔神", "1ミリでも低い車高", "2セク将軍", "2日に3回振られる", "2本目は不要", "２枚看板", "２輪上がり", "３セク軍師", "４ＷＤコンプレックス", "４セク帝王", "AT限定免许", "ＣＯＭＰＬＥＴＥ愛", "ＤＲＥＡＭ（夢）", "Ｉ　ＬＯＶＥ　ＣＡＲ．", "Ｉ　ＬＯＶＥ　頭文字Ｄ", "ＩＣＥ　ＦＩＥＬＤＥＲ", "Ｍｒ．ドアンダー", "ＭＴテクニシャン", "Ｓ高のスーパー男子高生", "アイデンティティ重視", "アウト・オブ・眼中", "アクセルワークの達人", "アクセル全開！", "アスファルトダンサー", "アドバンテージを覆せし者", "アドレナリン発生装置", "あの人に負けたくない", "アブソリュート・ゼロ", "アフターファイヤー", "アマチュア", "アルティメットドライバー", "アンダーをだしてしまう", "あんたが大将！", "いい角度でスピンするウデ", "イエスマン", "イカサマ師", "いつだって真剣（マジ）！", "いぶし銀", "いろは坂のゴロツキ", "いろは坂のサル", "インベタのさらにイ", "インポジション", "ウワサのドリフトドライバー", "エースに次ぐもの", "エース格のドライバー", "エキサイト", "エクスタシー", "えげつないライン", "エコモード", "エコロジスト", "エターナルドライバー", "エボに死角なし", "エンジン全開！", "エンターテイナー", "オートマを極めし者", "オーバースピード", "オーバーテイカー", "オールマイティ", "おてんば", "オレのこだわりの美学", "オレの獲物", "お先に失礼！", "お前の友達の友達は‥", "カーイズマイライフ", "カウンターアタック", "カスタマイザー", "ガチンコの走り屋集団", "ガチンコモード", "ガチンコ上等！", "かっとびヒルクライム", "カミカゼダウンヒラー", "ガムテープデスマッチ", "カリスマ", "ガンコじじい", "キケンゾーン", "キタキター！", "ギャラクシー", "キングオブキング", "キュルルルル！！", "キンコン♪キンコン♪", "ゴァアアアア！", "ドッギャアァアア！！！", "パン！パン！", "ブォォォン！", "プシャァァァ！！", "プン！", "クランクは得意", "クリーンな対戦相手", "クリエーター", "クルマと峠を愛するもの", "クルマニア", "クルマ酔い", "クレバーな公道ランナー", "ゲームセンター通い", "コーナー２つで消える", "コーナリングパフォーマンス", "こだわり派", "ゴッドアーム", "ゴッドフット", "ザ・一匹狼", "サーキット上がり", "サービス精神", "サンデードライバー", "シートの神様", "シュッとしてる", "シロウト集団", "シンプルイズベスト", "スーパーテクニック", "スーパーハイペース", "スキール音は悪魔の戦慄き", "スキがない走り", "スゴウデ", "スターライトダンサー", "スタイリッシュ", "ステアリングの達人", "ステアリングの魔術師", "ストリートスペシャリスト", "ストリートドライバー", "ストレートが速い", "スピードキング", "スピードの世界に生きるもの", "スプリントの真髄", "すべて不明（じゃ書くなよ）", "スポーツシビック", "スレちがいの恋", "スロースターター", "セオリー無視", "セミプロ級のテクニシャン", "ゼロカウンタードリフト", "ゼロ理論の拡大解釈", "ゼロ理論の体現者", "そうだ、峠へ行こう！", "ゾッとするほどデンジャラス", "ターボ使いの彼", "ダーリンは天才", "ダイエット中", "ダイナミック", "ダイナミックな急坂下り", "タイヤマネージメントの達人", "ダウンヒルアタッカー", "ダウンヒルスペシャリスト", "タクシー代わり", "ただのギャラリー", "タフガイ", "ダブルエース", "ダントツのカリスマ", "チーフドライバー", "チーフメカニック", "チームの中で３番目くらい", "チャリで来た", "チャレンジ精神", "チューニング", "ちょっとおきゃんな", "ちょっとおしゃまな", "ツボにはまると速い", "ディープダウンヒル", "データ収集家", "テール・トゥ・ノーズ", "テールスライド", "テクニシャン", "デスマッチスペシャリスト", "テンションマックス", "テンション全開モード", "テンション臨界点", "ドッカンターボ", "ドッグファイター", "ドッグファイト", "トップオブストリート", "トップランナー", "とてもはやい", "トラブルメーカー", "トリックスター", "ドリフトアーティスト", "ドリフトクイーン", "ドリフトのまねごとはできる", "ドリフトの化身", "ドリフトの華", "ドリフトの権化", "ドリフトの神", "ドリフトの名人", "ドリフト家", "ドリフト狂", "ドリフト先輩", "ドリフト番長", "ドリフト部長", "トンネル愛好者", "トンビに油揚げ", "ド新人", "ド迫力", "ド根性！！", "ナチュラリスト", "なんだか色っぽい‥", "ニュータイプの走り屋", "ネット上では伝説のチーム", "ノーチャンス", "ノーブーストウィン", "ノーフューチャー", "ノーブレーキ走法", "パートナーシップ", "ハードブレーキング", "ハートを振りまく彼氏", "ハートを振りまく彼女", "パーフェクトウィン！！", "パープルシャドウの重鎮", "ハイアベレージ走行", "ハイオク満タンで！", "ハイスピードジャンキー", "バカッ速", "バスで来た", "車で来た！", "歩いて来た", "ハチ‥ロク？", "バックが苦手", "バックミラーは用無しだ！", "パッションの塊", "ハッピーボーイ", "パネルストライカー", "パネルブレイカー", "パフォーマー", "バラ色のパラダイス", "はりきりボーイ", "バレンタイン", "パワー命", "ヒール・アンド・トウ", "ヒーロー", "ファーストコンタクト", "ファンキー野郎", "ファンタジスタ", "ファンタズムドライバー", "フィーバー", "フェアプレイヤー", "ぶっちぎりチャンプ", "ぶっちゃけ始めたばかり", "ブラインド走行", "フルスロットル", "プレイボーイ", "ブレーキングの達人", "プレッシャーに弱くキレやすい", "プレッシャーメーカー", "プロゲーマー", "プロジェクトＤの追っかけ", "プロフェッショナル", "プロよりもプロっぽい", "プロレーサー", "ペースメーカー", "ペーパードライバー", "ベタ踏み大好き", "ベテラン", "ホームコースの秋名", "ポジショニング重視", "ま‥負けてなどいない！", "マーシャル役", "まさに野獣", "まずは格好から", "マニュアルを極めし者", "ミゾ落とし研究家", "ミッドナイトランナー", "ミラクルシビック", "ミラクルダウンヒラー", "ミラクルボーイ", "めちゃくちゃはやい", "もうスペースがない", "モラリスト", "やとわれ参謀", "ラーメン大好き", "ラッキーマン", "ラリースト", "ランエボキラー", "ランエボマスター", "ランエボ最強", "リベンジ宣言", "レイトブレーキング", "レインバトルのプロ", "レーシングドライバー", "レース経験者", "レコードホルダー", "レッドサンズの一軍", "レッドフラッグ", "ロータリー・ブラザース", "ロータリーロケット", "ローリングナイス", "ロケットスターター", "ロンリーウルフ", "ロンリードライバー", "ワインディングマジシャン", "わが名は‥", "ワルそうな奴は大体友達", "愛車", "悪夢のジョーカー", "悪夢のマシン", "圧倒的な力にひれ伏せ！", "安全運転", "暗黙のルールを破る", "闇を切り裂く", "偉大なドリフトアーティスト", "意地のはりあい", "異邦人", "一生に一度のチャンス", "一切の妥協なし", "一万一千回転までキッチリ回せ", "雨のダウンヒル", "碓氷の跳ね馬", "碓氷の天使", "噂の走り屋", "運転がうまい", "雲の上の存在", "栄光のゴール", "栄誉ある走り", "永遠の二番手", "遠征組", "王者の風格", "俺だって勝ちたいんだよ！", "俺の掟", "俺は持っている！！", "俺は生きている！！", "俺は盛っている！！", "俺より強いヤツはもういる", "下りスペシャリスト", "何キロ出てんだーっ", "果報者", "火の玉バトル", "火の玉ボーイ", "荷重移動の芸術家", "華麗なるドリフト", "餓狼", "怪速の男", "外（アウト）がガラ空きだ", "外連味のない走り", "崖っぷち", "街が眠る時‥俺達は走る！", "覚醒", "楽しさ第一主義", "活殺自在", "完璧主義者", "感覚派", "間一髪", "顔を洗うのと同じ日常", "危険な香り", "奇跡のショータイム", "嬉しい誤算", "気持ちはいつでも３連勝", "起死回生の心理戦", "鬼のようなコーナリング", "鬼軍曹", "究極のとうふ屋ドリフト", "教官", "狂気のドライバー", "狂乱のダウンヒラー", "響くエキゾーストノート", "驚異のペース管理", "暁を駆ける狼", "極めし者", "極限のドライバー", "極限バトル", "玉砕上等", "空中に描くライン", "経験豊富", "軽自動車愛好家", "激走", "激速プンプン丸", "激動たるドライバー", "元ラリースト", "幻惑のドライバー", "現役のレーサー", "現役最強", "現役走り屋", "限界ギリギリブレーキング", "限界という名のグレーゾーン", "限界を超えた挑戦", "限界領域", "孤高のレーサー", "孤高の走り屋", "孤高の天才", "孤独なハート", "孤独なランナー", "己を超えし者", "湖のほとりを愛する者", "虎視眈々", "公道キング", "公道のカリスマ", "公道のスペシャリスト", "公道の策士", "公道の神様", "公道の幽霊", "公道マイスター", "幸せのテンションの絶頂", "荒っぽいスタイル", "香織さんの禅問答", "高いコンセントレーション", "高級嗜好", "高橋兄弟並み", "高速コーナーが得意", "剛腕", "轟くロータリーサウンド", "今‥一番抱かれたい走り屋", "混乱と孤独", "最も警戒すべき男", "最強のコーナリングマシン", "最強のライバル", "最強の敵", "最強の壁", "最強軍団", "最狂のクレイジーダウンヒル", "最後の砦", "最後まで諦めない！", "最高のライバル", "最高のお友達", "最高だぜッ！！", "最速コンビネーション", "最速王", "埼玉のゴロツキ", "策士策に溺れる", "山嵐", "残像しか見えない！", "仕事帰り", "四次元パフォーマー", "子供の心と大人の財力", "止めたくても止まらない", "死ぬ気かァ！？", "死んだ走り屋の幽霊", "死神", "糸の切れた凧", "至高のドリフトアーティスト", "至高のプライド", "試行錯誤", "次元を超えた走り", "自己主張の激しい人", "自称エキスパート", "自称最強", "自称最速", "失恋", "疾走する真紅", "実力ナンバーワン", "社長のキモいり", "車と対話するもの", "車は中身で勝負！", "若き獅子", "若き天才ダウンヒラー", "若さゆえの狂気", "若葉マーク", "弱点のない車", "珠玉の名機", "首領", "秋名が生んだ怪物", "秋名のゴロツキ", "秋名の仲間", "集中力が切れた‥", "重ねた想い", "宿命のライバル", "出会いそして別れ", "純粋なスピリット", "純粋なる走り屋", "順風満帆", "初っ端から全開", "初心者", "諸刃の剣", "女でも男には負けねーよ！", "勝算２０パーセント", "勝負は１本！", "勝利の方程式", "勝率ゼロパーセント", "匠", "将来有望", "消耗戦の達人", "衝撃のドライバー", "衝撃の稲妻", "乗用車使い", "常識を超えるドライブ", "情熱的ファン", "職人の世界", "触るな！危険！", "心のエアバッグ", "心技体の完璧調和", "新たなる伝説", "新たな挑戦者", "新生ハチロク", "申し子", "真夏のビーチに行く途中", "真夜中の悪夢", "真夜中の女豹", "神がかりな何か", "神サマそりゃないよォ！！", "神に選ばれた者", "神のアクセルワーク", "神業", "神聖の翼", "親バカ", "親子二代", "親友の愛車", "進化する天才", "人一倍熱血漢", "人間コンピューター", "人間シャーシダイナモ", "人車一体", "人生アクセル全開！！", "人生いろいろ", "人生はハーフアクセル", "人生観が変わるほどの衝撃", "仁義なき走り屋", "水を得た魚", "酔い止め服用", "酔狂のヒルクライマー", "寸分たがわぬクラッチミート", "世界一だぜせかいいち！！", "世界最強のテンロク", "晴れ男", "正真正銘の本モノ", "正統派", "清楚な乙女", "精度が違う！？", "聖地神奈川", "青春まっただなか", "静かなるドライバー", "積極的に踏む人", "赤いイナズマ", "赤城のゴロツキ", "赤城の白い彗星", "絶体絶命", "絶妙のマシンコントロール", "先行逃げ切りタイプ", "千里眼を持つ者", "選ばれた人間", "全開", "全開で飛ばせ", "全開ヒルクライム", "全国制覇！", "全身全霊", "壮絶なカニ走り", "想定外", "草食系男子", "走りなれてる峠（やま）", "走りに死角なし", "走りのエゴ", "走りの真骨頂", "走りの神髄", "走りの頂点", "走り屋（リアル）", "走り屋の誇り", "走り屋仲間", "走り出した伝説", "走る悦び", "走る喜びを知るもの", "打倒、ハチロク！！", "大人の味わい", "大胆不敵", "大明神", "卓越したドライビングセンス", "誰が呼んだか、その名は‥", "弾丸スプリンター", "男の決心", "地元スペシャルゥ…？", "地元のアドバンテージ", "地元の意地", "地元の常連", "地元最強", "地獄に仏", "地方遠征隊", "池谷の二の舞", "筑波のゴロツキ", "超人", "超絶ＧＴ‐Ｒ", "超熱血漢", "追走するカナリーイエロー", "痛快ボクサー", "通りすがり", "低中速コーナーの鉄人", "弟子は取りません！", "鉄人", "天下統一", "天駆ける翼", "天才ドライバー", "天才的ドライビングセンス", "天才肌", "天上天下唯我独尊", "天性のセンス", "天然（ナチュラル）", "天然おやじキラー", "天然ボケ", "伝説の走り屋", "伝説の男", "伝説誕生の立会人", "伝統と革新の狭間", "電光ステアリング", "電光石火", "努力した奴が勝つ", "努力家", "度胸一発", "怒りのヒルクライム", "怒りの咆哮", "怒涛のゴール", "冬を制する者", "東堂塾ＯＢ", "東堂塾のエース", "藤原ゾーン", "藤原とうふ店", "豆腐屋の息子", "頭文字Ｄジャンキー", "同調の達人", "峠がはぐくんだ奇蹟の走り", "峠センスのかたまり", "峠のプリンス", "峠の王子様", "峠の王様", "峠の釜めし好き", "峠の桜吹雪", "峠の手品師", "峠の狩人", "峠の女神", "峠の堕天使", "峠の番長", "峠仙人", "特攻隊長", "突っつき屋", "突撃！", "謎の走り屋Ｘ", "謎の達人", "肉食系男子", "入賞ドライバー", "猫好き", "熱き魂", "配達帰り", "白き翼を持つ者", "白と黒の閃光", "白銀バトル", "爆走する鉄の塊", "爆弾野郎", "爆熱のヒルクライマー", "爆裂", "箱根のゴロツキ", "罰金百万円", "板金７万円コース", "盤石のコントロール", "彼氏募集中", "彼女いない歴＝年齢", "彼女がほしくてたまらない", "彼女募集中", "秘密兵器", "非凡な才能", "必殺のサイドプレス", "百戦錬磨", "漂泊の走り屋", "不確定要素", "不完全な覚醒", "不器用なぐらいに真剣", "不屈の闘志", "不思議なめぐりあわせ", "不死身のドライバー", "不死鳥", "不世出の天才", "負けずギライ", "負けなしの走り屋", "負けられない戦いがある！", "封印を解いた", "風に舞う落ち葉", "復活したカリスマ", "別な次元", "変化しながら加速", "暮れなずむドライバー", "某とうふ屋", "本モノのドリフト", "本番に強い", "凡人", "魔人の走り", "魔法使い", "満を持して登場", "未知の領域", "未来に描くライン", "妙義のゴロツキ", "妙義の谷の悪魔", "夢を語りあえるヒト", "無の心", "無意識に反応するセンス", "無限の勝利", "無限の戦闘力", "無事故無違反", "無双", "無敵のダウンヒラー", "無敵の戦闘機", "無敗伝説", "名も無き走り屋", "模範ドライバー", "目からウロコが落ちた", "問題児", "夜の闇を切り裂く閃光", "勇猛果敢なアタック", "友情パワー", "有言実行", "有名なドリフトドライバー", "翼－ＷＩＮＧ－", "翼の持ち主", "理想のライン", "理論派", "流星の如く", "流麗なるドリフト", "龍王", "龍鬼", "涼介のファン", "良いドリフト", "類稀なるドリフト", "例によって瞑想中‥", "冷静なアクセルワーク", "冷静沈着", "冷徹なる策士", "渾身のダウンヒルアタック", "獰猛な野獣", "類は友を呼ぶ", "天地開闢", "免許皆伝", "白い悪魔", "幽霊（ゴースト）ライン", "デッド・オア・アライブ", "グランツーリスモ", "ミッドシップスペシャリスト", "原点回帰", "運命の出会い", "本モノはどっちだ！？", "宇宙一のハチロク使い！", "究極の公道パフォーマンス", "最高レベルの技術", "最速のFC", "超一流の職人", "超一流の走り屋", "伝説の再来", "伝説の終結者"]
data_dict = dict()

def pretty_bytes(byte_data, byte_order='big'):
    if byte_order not in ('big', 'little'):
        raise Exception("Byte order must be big or little")
    num = int.from_bytes(byte_data, byteorder=byte_order)
    hex_str = hex(num)[2:]
    expected_length = len(byte_data) * 2
    hex_str = hex_str.zfill(expected_length)
    return '0x' + hex_str

def safe_bytes(byte_data, size, byteorder='little', signed=False):
    if not byte_data:
        return b'\x00' * size
    if byteorder not in ('little', 'big'):
        raise ValueError("Invalid byte order")
    if isinstance(byte_data, str):
        if byte_data.startswith('0x'):
            byte_data = byte_data[2:]
        if len(byte_data) % 2 != 0:
            byte_data = '0' + byte_data
        byte_data = bytes.fromhex(byte_data)
    elif isinstance(byte_data, int):
        return byte_data.to_bytes(size, byteorder=byteorder, signed=signed)
    if byteorder == 'big':
        byte_data = byte_data[::-1]
    if byteorder == 'little':
        byte_data = byte_data.ljust(size, b'\x00')
    else:
        byte_data = byte_data.rjust(size, b'\x00')
    return byte_data[:size]

def ms_to_time(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    remaining_milliseconds = (ms % 60000) % 1000
    return f"{minutes}'{seconds:02}\"{remaining_milliseconds:03}"

def time_to_ms(time_str):
    minutes, rest = time_str.split("'")
    seconds, milliseconds = rest.split('"')
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    total_ms = (minutes * 60000) + (seconds * 1000) + milliseconds
    return total_ms

def read_card(filename):
    f = filename
    header = f.read(80)
    data_dict["Game Version"] = [card_version_dict[pretty_bytes(f.read(2), byte_order='little')], True]
    data_dict["Issued Store"] = [pretty_bytes(f.read(2)), False]
    data_dict["User ID"] = [int.from_bytes(f.read(4), byteorder="big", signed=True), False]
    data_dict["Home Area"] = [prefectures[int.from_bytes(f.read(2), byteorder="little")], True]
    data_dict["Avatar Gender"] = [avatar_gender_list[int.from_bytes(f.read(2), byteorder="little")], True]
    data_dict["Previous Card ID"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}"] = [dcoin, False]
    data_dict["Year"] = [pretty_bytes(f.read(2)), False]
    data_dict["Month"] = [pretty_bytes(f.read(2)), False]
    data_dict["D.Net Stamp"] = [pretty_bytes(f.read(2)), False]
    data_dict["Error Count"] = [pretty_bytes(f.read(2)), False]
    data_dict["Checksum"] = [pretty_bytes(f.read(2)), False]
    for i in range(3):
        dcoin = int.from_bytes(f.read(2), byteorder="little")
        data_dict[f"DCoin{i}_2"] = [dcoin, False]
    data_dict["Year_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Month_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["D.Net Stamp_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Error Count_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Checksum_2"] = [pretty_bytes(f.read(2)), False]
    data_dict["Store Name"] = [(f.read(32).rstrip(b'\x00')).decode('shift-jis'), True]
    config_flag_1 = pretty_bytes(f.read(1))
    data_dict["Wheel Sensitivity"] = [int(config_flag_1[3]), True]
    data_dict["BGM Volume"] = [bgm_volume_list[int(config_flag_1[2])], True]
    config_flag_2 = pretty_bytes(f.read(1))
    config_flag_3 = bin(int.from_bytes(f.read(1), byteorder="little"))[2:].zfill(8)
    data_dict["Force Quit"] = [(int(config_flag_3[7])), True]
    data_dict["Cornering Guide"] = [(int(config_flag_3[6])), True]
    data_dict["Guide Line"] = [(int(config_flag_3[5])), True]
    data_dict["Cup"] = [(int(config_flag_3[4])), True]
    data_dict["Barricade"] = [(int(config_flag_3[3])), True]
    data_dict["Ghost Car"] = [(int(config_flag_3[2])), True]
    data_dict["Class"] = [class_list[int.from_bytes(f.read(1), byteorder="little")-1], True]
    data_dict["Class (Match)"] = [class_list[int.from_bytes(f.read(1), byteorder="little")], False]
    data_dict["Class (Tag Match)"] = [class_list[int.from_bytes(f.read(1), byteorder="little")], False]
    data_dict["Current Car"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Number of Cars"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Play Count"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Pride Points"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Pride Points"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Class Gauge"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Team ID"] = [int.from_bytes(f.read(4), byteorder="little", signed=True), False]
    data_dict["First Card ID"] = [pretty_bytes(f.read(4)), False]
    data_dict["Team Flag"] = [pretty_bytes(f.read(4)), False]
    data_dict["Driver Flags"] = [pretty_bytes(f.read(4)), False]
    data_dict["Driver Points"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Avatar"] = [pretty_bytes(f.read(12)), True]
    padding = f.read(32)
    data_dict["Driver Name"] = [(f.read(14).rstrip(b'\x00')).decode('shift-jis'), True]
    data_dict["CRC01"] = [pretty_bytes(f.read(2)), False]
    for i in range(data_dict["Number of Cars"][0]):
        car_dict = dict()
        model = int.from_bytes(f.read(1), byteorder="little")
        make = make_list[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Make"] = make
        car_dict["Model"] = model_dict[make][model]
        car_dict["Color"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Tuning"] = pretty_bytes(f.read(2))
        car_dict["Option Flag"] = pretty_bytes(f.read(2))
        car_dict["Car Flag"] = pretty_bytes(f.read(2))
        padding = f.read(2)
        for j in range(4):
            car_dict[f"Event Sticker {j+1}"] = int.from_bytes(f.read(1), byteorder="little", signed=True)
        car_dict["Battle Wins"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Bought Sequence ID"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Infinity Tune"] = int.from_bytes(f.read(2), byteorder="little")
        padding = f.read(2)
        car_dict["Numplate Prefecture"] = car_prefectures[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Hirigana"] = car_hirigana[int.from_bytes(f.read(1), byteorder="little")]
        car_dict["Numplate Class Code"] = int.from_bytes(f.read(2), byteorder="little")
        car_dict["Numplate Plate Number"] = int.from_bytes(f.read(4), byteorder="little")
        car_dict["Customizations"] = pretty_bytes(f.read(64))
        data_dict[f"Car {i+1}"] = [car_dict, True]
    for i in range(3 - data_dict["Number of Cars"][0]):
        f.read(96)
    data_dict["Avatar Points"] = [int.from_bytes(f.read(1), byteorder="little"), False]
    data_dict["My Frame"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Selected Cup"] = [cup_list[int.from_bytes(f.read(1), byteorder="little")], True]
    data_dict["Tachometer"] = [tachometer_list[int.from_bytes(f.read(1), byteorder="little")], True]
    padding = f.read(1)
    data_dict["Battle Stance"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["CRC11"] = [pretty_bytes(f.read(2)), False]
    padding = f.read(2)
    data_dict["Story Losses"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Story Wins"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    padding = f.read(6)
    data_dict["Infinity Result Data 1"] = [pretty_bytes(f.read(1)), False]
    data_dict["Infinity Result Data 2"] = [pretty_bytes(f.read(1)), False]
    data_dict["Infinity Rank"] = [int.from_bytes(f.read(2), byteorder="little"), True]
    data_dict["Story Progress"] = [pretty_bytes(f.read(24)), True]
    padding = f.read(4)
    course_dict = dict()
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course] = {"Time": ms_to_time(int.from_bytes(f.read(3), byteorder="little"))}
        termination = f.read(1)
    data_dict["Courses"] = [course_dict, True]
    for i in range(len(courses)):
        course = courses[i]
        model = int.from_bytes(f.read(1), byteorder="little", signed=True)
        make = make_list[int.from_bytes(f.read(1), byteorder="little", signed=True)]
        if model == -1:
            course_dict[course]["Car Make"] = "Not Played"
            course_dict[course]["Car Model"] = "Not Played"
        else:
            course_dict[course]["Car Make"] = make
            course_dict[course]["Car Model"] = model_dict[make][model]
    data_dict["Net VS. Plays"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Wins"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    padding = f.read(4)
    data_dict["Net Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Refuse Course Flag"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Total In-Store Plays"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Total In-Store Wins"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["In-Store Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["In-Store Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["In-Store Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course]["In-Store Wins"] = int.from_bytes(f.read(1), byteorder="little")
    padding = f.read(4)
    data_dict["Net Tag VS Plays"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Tag VS Wins"] = [int.from_bytes(f.read(4), byteorder="little"), False]
    data_dict["Net Tag VS Now Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Tag VS Now Count Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Net Tag VS Count Win Max"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    padding = f.read(6)
    data_dict["Tag Level EXP"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Total Bought"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["CRC12"] = [pretty_bytes(f.read(2)), False]
    padding = f.read(2)
    data_dict["Tag Story Level"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Story Progress"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Tag Story Lose Count"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    padding = f.read(1)
    data_dict["Tag New Comer"] = [bool(int.from_bytes(f.read(1), byteorder="little")), False]
    data_dict["Tag Story Wins"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    course_proficiency_dict = dict()
    for i in range(16):
        course = courses[i*2]
        course_proficiency_dict[course[:-5].rstrip()] = int.from_bytes(f.read(2), byteorder="little")
    data_dict["Course Proficiency"] = [course_proficiency_dict, True]
    for i in range(3):
        data_dict[f"Pro D Mission Flag {i}"] = [pretty_bytes(f.read(2)), False]
    data_dict["Pro D Mission Page"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(3):
        data_dict[f"Pro D Mission Flag Done {i}"] = [pretty_bytes(f.read(2)), False]
    data_dict["Pro D Mission Page Done"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    data_dict["Mileage"] = [int.from_bytes(f.read(4), byteorder="little"), True]
    data_dict["Aura"] = [aura_list[int.from_bytes(f.read(1), byteorder="little")], True]
    data_dict["Title Effect"] = [int.from_bytes(f.read(1), byteorder="little"), True]
    data_dict["Title"] = [title_list[int.from_bytes(f.read(2), byteorder="little")-1], True]
    for i in range(10):
        data_dict[f"Title Stocker {i}"] = [int.from_bytes(f.read(1), byteorder="little"), False]
    data_dict["CRC13"] = [pretty_bytes(f.read(2)), False]
    for i in range(3):
        data_dict[f"Parts Stocker Index {i}"] = [int.from_bytes(f.read(2), byteorder="little"), False]
    for i in range(45):
        data_dict[f"Parts Stocker {i}"] = [int.from_bytes(f.read(2), byteorder="little", signed=True), False]
    data_dict["Parts Stocker Position 0"] = [int.from_bytes(f.read(1), byteorder="little", signed=True), False]
    data_dict["Parts Stocker Position 1"] = [int.from_bytes(f.read(1), byteorder="little", signed=True), False]
    data_dict["CRC21"] = [pretty_bytes(f.read(2)), False]
    for i in range(len(courses)):
        course = courses[i]
        course_dict[course]["Lap 1"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
        course_dict[course]["Lap 2"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
        course_dict[course]["Lap 3"] = ms_to_time(int.from_bytes(f.read(2), byteorder="little"))
    tuning_dict = dict()
    for i in range(25):
        tuning_dict[f"Car {i}"] = pretty_bytes(f.read(1))
    data_dict["Car Tunings"] = [tuning_dict, False]
    data_dict["Time Release Car Open Flag"] = [pretty_bytes(f.read(1)), False]
    padding = f.read(4)
    data_dict["CRC22"] = [pretty_bytes(f.read(2)), False]
    return data_dict

def write_card(filename, data_dict):
    f = filename
    f.seek(80)
    f.write(safe_bytes(card_version_dict.inverse.get(data_dict["Game Version"][0]), 2, byteorder='big'))
    f.write(safe_bytes(data_dict["Issued Store"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["User ID"][0], 4, byteorder='big', signed=True))
    f.write(safe_bytes(prefectures.index(data_dict["Home Area"][0]), 2, byteorder='little'))
    f.write(safe_bytes(avatar_gender_list.index(data_dict["Avatar Gender"][0]), 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Previous Card ID"][0], 4, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}"][0]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum"][0], 2, byteorder='little'))
    for i in range(3):
        dcoin = data_dict[f"DCoin{i}_2"][0]
        f.write(safe_bytes(dcoin, 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Year_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Month_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["D.Net Stamp_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Error Count_2"][0], 2, byteorder='little'))
    f.write(safe_bytes(data_dict["Checksum_2"][0], 2, byteorder='little'))
    store_name = data_dict["Store Name"][0].encode('shift-jis')
    padded_store_name = store_name + b'\0' * (32 - len(store_name))  # Pad with null bytes to 32 bytes
    f.write(safe_bytes(padded_store_name, 32, byteorder='little'))

    config_flag_1 = ''
    config_flag_1 += str(bgm_volume_list.index(data_dict["BGM Volume"][0]))
    config_flag_1 += str(data_dict["Wheel Sensitivity"][0])
    f.write(safe_bytes(config_flag_1, 1))
    config_flag_2 = f.read(1)

    config_flag_3 = '00'
    config_flag_3 += str(data_dict["Ghost Car"][0])
    config_flag_3 += str(data_dict["Barricade"][0])
    config_flag_3 += str(data_dict["Cup"][0])
    config_flag_3 += str(data_dict["Guide Line"][0])
    config_flag_3 += str(data_dict["Cornering Guide"][0])
    config_flag_3 += str(data_dict["Force Quit"][0])
    f.write(safe_bytes(int(config_flag_3, 2), 1))

    f.write(safe_bytes(class_list.index(data_dict["Class"][0])+1, 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Match)"][0]), 1))
    f.write(safe_bytes(class_list.index(data_dict["Class (Tag Match)"][0]), 1))
    f.write(safe_bytes(data_dict["Current Car"][0], 1))
    f.write(safe_bytes(data_dict["Number of Cars"][0], 1))
    f.write(safe_bytes(data_dict["Play Count"][0], 2))
    f.write(safe_bytes(data_dict["Pride Points"][0], 2))
    f.write(safe_bytes(data_dict["Tag Pride Points"][0], 2))
    f.write(safe_bytes(data_dict["Class Gauge"][0], 2))
    f.write(safe_bytes(data_dict["Team ID"][0], 4, signed=True))
    f.write(safe_bytes(data_dict["First Card ID"][0], 4))
    f.write(safe_bytes(data_dict["Team Flag"][0], 4))
    f.write(safe_bytes(data_dict["Driver Flags"][0], 4))
    f.write(safe_bytes(int(data_dict["Driver Points"][0]), 4))
    f.write(safe_bytes(data_dict["Avatar"][0], 12))
    f.write(b'\x00' * 32)
    encoded_name = data_dict["Driver Name"][0].encode('shift-jis')
    padded_name = encoded_name.ljust(14, b'\x00')
    f.write(safe_bytes(padded_name, 14))
    f.write(safe_bytes(data_dict["CRC01"][0], 2))
    for i in range(data_dict["Number of Cars"][0]):
        car_dict = data_dict[f"Car {i+1}"][0]
        f.write(safe_bytes(model_dict[car_dict["Make"]].index(car_dict["Model"]), 1))
        f.write(safe_bytes(make_list.index(car_dict["Make"]), 1))
        f.write(safe_bytes(car_dict["Color"], 2))
        f.write(safe_bytes(car_dict["Tuning"], 2))
        f.write(safe_bytes(car_dict["Option Flag"], 2))
        f.write(safe_bytes(car_dict["Car Flag"], 2))
        padding = f.read(2)
        for j in range(4):
            f.write(safe_bytes(car_dict[f"Event Sticker {j+1}"], 1, signed=True))
        f.write(safe_bytes(car_dict["Battle Wins"], 2))
        f.write(safe_bytes(car_dict["Bought Sequence ID"], 2))
        f.write(safe_bytes(car_dict["Infinity Tune"], 2))
        padding = f.read(2)
        f.write(safe_bytes(car_prefectures.index(car_dict["Numplate Prefecture"]), 1))
        f.write(safe_bytes(car_hirigana.index(car_dict["Numplate Hirigana"]), 1))
        f.write(safe_bytes(car_dict["Numplate Class Code"], 2))
        f.write(safe_bytes(car_dict["Numplate Plate Number"], 4))
        f.write(safe_bytes(car_dict["Customizations"], 64))
    for i in range(3 - data_dict["Number of Cars"][0]):
        f.read(96)
    f.write(safe_bytes(data_dict["Avatar Points"][0], 1))
    f.write(safe_bytes(int(data_dict["My Frame"][0]), 1))
    f.write(safe_bytes(cup_list.index(data_dict["Selected Cup"][0]), 1))
    f.write(safe_bytes(tachometer_list.index(data_dict["Tachometer"][0]), 1))
    padding = f.read(1)
    f.write(safe_bytes(data_dict["Battle Stance"][0], 1))
    f.write(safe_bytes(data_dict["CRC11"][0], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Story Losses"][0], 2))
    f.write(safe_bytes(data_dict["Story Wins"][0], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Infinity Result Data 1"][0], 1))
    f.write(safe_bytes(data_dict["Infinity Result Data 2"][0], 1))
    f.write(safe_bytes(data_dict["Infinity Rank"][0], 2))
    f.write(safe_bytes(data_dict["Story Progress"][0], 24))
    padding = f.read(4)
    course_dict = data_dict["Courses"][0]
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_dict[course]["Time"]), 3))
        termination = f.read(1)
    for i in range(len(courses)):
        course = courses[i]
        if course_dict[course]["Car Model"] == 'Not Played':
            f.write(safe_bytes('0xFF', 1))
            f.write(safe_bytes('0xFF', 1))
        else:
            f.write(safe_bytes(model_dict[course_dict[course]["Car Make"]].index(course_dict[course]["Car Model"]), 1))
            f.write(safe_bytes(make_list.index(course_dict[course]["Car Make"]), 1))
    f.write(safe_bytes(data_dict["Net VS. Plays"][0], 4))
    f.write(safe_bytes(data_dict["Net Wins"][0], 4))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Now Count"][0], 2))
    f.write(safe_bytes(data_dict["Net Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["Net Count Win Max"][0], 2))
    f.write(safe_bytes(data_dict["Refuse Course Flag"][0], 2))
    f.write(safe_bytes(data_dict["Total In-Store Plays"][0], 4))
    f.write(safe_bytes(data_dict["Total In-Store Wins"][0], 4))
    f.write(safe_bytes(data_dict["In-Store Now Count"][0], 2))
    f.write(safe_bytes(data_dict["In-Store Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["In-Store Count Win Max"][0], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(course_dict[course]["In-Store Wins"], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["Net Tag VS Plays"][0], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Wins"][0], 4))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count"][0], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Now Count Wins"][0], 2))
    f.write(safe_bytes(data_dict["Net Tag VS Count Win Max"][0], 2))
    padding = f.read(6)
    f.write(safe_bytes(data_dict["Tag Level EXP"][0], 2))
    f.write(safe_bytes(data_dict["Total Bought"][0], 2))
    f.write(safe_bytes(data_dict["CRC12"][0], 2))
    padding = f.read(2)
    f.write(safe_bytes(data_dict["Tag Story Level"][0], 2))
    f.write(safe_bytes(data_dict["Tag Story Progress"][0], 2))
    f.write(safe_bytes(data_dict["Tag Story Lose Count"][0], 2))
    padding = f.read(1)
    f.write(safe_bytes(int(data_dict["Tag New Comer"][0]), 1))
    f.write(safe_bytes(data_dict["Tag Story Wins"][0], 2))
    course_proficiency_dict = data_dict["Course Proficiency"][0]
    for i in range(16):
        course = courses[i*2]
        f.write(safe_bytes(course_proficiency_dict[course[:-5].rstrip()], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag {i}"][0], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page"][0], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Pro D Mission Flag Done {i}"][0], 2))
    f.write(safe_bytes(data_dict["Pro D Mission Page Done"][0], 2))
    f.write(safe_bytes(int(data_dict["Mileage"][0]), 4))
    f.write(safe_bytes(aura_list.index(data_dict["Aura"][0]), 1))
    f.write(safe_bytes(int(data_dict["Title Effect"][0]), 1))
    f.write(safe_bytes(title_list.index(data_dict["Title"][0]) + 1, 2))
    for i in range(10):
        f.write(safe_bytes(data_dict[f"Title Stocker {i}"][0], 1))
    f.write(safe_bytes(data_dict["CRC13"][0], 2))
    for i in range(3):
        f.write(safe_bytes(data_dict[f"Parts Stocker Index {i}"][0], 2))
    for i in range(45):
        f.write(safe_bytes(data_dict[f"Parts Stocker {i}"][0], 2, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 0"][0], 1, signed=True))
    f.write(safe_bytes(data_dict["Parts Stocker Position 1"][0], 1, signed=True))
    f.write(safe_bytes(data_dict["CRC21"][0], 2))
    for i in range(len(courses)):
        course = courses[i]
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 1"]), 2))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 2"]), 2))
        f.write(safe_bytes(time_to_ms(course_dict[course]["Lap 3"]), 2))
    tuning_dict = data_dict["Car Tunings"][0]
    for i in range(25):
        f.write(safe_bytes(tuning_dict[f"Car {i}"], 1))
    f.write(safe_bytes(data_dict["Time Release Car Open Flag"][0], 1))
    padding = f.read(4)
    f.write(safe_bytes(data_dict["CRC22"][0], 2))
