"""
47都道府県の観光コースページを生成するスクリプト
出力: content/japan/_index.md + content/japan/{slug}.md × 47
"""

import os
import re
import textwrap

# ─── Prefecture Data ──────────────────────────────────────────────────────────

PREFECTURES = [
    {"name":"北海道","slug":"hokkaido","region":"北海道","lead":"雄大な自然、雪景色、温泉、海鮮を組み合わせやすい長期滞在向けエリア。","areas":["札幌","小樽","富良野","函館"],"spots":["大通公園","美瑛の丘","旭山動物園","函館山"],"seasons":["夏","冬"],"themes":["絶景","グルメ","子連れ","温泉"],"days":"2泊3日から4泊5日","transport":"広域移動はレンタカーかJR。都市部は地下鉄とバスが便利。","stay":"初回は札幌、道南重視なら函館、花畑や丘陵なら富良野・美瑛。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/6/64/Odori_Park_in_Sapporo_-_Hokkaido_Prefecture_at_night_in_March_2026.jpg","title":"Odori Park in Sapporo","license":"CC BY-SA 4.0","artist":"contri"}},
    {"name":"青森県","slug":"aomori","region":"東北","lead":"ねぶた、奥入瀬、弘前城、りんごの食を軸に、夏祭りと自然散策が強い県。","areas":["青森市","弘前","八戸","十和田"],"spots":["ねぶたの家ワ・ラッセ","奥入瀬渓流","弘前城","八食センター"],"seasons":["春","夏","秋"],"themes":["祭り","絶景","グルメ","車なし"],"days":"1泊2日から2泊3日","transport":"新幹線と在来線で都市間移動、奥入瀬方面はバスかレンタカー。","stay":"祭りは青森市、桜は弘前、海鮮は八戸が使いやすい。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/3/3e/Aomori_Nebuta_Festival_2019_Shinmachi_Street.jpg","title":"Aomori Nebuta Festival","license":"CC BY-SA 4.0","artist":"Mccunicano"}},
    {"name":"岩手県","slug":"iwate","region":"東北","lead":"平泉の歴史、三陸海岸、花巻温泉を組み合わせる広域周遊型の旅先。","areas":["盛岡","平泉","花巻","三陸"],"spots":["中尊寺","浄土ヶ浜","小岩井農場","花巻温泉"],"seasons":["春","夏","秋"],"themes":["歴史","絶景","温泉","グルメ"],"days":"1泊2日から2泊3日","transport":"新幹線で盛岡・一ノ関へ入り、三陸は鉄道とレンタカーの併用が現実的。","stay":"都市観光は盛岡、歴史は平泉、温泉重視なら花巻。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/5/5d/Chuson-ji_Belfry_01.jpg","title":"Chuson-ji Belfry","license":"CC BY-SA 3.0","artist":"Tak1701d"}},
    {"name":"宮城県","slug":"miyagi","region":"東北","lead":"仙台の都市観光と松島の景観、温泉、海鮮を短い日程で組みやすい。","areas":["仙台","松島","秋保","鳴子"],"spots":["松島","瑞鳳殿","仙台城跡","秋保温泉"],"seasons":["春","夏","秋"],"themes":["絶景","歴史","温泉","グルメ"],"days":"日帰りから1泊2日","transport":"仙台を起点にJRとバスで動きやすく、松島は車なしでも行きやすい。","stay":"初回は仙台駅周辺、温泉目的なら秋保・鳴子。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/2/21/Fukuura_Island%2C_Matsushima_Miyagi_Aerial_photograph.2015.jpg","title":"Fukuura Island, Matsushima","license":"Attribution","artist":"国土交通省地図・空中写真閲覧サービス"}},
    {"name":"秋田県","slug":"akita","region":"東北","lead":"角館、田沢湖、乳頭温泉郷など、歴史ある街並みと温泉を静かに巡れる。","areas":["秋田市","角館","田沢湖","男鹿"],"spots":["角館武家屋敷","田沢湖","乳頭温泉郷","男鹿半島"],"seasons":["春","秋","冬"],"themes":["温泉","歴史","絶景","穴場"],"days":"1泊2日から2泊3日","transport":"秋田新幹線と路線バスが基本。温泉や男鹿は車があると楽。","stay":"街歩きは角館、温泉重視なら田沢湖・乳頭温泉郷。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/b/b0/Kakunodate_Police_Station%2C_April_2023_01.jpg","title":"Kakunodate","license":"CC BY-SA 4.0","artist":"Calistemon"}},
    {"name":"山形県","slug":"yamagata","region":"東北","lead":"山寺、蔵王、銀山温泉、果物狩りを季節で組み替えられる温泉県。","areas":["山形市","蔵王","天童","庄内"],"spots":["山寺","蔵王温泉","銀山温泉","羽黒山"],"seasons":["夏","秋","冬"],"themes":["温泉","歴史","絶景","グルメ"],"days":"1泊2日から2泊3日","transport":"山形駅を起点にバス移動。蔵王や銀山温泉は時刻確認が重要。","stay":"温泉は蔵王・銀山、街歩きと食は山形駅周辺。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/f/f1/JR_East_Yamadera_Station_Gate%2C_Yamagata_Pref.jpg","title":"Yamadera Station","license":"CC BY-SA 4.0","artist":"Mister0124"}},
    {"name":"福島県","slug":"fukushima","region":"東北","lead":"会津の歴史、大内宿、磐梯吾妻、温泉を組み合わせる周遊旅行に向く。","areas":["会津若松","福島市","郡山","磐梯"],"spots":["大内宿","鶴ヶ城","五色沼","飯坂温泉"],"seasons":["春","夏","秋"],"themes":["歴史","絶景","温泉","ドライブ"],"days":"1泊2日から2泊3日","transport":"会津方面は鉄道とバス、磐梯高原はレンタカーで回りやすい。","stay":"歴史旅は会津若松、温泉なら飯坂・東山。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/8/83/Ouchi-juku%2C_Fukushima%3B_September_2009_%2816%29.jpg","title":"Ouchi-juku","license":"CC BY 2.0","artist":"TANAKA Juuyoh"}},
    {"name":"茨城県","slug":"ibaraki","region":"関東","lead":"花絶景、海沿い、歴史公園を日帰りドライブで巡りやすい首都圏近郊の県。","areas":["水戸","ひたちなか","大洗","つくば"],"spots":["国営ひたち海浜公園","偕楽園","大洗磯前神社","筑波山"],"seasons":["春","夏","秋"],"themes":["絶景","子連れ","ドライブ","花"],"days":"日帰りから1泊2日","transport":"鉄道でも主要地へ行けるが、海沿いと筑波山は車が効率的。","stay":"海沿いなら大洗、街歩きは水戸、研究都市観光はつくば。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/3/3d/Miharashi_no_Oka_%28Hitachi_Seaside_Park%29_01.JPG","title":"Miharashi no Oka","license":"Public domain","artist":"Abasaa"}},
    {"name":"栃木県","slug":"tochigi","region":"関東","lead":"日光の社寺、那須高原、温泉を組み合わせる王道の週末旅。","areas":["日光","宇都宮","那須","鬼怒川"],"spots":["日光東照宮","華厳の滝","那須高原","鬼怒川温泉"],"seasons":["春","秋","冬"],"themes":["歴史","絶景","温泉","子連れ"],"days":"日帰りから1泊2日","transport":"日光は鉄道とバスで可能。那須高原は車が便利。","stay":"歴史は日光、家族旅は那須、温泉なら鬼怒川。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/e/e2/NikkoCaparisonedHorse5423.jpg","title":"Nikko","license":"Public domain","artist":"Fg2"}},
    {"name":"群馬県","slug":"gunma","region":"関東","lead":"草津、伊香保、水上など温泉地が強く、首都圏からの短期旅行に向く。","areas":["草津","伊香保","水上","前橋"],"spots":["草津温泉","伊香保石段街","尾瀬","富岡製糸場"],"seasons":["夏","秋","冬"],"themes":["温泉","歴史","絶景","ドライブ"],"days":"日帰りから1泊2日","transport":"温泉地は高速バスが便利。複数地を巡るなら車。","stay":"温泉目的は草津・伊香保、自然散策は水上・尾瀬方面。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/c/ce/Kusatsu_Onsen%2C_Gunma_Prefecture%3B_November_2018_%2802%29.jpg","title":"Kusatsu Onsen","license":"CC BY 2.0","artist":"雷太"}},
    {"name":"埼玉県","slug":"saitama","region":"関東","lead":"川越、秩父、長瀞など、日帰りで歴史散策と自然を選べる近郊観光地。","areas":["川越","秩父","長瀞","さいたま"],"spots":["小江戸川越","三峯神社","長瀞岩畳","鉄道博物館"],"seasons":["春","秋","冬"],"themes":["歴史","子連れ","車なし","穴場"],"days":"日帰りから1泊2日","transport":"川越と大宮は電車向き。秩父・長瀞は鉄道でも行けるが本数確認が必要。","stay":"街歩きは川越、自然と温泉は秩父。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/1/1e/Kawagoe_in_Saitama_Prefecture.png","title":"Kawagoe","license":"Public domain","artist":"user:alberth2"}},
    {"name":"千葉県","slug":"chiba","region":"関東","lead":"成田山、房総半島、海沿いドライブ、テーマパークを目的別に組みやすい。","areas":["成田","舞浜","館山","銚子"],"spots":["成田山新勝寺","鴨川シーワールド","鋸山","犬吠埼"],"seasons":["春","夏","秋"],"themes":["子連れ","歴史","海","ドライブ"],"days":"日帰りから1泊2日","transport":"成田・舞浜は鉄道、房総半島はレンタカーが効率的。","stay":"子連れは舞浜・鴨川、寺社観光は成田、海旅は館山。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/f/fa/Naritasan-Shinshoji-Temple.Great-Main-Hall.jpg","title":"Naritasan Shinshoji","license":"CC BY-SA 3.0","artist":"Hoku-sou-san"}},
    {"name":"東京都","slug":"tokyo","region":"関東","lead":"都市観光、文化施設、下町、離島まで旅行タイプを細かく分けられる巨大ハブ。","areas":["浅草","銀座","新宿","奥多摩"],"spots":["浅草寺","東京駅","上野公園","高尾山"],"seasons":["春","秋","冬"],"themes":["車なし","雨の日","グルメ","歴史"],"days":"日帰りから2泊3日","transport":"鉄道と地下鉄でほぼ完結。郊外や島旅は日程に余裕を持つ。","stay":"初回は東京駅・上野・新宿、落ち着いた旅は日本橋・蔵前。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/3/35/Minato_City%2C_Tokyo%2C_Japan.jpg","title":"Minato City, Tokyo","license":"CC BY 4.0","artist":"David Kernan"}},
    {"name":"神奈川県","slug":"kanagawa","region":"関東","lead":"横浜、鎌倉、箱根、湘南を短期旅行で組み替えやすい人気エリア。","areas":["横浜","鎌倉","箱根","湘南"],"spots":["みなとみらい","鶴岡八幡宮","芦ノ湖","江の島"],"seasons":["春","夏","秋"],"themes":["車なし","温泉","歴史","デート"],"days":"日帰りから1泊2日","transport":"鉄道移動が強い。箱根は登山電車とバスの周遊券が便利。","stay":"都市観光は横浜、温泉は箱根、海辺は湘南・鎌倉。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/d/d2/070203_MM21%26FUJI.jpg","title":"Minato Mirai and Fuji","license":"CC BY-SA 3.0","artist":"名古屋太郎"}},
    {"name":"新潟県","slug":"niigata","region":"中部","lead":"米どころの食、佐渡島、越後湯沢、雪国文化を季節で楽しめる。","areas":["新潟市","佐渡","越後湯沢","長岡"],"spots":["佐渡金山","清津峡","越後湯沢温泉","弥彦神社"],"seasons":["夏","秋","冬"],"themes":["グルメ","温泉","絶景","離島"],"days":"1泊2日から2泊3日","transport":"新幹線で入りやすく、佐渡はフェリー時間を軸に計画する。","stay":"食と街歩きは新潟市、温泉は越後湯沢、島旅は佐渡。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/7/70/Tabi_miyage_dai_nish%C5%AB%2C_Sado_Aikawa-machi_by_Kawase_Hasui.jpg","title":"Sado Aikawa-machi","license":"Public domain","artist":"Hasui Kawase"}},
    {"name":"富山県","slug":"toyama","region":"中部","lead":"立山黒部、富山湾鮨、五箇山を組み合わせる山海のコンパクト旅。","areas":["富山市","立山","黒部","高岡"],"spots":["立山黒部アルペンルート","黒部峡谷","雨晴海岸","五箇山"],"seasons":["春","夏","秋"],"themes":["絶景","グルメ","歴史","車なし"],"days":"1泊2日から2泊3日","transport":"北陸新幹線と地鉄、アルペンルートは乗り継ぎ計画が重要。","stay":"街歩きは富山市、山岳観光は立山・宇奈月。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/c/c1/Tateyama_Kurobe_Alpine_Route%2C_Map_%28Universal%29.jpg","title":"Tateyama Kurobe Alpine Route Map","license":"Public domain","artist":"Batholith"}},
    {"name":"石川県","slug":"ishikawa","region":"中部","lead":"金沢の文化観光、能登、加賀温泉郷を組み合わせる大人旅向き。","areas":["金沢","加賀","能登","白山"],"spots":["兼六園","ひがし茶屋街","近江町市場","加賀温泉郷"],"seasons":["春","秋","冬"],"themes":["歴史","グルメ","温泉","車なし"],"days":"1泊2日から2泊3日","transport":"金沢市内はバス周遊が便利。能登・白山方面は車向き。","stay":"初回は金沢、温泉目的なら山代・山中・片山津。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/a/a0/131109_Kenrokuen_Kanazawa_Ishikawa_pref_Japan01s3.jpg","title":"Kenrokuen Kanazawa","license":"CC BY 2.5","artist":"663highland"}},
    {"name":"福井県","slug":"fukui","region":"中部","lead":"恐竜、永平寺、東尋坊、越前がにを軸に家族旅と歴史旅を作りやすい。","areas":["福井市","勝山","あわら","敦賀"],"spots":["福井県立恐竜博物館","永平寺","東尋坊","一乗谷朝倉氏遺跡"],"seasons":["春","夏","冬"],"themes":["子連れ","歴史","グルメ","温泉"],"days":"1泊2日","transport":"北陸新幹線とバスが基本。海沿い周遊は車が便利。","stay":"子連れは福井市・勝山、温泉はあわら。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/1/18/Temple_Eihei%2C_Eiheiji_town%2C_Fukui_Prefecture.JPG","title":"Temple Eihei","license":"CC BY-SA 3.0","artist":"黒ゆり"}},
    {"name":"山梨県","slug":"yamanashi","region":"中部","lead":"富士山、湖、ワイナリー、温泉を首都圏から短期で楽しめる。","areas":["富士五湖","甲府","勝沼","清里"],"spots":["河口湖","忍野八海","昇仙峡","勝沼ワイナリー"],"seasons":["春","夏","秋"],"themes":["絶景","温泉","グルメ","ドライブ"],"days":"日帰りから1泊2日","transport":"高速バスと鉄道で富士五湖へ。複数湖を巡るなら車が便利。","stay":"富士山眺望は河口湖、温泉と食は石和・甲府。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/3/36/Lake_Kawaguchiko_Sakura_Mount_Fuji_4.JPG","title":"Lake Kawaguchiko and Mount Fuji","license":"CC BY 3.0","artist":"Midori"}},
    {"name":"長野県","slug":"nagano","region":"中部","lead":"山岳景観、善光寺、軽井沢、温泉を目的別に展開できる強い観光県。","areas":["長野市","松本","軽井沢","上高地"],"spots":["善光寺","松本城","上高地","地獄谷野猿公苑"],"seasons":["夏","秋","冬"],"themes":["絶景","温泉","歴史","避暑"],"days":"1泊2日から3泊4日","transport":"新幹線と特急で主要地へ。高原や温泉地はバス時刻を確認。","stay":"初回は長野市か松本、避暑は軽井沢・蓼科、山歩きは上高地周辺。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/8/88/150920_Kappa-bashi_Kamikochi_Japan01n.jpg","title":"Kappa-bashi Kamikochi","license":"CC BY 2.5","artist":"663highland"}},
    {"name":"岐阜県","slug":"gifu","region":"中部","lead":"白川郷、飛騨高山、下呂温泉、郡上八幡を巡る歴史と温泉の県。","areas":["高山","白川郷","下呂","岐阜市"],"spots":["白川郷","飛騨高山古い町並","下呂温泉","岐阜城"],"seasons":["春","秋","冬"],"themes":["歴史","温泉","絶景","グルメ"],"days":"1泊2日から2泊3日","transport":"高山線と高速バスが基本。白川郷は予約制バスも確認。","stay":"街歩きは高山、温泉は下呂、城下町は岐阜市。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/e/e6/Ogi_Shirakawa-g%C5%8D%2C_Gifu%2C_Japan.jpg","title":"Ogi Shirakawa-go","license":"CC BY 2.5","artist":"663highland"}},
    {"name":"静岡県","slug":"shizuoka","region":"中部","lead":"富士山、伊豆、浜名湖、茶畑を横長の県土で目的別に分けると探しやすい。","areas":["静岡市","伊豆","富士宮","浜松"],"spots":["三保松原","修善寺温泉","富士山本宮浅間大社","浜名湖"],"seasons":["春","夏","秋"],"themes":["絶景","温泉","海","グルメ"],"days":"日帰りから2泊3日","transport":"新幹線駅が多く入りやすい。伊豆半島周遊は車が便利。","stay":"温泉は伊豆、富士山眺望は富士・清水、うなぎと湖は浜松。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/9/97/Mount_Fuji_%28Japan%29.jpg","title":"Mount Fuji","license":"CC BY-SA 4.0","artist":"Dandy1022"}},
    {"name":"愛知県","slug":"aichi","region":"中部","lead":"名古屋めし、城、産業観光、離島を都市滞在から日帰りで伸ばせる。","areas":["名古屋","犬山","常滑","三河湾"],"spots":["名古屋城","熱田神宮","犬山城","リニア・鉄道館"],"seasons":["春","秋","冬"],"themes":["グルメ","歴史","子連れ","車なし"],"days":"日帰りから1泊2日","transport":"名古屋市内は地下鉄、犬山や常滑も鉄道で行きやすい。","stay":"初回は名古屋駅・栄、城下町なら犬山。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/4/45/Nagoya_Castle%28Larger%29.jpg","title":"Nagoya Castle","license":"CC BY-SA 3.0","artist":"Base64"}},
    {"name":"三重県","slug":"mie","region":"近畿","lead":"伊勢神宮、鳥羽水族館、熊野古道、松阪牛を目的別に展開できる。","areas":["伊勢","鳥羽","志摩","熊野"],"spots":["伊勢神宮","おかげ横丁","鳥羽水族館","熊野古道伊勢路"],"seasons":["春","夏","秋"],"themes":["歴史","子連れ","グルメ","海"],"days":"1泊2日から2泊3日","transport":"近鉄で伊勢・鳥羽へ。志摩や熊野は日程と交通を分ける。","stay":"参拝は伊勢、海景色と水族館は鳥羽・志摩。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/1/1a/Ise-Grand-Shrine-Emperor-Meiji-Sadahide-Utagawa-1869.png","title":"Ise Grand Shrine","license":"Public domain","artist":"Sadahide Utagawa"}},
    {"name":"滋賀県","slug":"shiga","region":"近畿","lead":"琵琶湖を中心に、城、寺社、湖畔カフェ、サイクリングを組みやすい。","areas":["大津","彦根","近江八幡","長浜"],"spots":["琵琶湖","彦根城","近江八幡水郷","比叡山延暦寺"],"seasons":["春","夏","秋"],"themes":["歴史","絶景","ドライブ","車なし"],"days":"日帰りから1泊2日","transport":"JRで湖東・湖南を移動しやすい。湖西や湖北周遊は車も便利。","stay":"京都連泊の日帰りも可能。湖畔滞在は大津・長浜。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/1/15/Drone_shot_of_Otsu_and_Lake_Biwa_2.jpg","title":"Otsu and Lake Biwa","license":"CC BY-SA 4.0","artist":"Benlisquare"}},
    {"name":"京都府","slug":"kyoto","region":"近畿","lead":"寺社、町家、庭園、丹後の海まで、混雑回避と朝観光の設計が重要。","areas":["京都市","宇治","嵐山","天橋立"],"spots":["清水寺","伏見稲荷大社","平等院","天橋立"],"seasons":["春","秋","冬"],"themes":["歴史","車なし","雨の日","混雑回避"],"days":"1泊2日から3泊4日","transport":"市内は地下鉄・バス・徒歩。混雑時はエリアを絞る。","stay":"初回は京都駅・四条、落ち着いた旅は岡崎・御所周辺。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/d/d8/Four_ladies_wearing_a_yukata_in_front_of_the_North_Gate_of_Kiyomizu-dera_temple_Kyoto_Japan.jpg","title":"Kiyomizu-dera temple Kyoto","license":"CC BY-SA 4.0","artist":"Basile Morin"}},
    {"name":"大阪府","slug":"osaka","region":"近畿","lead":"食、城、商店街、テーマパーク、近郊観光の起点として使いやすい都市型旅行先。","areas":["梅田","難波","天王寺","ベイエリア"],"spots":["大阪城","道頓堀","新世界","海遊館"],"seasons":["春","秋","冬"],"themes":["グルメ","子連れ","雨の日","車なし"],"days":"日帰りから2泊3日","transport":"地下鉄とJRで完結。京都・神戸・奈良への日帰り拠点にも向く。","stay":"買い物は梅田、食べ歩きは難波、家族旅はベイエリア。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/b/b9/Osaka_Castle_Outer_Moat_and_Osaka_Business_Park%2C_November_2016.jpg","title":"Osaka Castle Outer Moat","license":"CC BY-SA 4.0","artist":"Martin Falbisoner"}},
    {"name":"兵庫県","slug":"hyogo","region":"近畿","lead":"神戸、姫路城、有馬温泉、淡路島、城崎温泉まで多様な目的に対応。","areas":["神戸","姫路","有馬","淡路島"],"spots":["姫路城","神戸北野","有馬温泉","城崎温泉"],"seasons":["春","秋","冬"],"themes":["歴史","温泉","グルメ","ドライブ"],"days":"1泊2日から2泊3日","transport":"神戸・姫路は鉄道が便利。淡路島や温泉周遊は車も有効。","stay":"都市観光は神戸、温泉は有馬・城崎、城旅は姫路。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/7/7d/Ch%C3%A2teau_de_Himeji02.jpg","title":"Himeji Castle","license":"CC BY-SA 3.0","artist":"Bernard Gagnon"}},
    {"name":"奈良県","slug":"nara","region":"近畿","lead":"古都の寺社、山の辺の道、吉野の桜を徒歩と鉄道で巡る歴史旅向き。","areas":["奈良市","斑鳩","飛鳥","吉野"],"spots":["東大寺","春日大社","法隆寺","吉野山"],"seasons":["春","秋","冬"],"themes":["歴史","車なし","桜","一人旅"],"days":"日帰りから1泊2日","transport":"近鉄とJRが便利。寺社巡りは徒歩時間を多めに見る。","stay":"初回は奈良駅周辺、吉野や飛鳥は別日程で組むと楽。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/4/47/Daibutsuden%2C_Nara.jpg","title":"Daibutsuden, Nara","license":"CC BY-SA 4.0","artist":"Unknown"}},
    {"name":"和歌山県","slug":"wakayama","region":"近畿","lead":"高野山、熊野三山、白浜温泉、海岸絶景を巡る信仰と温泉の県。","areas":["高野山","白浜","熊野","和歌山市"],"spots":["高野山","熊野那智大社","白良浜","アドベンチャーワールド"],"seasons":["春","夏","秋"],"themes":["歴史","温泉","子連れ","絶景"],"days":"1泊2日から2泊3日","transport":"高野山と白浜は鉄道で行ける。熊野周遊は移動時間を長めに確保。","stay":"信仰体験は高野山、温泉と海は白浜、熊野古道は勝浦周辺。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/f/f8/Narrow_rock_garden%2C_Kongobuji%2C_Koyasan%2C_2016.jpg","title":"Kongobuji, Koyasan","license":"CC0","artist":"DimiTalen"}},
    {"name":"鳥取県","slug":"tottori","region":"中国","lead":"砂丘、温泉、山陰海岸、境港を組み合わせる穴場の自然旅。","areas":["鳥取市","倉吉","米子","境港"],"spots":["鳥取砂丘","三朝温泉","投入堂","水木しげるロード"],"seasons":["春","夏","秋"],"themes":["絶景","温泉","子連れ","穴場"],"days":"1泊2日","transport":"東西に長いためエリアを絞る。砂丘周辺はバス、広域は車が便利。","stay":"砂丘は鳥取市、温泉は三朝、家族旅は米子・境港。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/e/e1/Tottori-Sakyu_Tottori_Japan.JPG","title":"Tottori Sand Dunes","license":"CC BY-SA 3.0","artist":"Hashi photo"}},
    {"name":"島根県","slug":"shimane","region":"中国","lead":"出雲大社、松江城、石見銀山、隠岐を静かに巡る歴史と縁結びの県。","areas":["出雲","松江","石見","隠岐"],"spots":["出雲大社","松江城","足立美術館","石見銀山"],"seasons":["春","秋","冬"],"themes":["歴史","縁結び","穴場","一人旅"],"days":"1泊2日から2泊3日","transport":"出雲・松江は鉄道とバス。石見や隠岐は日程を分ける。","stay":"参拝は出雲、城下町と湖景色は松江。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/c/c6/Izumo_Taisha_gardens.jpg","title":"Izumo Taisha gardens","license":"CC BY 4.0","artist":"Immanuelle"}},
    {"name":"岡山県","slug":"okayama","region":"中国","lead":"後楽園、倉敷、瀬戸内の島々、フルーツを鉄道で巡りやすい。","areas":["岡山市","倉敷","児島","蒜山"],"spots":["岡山後楽園","倉敷美観地区","吉備津神社","瀬戸大橋"],"seasons":["春","秋","冬"],"themes":["歴史","車なし","グルメ","アート"],"days":"日帰りから1泊2日","transport":"岡山駅を起点に倉敷へ鉄道移動しやすい。蒜山は車向き。","stay":"初回は岡山市か倉敷。アート旅は瀬戸内方面と組む。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/5/53/Kurashiki_Bikan_historical_quarter_20190324.jpg","title":"Kurashiki Bikan historical quarter","license":"CC BY-SA 4.0","artist":"Suicasmo"}},
    {"name":"広島県","slug":"hiroshima","region":"中国","lead":"宮島、平和記念公園、尾道、しまなみ海道を歴史と海景色で展開できる。","areas":["広島市","宮島","尾道","福山"],"spots":["厳島神社","平和記念公園","尾道","鞆の浦"],"seasons":["春","秋","冬"],"themes":["歴史","絶景","グルメ","車なし"],"days":"1泊2日から2泊3日","transport":"広島市と宮島は公共交通で快適。尾道・しまなみは自転車や車も選択肢。","stay":"初回は広島市、海辺の滞在は宮島・尾道。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/0/0e/Itsukushima_Gate.jpg","title":"Itsukushima Gate","license":"CC BY-SA 3.0","artist":"JordyMeow"}},
    {"name":"山口県","slug":"yamaguchi","region":"中国","lead":"角島、秋吉台、萩、下関をドライブで巡る絶景と歴史の穴場県。","areas":["下関","萩","山口市","長門"],"spots":["角島大橋","秋吉台","元乃隅神社","萩城下町"],"seasons":["春","夏","秋"],"themes":["絶景","ドライブ","歴史","穴場"],"days":"1泊2日から2泊3日","transport":"県内周遊はレンタカーが強い。下関・山口市は鉄道利用も可能。","stay":"海鮮は下関、歴史は萩、温泉と絶景は長門。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/2/20/Akiyoshidai_Yamaguchi_Japan.jpg","title":"Akiyoshidai Yamaguchi","license":"CC BY 2.0","artist":"uesakakohei"}},
    {"name":"徳島県","slug":"tokushima","region":"四国","lead":"阿波おどり、鳴門の渦潮、祖谷渓を組み合わせる体験型の旅先。","areas":["徳島市","鳴門","祖谷","阿南"],"spots":["阿波おどり会館","鳴門の渦潮","祖谷のかずら橋","大塚国際美術館"],"seasons":["春","夏","秋"],"themes":["祭り","絶景","雨の日","穴場"],"days":"1泊2日","transport":"徳島市と鳴門は公共交通、祖谷方面は車が現実的。","stay":"市内観光は徳島市、渦潮は鳴門、秘境感は祖谷。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/6/63/Awa-odori_2008_Tokushima_03.jpg","title":"Awa Odori","license":"CC BY-SA 2.0","artist":"Rosino"}},
    {"name":"香川県","slug":"kagawa","region":"四国","lead":"うどん、栗林公園、金刀比羅宮、直島を短い移動で楽しめる。","areas":["高松","琴平","小豆島","直島"],"spots":["栗林公園","金刀比羅宮","直島","父母ヶ浜"],"seasons":["春","夏","秋"],"themes":["グルメ","アート","車なし","島旅"],"days":"日帰りから1泊2日","transport":"高松を起点に鉄道・船で動きやすい。うどん巡りは車も便利。","stay":"初回は高松、参拝は琴平、アート旅は直島・小豆島。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/0/0b/Ritsurin.JPG","title":"Ritsurin Garden","license":"CC BY-SA 3.0","artist":"Leela Soden"}},
    {"name":"愛媛県","slug":"ehime","region":"四国","lead":"道後温泉、松山城、しまなみ海道、内子を組み合わせる温泉と歴史の県。","areas":["松山","道後","今治","内子"],"spots":["道後温泉","松山城","しまなみ海道","内子の町並み"],"seasons":["春","秋","冬"],"themes":["温泉","歴史","サイクリング","グルメ"],"days":"1泊2日から2泊3日","transport":"松山市内は路面電車が便利。しまなみ海道は自転車・車で計画。","stay":"温泉は道後、城と街歩きは松山市、海景色は今治。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/8/83/D%C5%8Dgo_Onsen.jpg","title":"Dogo Onsen","license":"CC BY 2.0","artist":"Arnaud Malon"}},
    {"name":"高知県","slug":"kochi","region":"四国","lead":"桂浜、四万十川、日曜市、カツオを軸に自然と食を楽しむ。","areas":["高知市","四万十","室戸","足摺"],"spots":["桂浜","高知城","ひろめ市場","四万十川"],"seasons":["春","夏","秋"],"themes":["グルメ","絶景","ドライブ","穴場"],"days":"1泊2日から2泊3日","transport":"高知市内は路面電車。四万十・足摺方面は車が便利。","stay":"食と街歩きは高知市、川旅は四万十、岬巡りは足摺。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/f/f3/Kochi_Katsurahama_Daytime_1.JPG","title":"Kochi Katsurahama","license":"CC BY-SA 3.0","artist":"京浜にけ"}},
    {"name":"福岡県","slug":"fukuoka","region":"九州","lead":"都市グルメ、太宰府、糸島、門司港を車なしでも回りやすい。","areas":["福岡市","太宰府","糸島","北九州"],"spots":["太宰府天満宮","中洲屋台","糸島","門司港レトロ"],"seasons":["春","秋","冬"],"themes":["グルメ","車なし","歴史","海"],"days":"日帰りから1泊2日","transport":"地下鉄・西鉄・JRで主要地へ移動しやすい。糸島周遊は車も便利。","stay":"初回は博多・天神、門司港や小倉は北九州泊もあり。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/8/8b/20100719_Dazaifu_Tenmangu_Shrine_3328.jpg","title":"Dazaifu Tenmangu Shrine","license":"CC BY-SA 4.0","artist":"Jakub Halun"}},
    {"name":"佐賀県","slug":"saga","region":"九州","lead":"有田・伊万里の焼き物、嬉野温泉、吉野ヶ里を静かに巡る穴場県。","areas":["佐賀市","嬉野","有田","唐津"],"spots":["吉野ヶ里歴史公園","嬉野温泉","有田焼の里","唐津城"],"seasons":["春","秋","冬"],"themes":["温泉","歴史","工芸","穴場"],"days":"日帰りから1泊2日","transport":"鉄道とバスで主要地へ。焼き物の里を細かく巡るなら車。","stay":"温泉は嬉野、焼き物旅は有田・伊万里、海沿いは唐津。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/c/c2/Yoshinogari_Historical_Park_Center_20230312_02.jpg","title":"Yoshinogari Historical Park","license":"CC BY-SA 4.0","artist":"Peka"}},
    {"name":"長崎県","slug":"nagasaki","region":"九州","lead":"異国情緒、夜景、教会群、島旅を組み合わせる歴史と港町の県。","areas":["長崎市","佐世保","雲仙","五島"],"spots":["グラバー園","稲佐山","ハウステンボス","雲仙温泉"],"seasons":["春","秋","冬"],"themes":["歴史","夜景","温泉","島旅"],"days":"1泊2日から3泊4日","transport":"長崎市内は路面電車が便利。五島や壱岐対馬は船・飛行機を別計画で。","stay":"初回は長崎市、家族旅は佐世保、温泉は雲仙。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/0/05/Nagasaki%2C_viewed_from_Mount_Inasayama%3B_January_2013.jpg","title":"Nagasaki from Mount Inasayama","license":"CC BY 2.0","artist":"Konstantin Leonov"}},
    {"name":"熊本県","slug":"kumamoto","region":"九州","lead":"熊本城、阿蘇、黒川温泉、天草を自然と温泉で展開できる。","areas":["熊本市","阿蘇","黒川","天草"],"spots":["熊本城","阿蘇山","草千里","黒川温泉"],"seasons":["春","夏","秋"],"themes":["絶景","温泉","歴史","ドライブ"],"days":"1泊2日から2泊3日","transport":"市内は路面電車。阿蘇・黒川・天草は車が強い。","stay":"歴史は熊本市、絶景と温泉は阿蘇・黒川。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/7/7c/Kumamoto_Castle_02n3200.jpg","title":"Kumamoto Castle","license":"CC BY 2.5","artist":"663highland"}},
    {"name":"大分県","slug":"oita","region":"九州","lead":"別府、由布院、国東半島を温泉とアート、自然で組み合わせる。","areas":["別府","由布院","大分市","国東"],"spots":["別府地獄めぐり","由布院温泉","宇佐神宮","九重夢大吊橋"],"seasons":["春","秋","冬"],"themes":["温泉","絶景","雨の日","ドライブ"],"days":"1泊2日から2泊3日","transport":"別府・由布院は鉄道でも可能。九重・国東は車が便利。","stay":"湯めぐりは別府、静かな滞在は由布院。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/f/f7/Beppu_station_Onsen_2024.jpg","title":"Beppu station Onsen","license":"CC BY-SA 4.0","artist":"Smiley.toerist"}},
    {"name":"宮崎県","slug":"miyazaki","region":"九州","lead":"青島、日南海岸、高千穂を晴天ドライブで巡る南国感のある県。","areas":["宮崎市","日南","高千穂","えびの"],"spots":["青島神社","鵜戸神宮","高千穂峡","都井岬"],"seasons":["春","夏","秋"],"themes":["絶景","神社","ドライブ","穴場"],"days":"1泊2日から2泊3日","transport":"日南海岸や高千穂はレンタカー向き。宮崎市周辺はバスも利用可。","stay":"海沿いは宮崎市・青島、高千穂は別泊にすると余裕が出る。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/2/2b/Takachiho-gorge.jpg","title":"Takachiho Gorge","license":"CC BY 2.5","artist":"Takasunrise0921"}},
    {"name":"鹿児島県","slug":"kagoshima","region":"九州","lead":"桜島、霧島、指宿、屋久島・奄美まで火山と島旅を展開できる。","areas":["鹿児島市","霧島","指宿","屋久島"],"spots":["桜島","仙巌園","霧島神宮","指宿砂むし温泉"],"seasons":["春","夏","秋"],"themes":["温泉","絶景","島旅","歴史"],"days":"1泊2日から4泊5日","transport":"鹿児島市と桜島は船で便利。霧島・指宿・島旅は日程を分ける。","stay":"初回は鹿児島市、温泉は霧島・指宿、自然は屋久島・奄美。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/5/5c/Sakurajima55.jpg","title":"Sakurajima","license":"CC BY 3.0","artist":"TANAKA Juuyoh"}},
    {"name":"沖縄県","slug":"okinawa","region":"沖縄","lead":"本島、宮古、石垣、西表を海・文化・自然で分けて計画するリゾート県。","areas":["那覇","恩納村","宮古島","石垣島"],"spots":["首里城公園","美ら海水族館","古宇利島","川平湾"],"seasons":["春","夏","冬"],"themes":["海","子連れ","島旅","ドライブ"],"days":"2泊3日から4泊5日","transport":"本島北部や離島は車が便利。那覇市内はゆいレールを活用。","stay":"初回は那覇と恩納村、離島は宮古島・石垣島を単独で組む。","image":{"url":"https://upload.wikimedia.org/wikipedia/commons/9/98/Naha_Okinawa_Japan_Shuri-Castle-02.jpg","title":"Shuri Castle","license":"CC BY-SA 3.0","artist":"CEphoto, Uwe Aranas"}},
]

# ─── Airport Code Mapping ─────────────────────────────────────────────────────

AIRPORT = {
    "hokkaido": "CTS",
    "aomori": "AOJ",
    "iwate": "HNA",
    "miyagi": "SDJ",
    "akita": "AXT",
    "yamagata": "GAJ",
    "fukushima": "FKS",
    "ibaraki": "IBR",
    "tochigi": "NRT",
    "gunma": "NRT",
    "saitama": "NRT",
    "chiba": "NRT",
    "tokyo": "HND",
    "kanagawa": "HND",
    "niigata": "KIJ",
    "toyama": "TOY",
    "ishikawa": "KMQ",
    "fukui": "KMQ",
    "yamanashi": "NRT",
    "nagano": "NGO",
    "gifu": "NGO",
    "shizuoka": "FSZ",
    "aichi": "NGO",
    "mie": "KIX",
    "shiga": "KIX",
    "kyoto": "KIX",
    "osaka": "KIX",
    "hyogo": "KIX",
    "nara": "KIX",
    "wakayama": "KIX",
    "tottori": "TTJ",
    "shimane": "IZO",
    "okayama": "OKJ",
    "hiroshima": "HIJ",
    "yamaguchi": "UBJ",
    "tokushima": "TKS",
    "kagawa": "TAK",
    "ehime": "MYJ",
    "kochi": "KCZ",
    "fukuoka": "FUK",
    "saga": "HSG",
    "nagasaki": "NGS",
    "kumamoto": "KMJ",
    "oita": "OIT",
    "miyazaki": "KMI",
    "kagoshima": "KOJ",
    "okinawa": "OKA",
}

# ─── Course Generator ─────────────────────────────────────────────────────────

def find_spot(spots, pattern):
    for s in spots:
        if re.search(pattern, s):
            return s
    return spots[0]


def generate_courses(p):
    areas = p["areas"]
    spots = p["spots"]
    themes = p["themes"]
    seasons = p["seasons"]

    first_season = seasons[0] if seasons else "春"
    best_theme = themes[0] if themes else "観光"
    second_theme = themes[1] if len(themes) > 1 else best_theme
    quiet_area = areas[2] if len(areas) > 2 else areas[0]
    food_area = areas[1] if len(areas) > 1 else areas[0]
    family_spot = find_spot(spots, r"公園|水族館|動物園|博物館|市場|城")
    culture_spot = find_spot(spots, r"城|寺|神社|大社|宮|跡|町並|園")
    scenic_spot = find_spot(spots, r"山|湖|海|島|峡|滝|岬|橋|丘|浜|湾")
    indoor_spot = spots[3] if ("雨の日" in themes and len(spots) > 3) else find_spot(spots, r"館|市場|城|寺|神社|温泉|公園")
    spot1 = spots[0]
    spot2 = spots[1] if len(spots) > 1 else areas[1] if len(areas) > 1 else areas[0]
    spot3 = spots[2] if len(spots) > 2 else spot1
    spot4 = spots[3] if len(spots) > 3 else spot1

    if "温泉" in themes:
        local_angle = "温泉滞在"
    elif "島旅" in themes:
        local_angle = "島旅"
    elif "祭り" in themes:
        local_angle = "祭りと町歩き"
    elif "アート" in themes:
        local_angle = "アート散策"
    elif "グルメ" in themes:
        local_angle = "ご当地グルメ"
    else:
        local_angle = f"{best_theme}深掘り"

    no_car = "車なし" in themes
    transport_title = "車なしで回る公共交通コース" if no_car else "レンタカーで巡るドライブコース"
    if no_car:
        transport_steps = [
            f"{areas[0]}の駅周辺に到着",
            f"{spot1}を中心に徒歩と公共交通で観光",
            f"{spot2}へ移動し、食事と街歩き",
            f"{areas[0]}へ戻り、宿泊または帰路へ",
        ]
    else:
        transport_steps = [
            f"{areas[0]}でレンタカーを借りる",
            f"{spot1}から{spot2}へ",
            f"昼は{food_area}周辺で休憩",
            f"{spot3}まで足を伸ばして宿泊地へ",
        ]

    transport_id = "without-car" if no_car else "drive"
    transport_label = "車なし" if no_car else "ドライブ"

    return [
        {
            "id": "seasonal",
            "title": f"{first_season}に行きたい季節満喫コース",
            "label": "季節",
            "summary": f"{p['name']}の{first_season}らしい景色と定番スポットを無理なくつなぐ初回向けコースです。",
            "point": f"{spot1}を午前に入れると、写真を撮りやすく混雑も避けやすくなります。",
            "transport": p["transport"],
            "lodging": p["stay"],
            "steps": [
                f"{areas[0]}を午前中に出発",
                f"{spot1}で{first_season}らしい景色を楽しむ",
                f"{spot2}で昼食と散策",
                p["stay"],
            ],
        },
        {
            "id": "family",
            "title": "家族向けゆったりコース",
            "label": "家族",
            "summary": f"移動距離を抑え、休憩と食事の時間を多めに取る{p['name']}の家族旅行向けコースです。",
            "point": f"{family_spot}を中心にすると、子どものペースに合わせて滞在時間を調整しやすくなります。",
            "transport": f"ベビーカーや荷物が多い場合はタクシー・レンタカーも選択肢。基本方針は、{p['transport']}",
            "lodging": f"荷物移動を減らせる{areas[0]}周辺、または{p['stay']}",
            "steps": [
                f"移動距離を短めにして{areas[0]}から開始",
                f"{family_spot}で滞在時間を長めに取る",
                f"{areas[1] if len(areas)>1 else areas[0]}で早めの夕食",
                "宿泊は荷物移動が少ないエリアを選ぶ",
            ],
        },
        {
            "id": "solo",
            "title": "一人旅で深く歩くコース",
            "label": "一人旅",
            "summary": f"写真、歴史、ローカルグルメを自分のペースで楽しむ{p['name']}の一人旅コースです。",
            "point": f"{quiet_area}を起点にすると、混みやすい定番地だけでなく落ち着いたエリアも見つけやすくなります。",
            "transport": f"徒歩時間を多めに取りつつ、長距離は公共交通を使います。{p['transport']}",
            "lodging": f"夜の移動を短くするため、{areas[0]}か{quiet_area}周辺が便利です。",
            "steps": [
                f"{quiet_area}を起点に午前の散策",
                f"{spot3}で写真や歴史をじっくり楽しむ",
                "カフェや市場で地元の食を試す",
                f"夕方は{spot4}へ寄って余裕を持って戻る",
            ],
        },
        {
            "id": transport_id,
            "title": transport_title,
            "label": transport_label,
            "summary": f"{p['name']}の移動条件に合わせて、主要スポットを効率よくつなぐ実用コースです。",
            "point": (
                f"{areas[0]}を起点にすると、乗り換えと荷物移動を減らせます。"
                if no_car
                else f"{spot1}から{spot2}へ進むと、景色と食事のリズムを作りやすいです。"
            ),
            "transport": (
                f"鉄道・バス・徒歩を基本にします。時刻表確認を前提に、{p['transport']}"
                if no_car
                else f"レンタカー利用を想定します。夕方の運転を短くするため、宿泊地は最後の訪問地に寄せます。"
            ),
            "lodging": p["stay"],
            "steps": transport_steps,
        },
        {
            "id": "rainy",
            "title": "雨の日・予定変更コース",
            "label": "雨の日",
            "summary": f"天候が崩れても旅程を崩しにくい、屋内・滞在型スポット中心の{p['name']}コースです。",
            "point": f"{indoor_spot}を先に押さえると、雨でも満足度を保ちやすくなります。",
            "transport": f"屋外移動を短くするため、{areas[0]}周辺を中心に組みます。{p['transport']}",
            "lodging": f"雨天時は駅や中心市街地に近い宿が便利です。{p['stay']}",
            "steps": [
                f"屋内や滞在型の{indoor_spot}を中心にする",
                f"{areas[0]}周辺で移動時間を短縮",
                f"{best_theme}に関係する食事・買い物・温泉を組み合わせる",
                f"晴れ間が出たら{spot1}へ短時間だけ立ち寄る",
            ],
        },
        {
            "id": "local-theme",
            "title": f"{local_angle}を深く楽しむコース",
            "label": "県らしさ",
            "summary": f"{p['name']}ならではの{local_angle}を中心に、定番観光より一歩深く楽しむコースです。",
            "point": f"{'・'.join(themes)}の中でも{best_theme}を主軸にすると、{p['name']}らしい旅の理由がはっきりします。",
            "transport": f"{areas[0]}を起点に、{spot1}と{spot2}を無理なくつなぎます。{p['transport']}",
            "lodging": f"{local_angle}を楽しむなら、{p['stay']}",
            "steps": [
                f"{areas[0]}で旅のテーマを確認",
                f"{spot1}で{best_theme}を体感",
                f"{spot2}で地域の空気を味わう",
                f"{food_area}周辺に泊まって余韻を残す",
            ],
        },
        {
            "id": "gourmet",
            "title": "ご当地グルメと市場・町歩きコース",
            "label": "グルメ",
            "summary": f"{p['name']}の食事、買い物、町歩きを観光の中心にした、移動負担が少ないコースです。",
            "point": f"{food_area}周辺に昼食時間を合わせると、食事と休憩を自然に組み込めます。",
            "transport": f"食事時間を軸に、徒歩・公共交通・短距離移動を組み合わせます。{p['transport']}",
            "lodging": f"夕食の選択肢を重視するなら{areas[0]}周辺、落ち着き重視なら{food_area}周辺が候補です。",
            "steps": [
                f"{areas[0]}で朝または昼の食事スポットを探す",
                f"{spot2}へ移動して散策",
                f"{food_area}周辺でカフェ・市場・土産店を回る",
                "夜は宿泊地で地元料理をゆっくり楽しむ",
            ],
        },
        {
            "id": "history-culture",
            "title": "歴史・文化をたどる学び旅コース",
            "label": "歴史文化",
            "summary": f"{p['name']}の寺社、城、町並み、文化施設をつなぎ、土地の背景が分かるコースです。",
            "point": f"{culture_spot}を最初に見ると、後に続く町歩きや食事にも地域の文脈が生まれます。",
            "transport": f"徒歩で見られる範囲を中心にし、離れた文化スポットは公共交通か車で補います。{p['transport']}",
            "lodging": f"歴史散策を重視するなら、朝の徒歩移動がしやすい{areas[0]}または{areas[1] if len(areas)>1 else areas[0]}周辺が便利です。",
            "steps": [
                f"{culture_spot}を午前に見学",
                f"{areas[0]}周辺で町歩き",
                f"{spot3}で歴史や文化を補足",
                "夕方は宿の近くで余裕を持って食事",
            ],
        },
        {
            "id": "scenic-photo",
            "title": "絶景写真と夕景を狙うコース",
            "label": "写真",
            "summary": f"{p['name']}の景色を写真で残したい人向けに、光の良い時間帯を意識したコースです。",
            "point": f"{scenic_spot}は天気と時間帯で印象が変わるため、移動に余白を作るのが大切です。",
            "transport": f"撮影時間を確保するため、移動先を絞ります。広域移動が必要な場合はレンタカーも検討します。{p['transport']}",
            "lodging": f"夕景や朝景を狙うなら、{scenic_spot}に近いエリアか{p['stay']}",
            "steps": [
                f"午前は{areas[0]}で移動を整える",
                f"昼前後に{scenic_spot}へ向かう",
                f"{spot2}で休憩しながら天候待ち",
                "夕方に景色の良い場所へ戻る",
            ],
        },
        {
            "id": "hidden-gems",
            "title": "混雑を避ける穴場・ゆったりコース",
            "label": "穴場",
            "summary": f"混みやすい定番だけに寄せず、{p['name']}を落ち着いて楽しむための余白重視コースです。",
            "point": f"{quiet_area}を入れると、観光地巡りだけでは見えにくい地域の日常や静かな景色に触れられます。",
            "transport": f"混雑回避のため朝は早めに動き、午後は移動距離を短くします。{p['transport']}",
            "lodging": f"静かに過ごしたい場合は中心地から少し離れた宿、利便性重視なら{areas[0]}周辺が向きます。",
            "steps": [
                f"朝早く{spot1}へ",
                f"昼は{quiet_area}周辺へ移動",
                f"{spot4}で短時間の立ち寄り",
                "早めに宿へ入り、夕方をゆっくり過ごす",
            ],
        },
    ]

# ─── Markdown Generator ───────────────────────────────────────────────────────

def yaml_str(s):
    s = str(s)
    if any(c in s for c in [':', '#', '[', ']', '{', '}', '*', '&', '!', '|', '>', "'", '"', '\n']):
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def yaml_list(lst):
    return "[" + ", ".join(yaml_str(x) for x in lst) + "]"


def write_prefecture_page(p, out_dir):
    slug = p["slug"]
    airport = AIRPORT.get(slug, "TYO")
    courses = generate_courses(p)

    # Build courses YAML block
    courses_yaml = ""
    for c in courses:
        steps_yaml = yaml_list(c["steps"])
        courses_yaml += f"""  - id: {c['id']}
    title: {yaml_str(c['title'])}
    label: {yaml_str(c['label'])}
    summary: {yaml_str(c['summary'])}
    point: {yaml_str(c['point'])}
    transport: {yaml_str(c['transport'])}
    lodging: {yaml_str(c['lodging'])}
    steps: {steps_yaml}
"""

    areas_yaml = yaml_list(p["areas"])
    spots_yaml = yaml_list(p["spots"])
    seasons_yaml = yaml_list(p["seasons"])
    themes_yaml = yaml_list(p["themes"])

    frontmatter = f"""---
title: {yaml_str(p['name'] + '観光モデルコース10選')}
description: {yaml_str(p['lead'])}
date: "2026-05-03"
prefecture: {yaml_str(p['name'])}
prefecture_slug: {slug}
region: {yaml_str(p['region'])}
areas: {areas_yaml}
spots: {spots_yaml}
seasons: {seasons_yaml}
themes: {themes_yaml}
days: {yaml_str(p['days'])}
transport: {yaml_str(p['transport'])}
stay: {yaml_str(p['stay'])}
airport: {airport}
image_url: {yaml_str(p['image']['url'])}
image_title: {yaml_str(p['image']['title'])}
image_license: {yaml_str(p['image']['license'])}
image_artist: {yaml_str(p['image']['artist'])}
courses:
{courses_yaml}---
"""

    # Markdown body: intro text (the template will render courses)
    body = f"""{p['lead']}

{p['name']}の旅行プランを目的別・旅スタイル別に10コース紹介します。定番からローカルまで、宿泊先や移動手段の選び方も合わせて解説しています。

## 基本情報

| 項目 | 内容 |
|------|------|
| 地方 | {p['region']} |
| 推奨日程 | {p['days']} |
| おすすめ季節 | {'・'.join(p['seasons'])} |
| 主なテーマ | {'・'.join(p['themes'])} |
| 交通 | {p['transport']} |
| 宿泊の目安 | {p['stay']} |

## 主なエリアとスポット

**エリア：** {'、'.join(p['areas'])}

**代表スポット：** {'、'.join(p['spots'])}
"""

    content = frontmatter + "\n" + body
    path = os.path.join(out_dir, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}")


def write_index_page(out_dir, site_params):
    regions_order = ["北海道","東北","関東","中部","近畿","中国","四国","九州","沖縄"]
    region_map = {}
    for p in PREFECTURES:
        region_map.setdefault(p["region"], []).append(p)

    body_lines = [
        "日本全国47都道府県の観光モデルコースをまとめました。地方別に絞り込んで探せます。\n"
    ]
    for region in regions_order:
        prefs = region_map.get(region, [])
        if not prefs:
            continue
        body_lines.append(f"\n## {region}\n")
        for p in prefs:
            body_lines.append(f"- [{p['name']}観光モデルコース10選]({{{{< relref \"{p['slug']}\" >}}}})")

    body = "\n".join(body_lines)

    content = f"""---
title: "日本観光コースガイド｜47都道府県まとめ"
description: "北海道から沖縄まで47都道府県の観光モデルコースを紹介。家族旅・一人旅・温泉・グルメなど目的別に選べます。"
date: "2026-05-03"
---

{body}
"""
    path = os.path.join(out_dir, "_index.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, "content", "japan")
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating japan pages → {out_dir}")
    write_index_page(out_dir, {})
    for p in PREFECTURES:
        write_prefecture_page(p, out_dir)
    print(f"\nDone: {len(PREFECTURES)} prefecture pages + 1 index")


if __name__ == "__main__":
    main()
