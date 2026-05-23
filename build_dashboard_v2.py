import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\泰国市场重点分析\processed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(r'E:\泰国市场重点分析\translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

def clean_title(zh):
    if not zh:
        return '美妆产品'
    # 1. 去除泰文字符
    zh = re.sub(r'[\u0e00-\u0e7f]+', '', zh)
    # 2. 去掉emoji
    zh = re.sub(r'[\U00010000-\U0010ffff]', '', zh, flags=re.UNICODE)
    zh = re.sub(r'[❗️💓✨🔥🌸]+', '', zh)
    # 3. 去掉直播/促销前缀词
    zh = re.sub(r'True/True/Live\s*[（(][^）)]*[）)]?\s*', '', zh)
    zh = re.sub(r'True/True/Live\s*', '', zh)
    zh = re.sub(r'准备发货\s*', '', zh)
    # 4. 去掉括号内的促销词（件数、买赠、折扣）
    zh = re.sub(r'[（(]\s*\d+\s*[件个包袋][）)]\s*', '', zh)
    zh = re.sub(r'[（(]\s*买\d+送\d+[）)]\s*', '', zh)
    zh = re.sub(r'[（(]\s*\d+\s*%\s*[^）)]*[）)]\s*', '', zh)
    zh = re.sub(r'[（(]\s*\d+件\s*\d+[^）)]*[）)]\s*', '', zh)
    # 5. 去掉方括号促销词
    zh = re.sub(r'\[销量第一[^\]]*\]', '', zh)
    zh = re.sub(r'\[特价[^\]]*\]', '', zh)
    zh = re.sub(r'\[唇垫\d+小时\*?\]', '', zh)
    zh = re.sub(r'\[[^\]]{0,8}Pick\]', '', zh)
    zh = re.sub(r'\[官方商店\]', '', zh)
    zh = re.sub(r'\[尺寸\d+克\]', '', zh)
    # 6. 按分隔符截取第一段（取最有信息量的）
    for sep in ['|', '｜']:
        if sep in zh:
            zh = zh.split(sep)[0].strip()
    # 7. 去掉句号后内容
    if '。' in zh:
        zh = zh.split('。')[0]
    # 8. 去掉机翻重复：找中文后重复的英文尾巴
    # 例如"美宝莲Super Stay乙烯基墨水唇膏美宝莲Super Stay乙烯基Inc唇膏" 
    # -> 检测重复的前N个字符
    if len(zh) > 20:
        half = len(zh) // 2
        first_half = zh[:half]
        if first_half.lower() in zh[half:].lower():
            zh = zh[:half + 5]  # 只保留前半段
    # 9. 去掉尾部多余的英文模型号和规格
    zh = re.sub(r'\s+[A-Z]{2,}[0-9]+\s*$', '', zh).strip()
    # 10. 空格清理
    zh = re.sub(r'\s{2,}', ' ', zh).strip()
    zh = zh.strip(' ,，、！!。.·-—')
    if len(zh) > 50:
        # 在第48字符处找最近的中文字符位置截断
        cut = 48
        while cut > 30 and not ('\u4e00' <= zh[cut] <= '\u9fff'):
            cut -= 1
        zh = zh[:cut] + '…'
    return zh if len(zh) > 1 else '美妆产品'

def fmt_price(p):
    """将 ฿235 转换为 HTML安全的 &#3647;235"""
    return p.replace('฿', '&#3647;')

icons = {'唇部':'&#128132;','粉底':'&#129803;','腮红':'&#127800;','睫毛膏':'&#128065;','遮瑕':'&#10024;','定妆喷雾':'&#128168;'}
icons_txt = {'唇部':'💄','粉底':'🫙','腮红':'🌸','睫毛膏':'👁','遮瑕':'✨','定妆喷雾':'💨'}

# === 品类洞察数据 ===
INSIGHTS = {
    '唇部': {
        'summary': '果冻胶感与哑光墨水是两大主流质地，高折扣（-77%~-99%）超低价产品带动销量爆发，本土及国际品牌均有斩获。',
        'tags': [
            ('质地', ['哑光液体唇膏','果冻染色','乙烯基墨水','唇彩油','光泽唇膏']),
            ('功效', ['持久不脱色','防水','16h持久','滋润保湿','不沾杯']),
            ('价位带', ['฿1-79（超值引流）','฿159-236（主流）','฿309-422（高端）']),
            ('热门品牌', ['MAYBELLINE','hince','4U2','L\'Oreal','KATE','Cathy Doll']),
        ],
        'insight': '泰国消费者偏好高折扣+哑光/果冻质感，本土品牌4U2、Cathy Doll以超低价策略占据榜单；国际品牌美宝莲依靠16h持久技术稳居前列。',
        'hotwords': ['哑光','防水','持久','果冻感','显色'],
    },
    '粉底': {
        'summary': '哑光粉底液占主导，SPF防晒+持久持妆是核心卖点；SUPERMOM单品月销60k+领跑全场，价格带分布宽泛。',
        'tags': [
            ('质地', ['哑光雾感','轻薄水润','软雾finish','BB霜','矿物质粉底']),
            ('功效', ['SPF50+防晒','32小时持妆','PA++++','遮瑕控油','保湿透气']),
            ('价位带', ['฿1-90（引流款）','฿119-165（平价）','฿439-560（高端）']),
            ('热门品牌', ['SUPERMOM','PALA','L\'Oreal','SRICHAND','Chaonang','Music Flower']),
        ],
        'insight': '泰国高温高湿气候推动"持妆控油"强需求，SPF50+防晒功能成为标配；SUPERMOM本土品牌凭借哑光雾感+平价策略月销60k+，欧莱雅32H卖点精准契合需求。',
        'hotwords': ['持妆','SPF50','哑光雾感','控油','防水'],
    },
    '腮红': {
        'summary': '腮红棒（膏状）崛起与防晒腮红为两大趋势；韩国品牌影响力强，价格带以中低价为主，高折扣引流普遍。',
        'tags': [
            ('质地', ['粉状腮红','奶油膏状腮红棒','液体腮红','镜面高光腮红','透明粉末']),
            ('功效', ['SPF50+防晒','防水持久','多用（唇颊眼）','自然提亮','哑光奶油感']),
            ('价位带', ['฿17-60（超值）','฿114-189（主流）','฿230+（高端）']),
            ('热门品牌', ['MizuMi','CANMAKE','LA GLACE','Sasi','SHAQINUO','ROM&ND']),
        ],
        'insight': '多用（唇/颊/眼）腮红棒是新兴增长点，SPF50+防晒腮红（MizuMi）月销30k+，说明防晒与彩妆结合的产品在泰国极具潜力；韩国小众品牌通过KOL引流效果显著。',
        'hotwords': ['多用一支','SPF防晒','奶油质地','防水','自然裸妆'],
    },
    '睫毛膏': {
        'summary': '防水防汗是核心刚需，睫毛膏与眉毛膏界限模糊；LA GLACE等本土品牌活跃，日本品牌KATE凭借精准眉形工具占领高端。',
        'tags': [
            ('质地', ['纤维加密','卷翘持久','纤细细刷头','浓密款','防水凝胶']),
            ('功效', ['防水防汗','24h持久','不沾污不结块','卷翘加密','细刷根根分明']),
            ('价位带', ['฿1-30（超值引流）','฿103-259（主流）','฿278-289（高端）']),
            ('热门品牌', ['LA GLACE','KATE','BROWIT','SUPERMOM','ZEESEA','bobaine']),
        ],
        'insight': '泰国高温多汗场景下防水睫毛膏是刚需，不结块+不晕染是核心痛点；睫毛膏与眉毛膏同品类竞争，KATE 3D眉毛膏以高价高评分证明专业品质溢价空间。',
        'hotwords': ['防水不晕','不结块','卷翘','持久24h','细刷头'],
    },
    '遮瑕': {
        'summary': '遮瑕+色彩矫正组合款受到热捧，BEAUTILAB桃色+蓝色矫正套组月销60k+领跑；哑光遮瑕是主流，功效叠加成趋势。',
        'tags': [
            ('质地', ['轻薄液体遮瑕','奶油膏状','哑光遮瑕','精华遮瑕','粉底遮瑕二合一']),
            ('功效', ['色彩矫正（桃色/蓝色）','遮黑眼圈','遮痘印/泛红','透气持妆','保湿亮肤']),
            ('价位带', ['฿1-39（引流款）','฿79-199（主流）','฿230（高端）']),
            ('热门品牌', ['BEAUTILAB','LA GLACE','Sasi','MEILINDA','YTL','OUKEYA']),
        ],
        'insight': '色彩矫正概念在泰国遮瑕品类引爆，BEAUTILAB桃色+蓝色矫正套组凭借¥1引流价月销60k+；LA GLACE透气精华遮瑕主打"遮而不厚重"切中热带肌肤痛点。',
        'hotwords': ['色彩矫正','遮黑眼圈','哑光','精华成分','透气轻薄'],
    },
    '定妆喷雾': {
        'summary': '锁妆+控油是核心功能，保湿Dewy与哑光Matte两种风格并存；价格极度分化，超值引流款（฿1-49）占据主要销量。',
        'tags': [
            ('质地', ['水雾型','矿泉水喷雾','闪光亮泽型','哑光控油型','珠光保湿']),
            ('功效', ['锁妆持久12h','控油防脱妆','保湿补水','防水抗汗','提亮发光']),
            ('价位带', ['฿1-49（超值）','฿149-215（中端）','฿300+（高端）']),
            ('热门品牌', ['VIVX','LAMEILA','PALA','Pramy','CUTE PRESS','Dazzle Me']),
        ],
        'insight': '定妆喷雾是泰国彩妆日常必备，Dewy水润感与哑光控油感各有受众；VIVX以60ml大容量+50%折扣策略月销20k+，突显性价比导向消费心理；珠光矿泉水喷雾兼具护肤属性在泰国有独特增长空间。',
        'hotwords': ['锁妆12h','控油','Dewy发光','矿泉水雾','防水抗汗'],
    },
}
colors = {
    '唇部':   {'main':'#E8506A','light':'#FFF0F2','mid':'#FFD6DC','text':'#C0384F'},
    '粉底':   {'main':'#E07B3A','light':'#FFF5EE','mid':'#FFE5CE','text':'#B85F20'},
    '腮红':   {'main':'#D4548A','light':'#FFF0F7','mid':'#FFD6EC','text':'#B03570'},
    '睫毛膏': {'main':'#5B6FAB','light':'#F0F3FF','mid':'#D6DDFF','text':'#3D4F8C'},
    '遮瑕':   {'main':'#B07A3E','light':'#FDF5E8','mid':'#F5E0B8','text':'#8A5D25'},
    '定妆喷雾':{'main':'#3DA8C4','light':'#EFF9FC','mid':'#C4EBF5','text':'#1E7E9A'},
}

lines = []

# ===================== CSS =====================
lines.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泰国Shopee美妆热销产品看板</title>
<style>
:root{
  --bg:#F7F8FC;
  --white:#FFFFFF;
  --gray1:#F2F4F8;
  --gray2:#E8EBF2;
  --gray3:#C4C9D8;
  --text:#1A1D2E;
  --text2:#555B73;
  --text3:#8A90A8;
  --shopee:#EE4D2D;
  --gold:#E8A020;
  --shadow:0 2px 12px rgba(30,40,80,0.08);
  --shadow-hover:0 8px 32px rgba(30,40,80,0.14);
  --radius:14px;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Microsoft YaHei','PingFang SC','Noto Sans SC',-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}

/* HEADER */
.header{
  background:linear-gradient(135deg,#fff 0%,#FFF5F7 100%);
  border-bottom:1px solid #F0D0D8;
  padding:18px 40px;
  display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:100;
  box-shadow:0 2px 16px rgba(220,80,100,0.07);
}
.header-brand{display:flex;align-items:center;gap:14px;}
.shopee-pill{
  background:var(--shopee);color:white;
  font-size:11px;font-weight:700;padding:4px 12px;
  border-radius:20px;letter-spacing:1px;
}
.header h1{
  font-size:20px;font-weight:800;
  background:linear-gradient(90deg,#E8506A,#D4548A);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.header-sub{font-size:12px;color:var(--text3);margin-top:2px;}
.header-stats{display:flex;gap:28px;}
.hstat{text-align:center;}
.hstat .v{font-size:22px;font-weight:800;color:var(--shopee);}
.hstat .l{font-size:11px;color:var(--text3);margin-top:1px;}

/* TABS */
.tabs-wrap{
  background:var(--white);
  border-bottom:2px solid var(--gray2);
  padding:0 40px;
  position:sticky;top:71px;z-index:99;
  box-shadow:0 2px 8px rgba(0,0,0,0.04);
}
.tabs{display:flex;overflow-x:auto;scrollbar-width:none;}
.tabs::-webkit-scrollbar{display:none;}
.tab{
  padding:14px 20px;cursor:pointer;
  font-size:14px;font-weight:600;color:var(--text3);
  white-space:nowrap;border-bottom:2px solid transparent;
  margin-bottom:-2px;transition:all 0.2s;
  display:flex;align-items:center;gap:6px;
}
.tab:hover{color:var(--text2);}
.tab.active{color:var(--shopee);border-bottom-color:var(--shopee);}
.tab-badge{
  font-size:10px;font-weight:700;padding:1px 7px;border-radius:10px;
  background:#FFF0F2;color:var(--shopee);
}

/* CONTENT */
.content{padding:28px 40px;}
.panel{display:none;}
.panel.active{display:block;}

/* STAT CARDS */
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:24px;}
.scard{
  background:var(--white);border-radius:var(--radius);
  padding:18px 20px;
  box-shadow:var(--shadow);
  border:1px solid var(--gray2);
  position:relative;overflow:hidden;
}
.scard-accent{position:absolute;top:0;left:0;right:0;height:3px;border-radius:var(--radius) var(--radius) 0 0;}
.scard .ico{font-size:20px;margin-bottom:6px;}
.scard .v{font-size:24px;font-weight:800;color:var(--text);}
.scard .l{font-size:11px;color:var(--text3);margin-top:3px;}

/* SECTION TITLE */
.sec-title{display:flex;align-items:center;gap:12px;margin-bottom:18px;}
.sec-title h2{font-size:17px;font-weight:700;color:var(--text);}
.sec-title .line{flex:1;height:1px;background:var(--gray2);}
.sec-tag{font-size:11px;color:var(--text3);background:var(--gray1);border:1px solid var(--gray2);padding:3px 10px;border-radius:20px;}

/* VIEW TOGGLE */
.view-toggle{display:flex;gap:6px;justify-content:flex-end;margin-bottom:18px;}
.vbtn{
  padding:6px 16px;border-radius:20px;
  border:1px solid var(--gray2);background:var(--white);
  color:var(--text3);font-size:12px;font-weight:600;cursor:pointer;transition:all 0.2s;
}
.vbtn.active,.vbtn:hover{
  background:#FFF0F2;border-color:#FFB8C4;color:var(--shopee);
}

/* PRODUCT GRID */
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;}

.pcard{
  background:var(--white);border-radius:var(--radius);
  border:1px solid var(--gray2);
  overflow:hidden;transition:all 0.25s;
  position:relative;
  box-shadow:var(--shadow);
}
.pcard:hover{
  transform:translateY(-4px);
  box-shadow:var(--shadow-hover);
  border-color:var(--gray3);
}

/* rank */
.rank-pin{
  position:absolute;top:10px;left:10px;z-index:10;
  width:26px;height:26px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:800;color:white;
}
.rk1{background:linear-gradient(135deg,#FFD700,#FFA500);box-shadow:0 2px 8px rgba(255,180,0,0.45);}
.rk2{background:linear-gradient(135deg,#CBD4E0,#9AAABB);}
.rk3{background:linear-gradient(135deg,#D4956A,#B06A40);}
.rkn{background:rgba(100,110,140,0.18);color:#666B88;font-size:10px;}

/* image */
.pimg-wrap{width:100%;height:195px;background:var(--gray1);overflow:hidden;position:relative;}
.pimg{width:100%;height:100%;object-fit:cover;transition:transform 0.3s;}
.pcard:hover .pimg{transform:scale(1.04);}
.pimg-ph{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:46px;background:linear-gradient(135deg,#FFF0F5,#FFF8F0);}
.disc-tag{
  position:absolute;top:10px;right:10px;
  background:var(--shopee);color:white;
  font-size:10px;font-weight:700;padding:3px 7px;border-radius:5px;
}

/* card body */
.pcard-body{padding:13px;}
.brand-line{display:flex;align-items:center;gap:6px;margin-bottom:7px;flex-wrap:wrap;}
.brand-pill{
  font-size:10px;font-weight:700;padding:2px 9px;border-radius:12px;
  white-space:nowrap;max-width:130px;overflow:hidden;text-overflow:ellipsis;
}
.promo-pill{
  font-size:10px;padding:2px 7px;border-radius:10px;
  background:#FFF8E8;color:#B07820;border:1px solid #F5E0A8;
  white-space:nowrap;max-width:80px;overflow:hidden;text-overflow:ellipsis;
}
.ptitle{
  font-size:12px;line-height:1.5;color:var(--text2);
  margin-bottom:10px;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
}
.price-big{font-size:17px;font-weight:800;color:var(--shopee);}
.metrics{display:flex;gap:10px;align-items:center;margin-top:6px;flex-wrap:wrap;}
.met{display:flex;align-items:center;gap:3px;font-size:11px;color:var(--text3);}
.met.star{color:#E8A020;font-weight:600;}
.met.sales{color:#3DA8C4;font-weight:600;}

/* TABLE */
.tbl-wrap{overflow-x:auto;border-radius:var(--radius);border:1px solid var(--gray2);background:var(--white);}
table{width:100%;border-collapse:collapse;font-size:13px;}
thead tr{background:var(--gray1);border-bottom:2px solid var(--gray2);}
th{padding:12px 14px;text-align:left;font-size:11px;font-weight:700;color:var(--text3);letter-spacing:0.4px;white-space:nowrap;}
tbody tr{border-bottom:1px solid var(--gray2);transition:background 0.15s;}
tbody tr:hover{background:var(--gray1);}
td{padding:10px 14px;vertical-align:middle;}
td.t-thumb img{width:46px;height:46px;object-fit:cover;border-radius:8px;border:1px solid var(--gray2);}
td.t-rank{font-size:13px;font-weight:800;text-align:center;width:40px;color:var(--text3);}
td.t-rank.top{color:var(--gold);}
td.t-price{color:var(--shopee);font-weight:700;}
td.t-sales{color:#3DA8C4;font-weight:600;}
td.t-rating{color:var(--gold);font-weight:600;}
td.t-disc{color:var(--shopee);font-weight:600;}
td.t-title{max-width:300px;}
td.t-title .tt{font-size:12px;color:var(--text);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4;}

/* OVERVIEW */
.ov-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
.ov-card{
  background:var(--white);border-radius:var(--radius);
  border:1px solid var(--gray2);padding:20px;
  cursor:pointer;transition:all 0.25s;
  box-shadow:var(--shadow);
}
.ov-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-hover);}
.ov-head{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.ov-emoji{font-size:30px;}
.ov-name{font-size:15px;font-weight:700;color:var(--text);}
.ov-count{font-size:11px;color:var(--text3);}
.ov-items{display:flex;flex-direction:column;gap:9px;}
.ov-item{display:flex;gap:10px;align-items:center;}
.ov-item img{width:42px;height:42px;object-fit:cover;border-radius:8px;border:1px solid var(--gray2);flex-shrink:0;}
.ov-item-info{flex:1;overflow:hidden;}
.ov-item-brand{font-size:10px;font-weight:700;margin-bottom:2px;}
.ov-item-title{font-size:11px;color:var(--text3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.ov-item-sales{font-size:11px;color:#3DA8C4;font-weight:600;margin-top:2px;}
.ov-item-price{font-size:12px;font-weight:700;color:var(--shopee);flex-shrink:0;}
.ov-divider{height:1px;background:var(--gray2);margin:12px 0;}
.ov-foot{display:flex;justify-content:space-between;font-size:11px;color:var(--text3);}
.ov-foot .fv{font-weight:700;color:var(--text2);}

/* INSIGHT BLOCK */
.insight-block{
  border-radius:16px;padding:20px 24px;margin-bottom:24px;
  border:1px solid var(--gray2);background:var(--white);
  box-shadow:var(--shadow);
}
.insight-header{display:flex;align-items:center;gap:10px;margin-bottom:16px;}
.insight-badge{
  font-size:11px;font-weight:700;letter-spacing:.5px;
  padding:3px 10px;border-radius:20px;color:#fff;
}
.insight-title{font-size:14px;font-weight:700;color:var(--text);}
.insight-summary{
  font-size:13px;color:var(--text2);line-height:1.7;
  padding:12px 14px;background:var(--gray1);border-radius:10px;
  margin-bottom:16px;border-left:3px solid currentColor;
}
.insight-rows{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:16px;}
.insight-row{background:var(--gray1);border-radius:10px;padding:12px 14px;}
.insight-row-label{font-size:10px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;margin-bottom:8px;opacity:.7;}
.insight-tags{display:flex;flex-wrap:wrap;gap:6px;}
.insight-tag{
  font-size:11px;padding:3px 10px;border-radius:20px;
  background:var(--white);border:1px solid var(--gray2);
  color:var(--text2);font-weight:500;
}
.insight-tag.hot{color:var(--shopee);border-color:rgba(238,77,45,0.3);background:rgba(238,77,45,0.06);}
.insight-tag.brand{font-weight:700;}
.hotword-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.hotword-label{font-size:11px;font-weight:700;color:var(--text3);flex-shrink:0;}
.hotword-chip{
  font-size:12px;padding:4px 12px;border-radius:20px;font-weight:600;
  color:#fff;display:inline-flex;align-items:center;gap:4px;
}
.insight-insight{
  font-size:12px;color:var(--text2);line-height:1.65;
  padding:10px 14px;border-radius:8px;margin-top:12px;
  background:linear-gradient(135deg,rgba(255,255,255,0.7),var(--gray1));
  border:1px solid var(--gray2);
}
.insight-insight::before{content:'💡 ';font-size:13px;}
@media(max-width:768px){.insight-rows{grid-template-columns:1fr;}}

/* FOOTER */
.footer{
  text-align:center;padding:24px;color:var(--text3);font-size:12px;
  border-top:1px solid var(--gray2);margin-top:40px;
  background:var(--white);
}

@media(max-width:768px){
  .header{padding:14px 16px;flex-wrap:wrap;gap:10px;}
  .content{padding:16px;}
  .tabs-wrap{padding:0 16px;}
  .stats-row{grid-template-columns:repeat(2,1fr);}
  .ov-grid{grid-template-columns:1fr;}
  .product-grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));}
}
</style>
</head>
<body>""")

# ===================== HEADER =====================
lines.append("""<div class="header">
<div class="header-brand">
<div style="font-size:30px">&#127481;&#127469;</div>
<div>
<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
<span class="shopee-pill">SHOPEE TH</span>
</div>
<h1>泰国美妆热销产品看板</h1>
<div class="header-sub">Thailand Beauty &middot; Bestseller Dashboard</div>
</div>
</div>
<div class="header-stats">
<div class="hstat"><div class="v">6</div><div class="l">热销品类</div></div>
<div class="hstat"><div class="v">120+</div><div class="l">热销产品</div></div>
<div class="hstat"><div class="v">60k+</div><div class="l">月最高销量</div></div>
</div>
</div>""")

# ===================== TABS =====================
t = ['<div class="tabs-wrap"><div class="tabs">']
t.append('<div class="tab active" onclick="switchTab(\'ov\')">&#128202; 总览</div>')
for cat in data:
    ic = {'唇部':'&#128132;','粉底':'&#129803;','腮红':'&#127800;','睫毛膏':'&#128065;','遮瑕':'&#10024;','定妆喷雾':'&#128168;'}.get(cat,'&#128132;')
    cnt = len(data[cat])
    t.append(f'<div class="tab" onclick="switchTab(\'{cat}\')">{ic} {cat} <span class="tab-badge">{cnt}</span></div>')
t.append('</div></div>')
lines.append(''.join(t))

lines.append('<div class="content">')

# ===================== OVERVIEW PANEL =====================
ov = ['<div class="panel active" id="panel-ov">']
ov.append("""<div class="stats-row">
<div class="scard"><div class="scard-accent" style="background:linear-gradient(90deg,#E8506A,#D4548A)"></div><div class="ico">&#127942;</div><div class="v">60k+</div><div class="l">月最高销量（粉底/遮瑕）</div></div>
<div class="scard"><div class="scard-accent" style="background:linear-gradient(90deg,#E8A020,#E07B3A)"></div><div class="ico">&#128176;</div><div class="v">&#3647;1~560</div><div class="l">热销价格区间（泰铢）</div></div>
<div class="scard"><div class="scard-accent" style="background:linear-gradient(90deg,#3DA8C4,#5B6FAB)"></div><div class="ico">&#11088;</div><div class="v">4.8-5.0</div><div class="l">热销产品评分区间</div></div>
<div class="scard"><div class="scard-accent" style="background:linear-gradient(90deg,#D4548A,#B07A3E)"></div><div class="ico">&#127991;</div><div class="v">-50%~-99%</div><div class="l">折扣力度范围</div></div>
</div>""")
ov.append('<div class="sec-title"><h2>各品类概览</h2><div class="line"></div><div class="sec-tag">点击卡片查看详情</div></div>')
ov.append('<div class="ov-grid">')

for cat, products in data.items():
    ic_txt = icons.get(cat,'💄')
    cl = colors.get(cat, {'main':'#E8506A','light':'#FFF0F2','mid':'#FFD6DC','text':'#C0384F'})
    top3 = products[:3]
    sales_vals = [p['sales_num'] for p in products if p['sales_num'] > 0]
    max_sales = max(sales_vals) if sales_vals else 0
    max_s = f'{max_sales//1000}k+' if max_sales >= 1000 else str(max_sales)
    blist = list(dict.fromkeys([p['brand'] for p in products if p['brand'] not in ('其他品牌','')]))[:3]
    bstr = ' &middot; '.join(blist) if blist else '多品牌'
    
    main_color = cl['main']
    cc = [f'<div class="ov-card" onclick="switchTab(\'{cat}\')" style="border-top:3px solid {main_color}">']
    cc.append(f'<div class="ov-head"><div class="ov-emoji">{ic_txt}</div><div><div class="ov-name">{cat}</div><div class="ov-count">Top {len(products)} 热销产品</div></div></div>')
    cc.append('<div class="ov-items">')
    for p in top3:
        zh_t = clean_title(translations.get(p['title'], p['title']))
        cc.append(f'<div class="ov-item"><img src="{p["img"]}" onerror="this.style.display=\'none\'"><div class="ov-item-info"><div class="ov-item-brand" style="color:{cl["text"]}">{p["brand"]}</div><div class="ov-item-title">{zh_t}</div><div class="ov-item-sales">&#128715; {p["sales"]}</div></div><div class="ov-item-price">{fmt_price(p["price"])}</div></div>')
    cc.append('</div>')
    cc.append('<div class="ov-divider"></div>')
    cc.append(f'<div class="ov-foot"><span>月最高: <span class="fv">{max_s}</span></span><span>品牌: <span class="fv">{bstr}</span></span></div>')
    cc.append('</div>')
    ov.append(''.join(cc))

ov.append('</div>')
ov.append('</div>')
lines.append(''.join(ov))

# ===================== CATEGORY PANELS =====================
for cat, products in data.items():
    ic_txt = icons.get(cat,'💄')
    cl = colors.get(cat, {'main':'#E8506A','light':'#FFF0F2','mid':'#FFD6DC','text':'#C0384F'})
    
    sales_vals = [p['sales_num'] for p in products if p['sales_num'] > 0]
    max_sales = max(sales_vals) if sales_vals else 0
    price_vals = [p['price_num'] for p in products if p['price_num'] > 0]
    avg_price = sum(price_vals)/len(price_vals) if price_vals else 0
    brands_all = list(dict.fromkeys([p['brand'] for p in products]))
    
    pp = [f'<div class="panel" id="panel-{cat}">']
    # stat row
    pp.append(f'<div class="stats-row">'
              f'<div class="scard"><div class="scard-accent" style="background:{cl["main"]}"></div><div class="ico">{ic_txt}</div><div class="v">{len(products)}</div><div class="l">热销产品数量</div></div>'
              f'<div class="scard"><div class="scard-accent" style="background:{cl["main"]}"></div><div class="ico">&#127942;</div><div class="v">{max_sales//1000}k+</div><div class="l">月最高销量</div></div>'
              f'<div class="scard"><div class="scard-accent" style="background:{cl["main"]}"></div><div class="ico">&#128176;</div><div class="v">&#3647;{avg_price:.0f}</div><div class="l">平均售价（泰铢）</div></div>'
              f'<div class="scard"><div class="scard-accent" style="background:{cl["main"]}"></div><div class="ico">&#127970;</div><div class="v">{len(brands_all)}</div><div class="l">品牌数量</div></div>'
              f'</div>')
    
    # === INSIGHT BLOCK ===
    ins = INSIGHTS.get(cat, {})
    if ins:
        tag_rows_html = ''
        for label, tags in ins.get('tags', []):
            tag_cls = 'brand' if label == '热门品牌' else ('hot' if label == '功效' else '')
            tags_html = ''.join(f'<span class="insight-tag {tag_cls}">{t}</span>' for t in tags)
            tag_rows_html += f'<div class="insight-row"><div class="insight-row-label" style="color:{cl["text"]}">{label}</div><div class="insight-tags">{tags_html}</div></div>'
        hotwords_html = ''.join(
            f'<span class="hotword-chip" style="background:{cl["main"]};opacity:{0.75+i*0.05:.2f}">#{w}</span>'
            for i, w in enumerate(ins.get('hotwords', []))
        )
        pp.append(
            f'<div class="insight-block">'
            f'<div class="insight-header">'
            f'<span class="insight-badge" style="background:{cl["main"]}">市场洞察</span>'
            f'<span class="insight-title">{cat}品类 · 消费趋势分析</span>'
            f'</div>'
            f'<div class="insight-summary" style="color:{cl["text"]};border-left-color:{cl["main"]}">{ins["summary"]}</div>'
            f'<div class="insight-rows">{tag_rows_html}</div>'
            f'<div class="hotword-row"><span class="hotword-label">热搜关键词</span>{hotwords_html}</div>'
            f'<div class="insight-insight">{ins["insight"]}</div>'
            f'</div>'
        )

    pp.append(f'<div class="view-toggle">'
              f'<button class="vbtn active" onclick="setView(\'{cat}\',\'grid\',this)">&#8862; 卡片视图</button>'
              f'<button class="vbtn" onclick="setView(\'{cat}\',\'table\',this)">&#9776; 列表视图</button>'
              f'</div>')
    
    pp.append(f'<div id="vt-{cat}" class="sec-title"><h2>{ic_txt} {cat} &middot; 热销 Top {len(products)}</h2><div class="line"></div><div class="sec-tag">按月销量排序</div></div>')
    
    # === GRID ===
    pp.append(f'<div id="grid-{cat}" class="product-grid">')
    for i, p in enumerate(products):
        rank = i + 1
        rk_cls = f'rk{rank}' if rank <= 3 else 'rkn'
        zh_t = clean_title(translations.get(p['title'], p['title']))
        t_esc = zh_t.replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
        disc_html = f'<div class="disc-tag">{p["discount"]}</div>' if p.get("discount") else ''
        promo_html = f'<span class="promo-pill">{p["promo"][:14]}</span>' if p.get("promo") else ''
        
        card = (
            f'<div class="pcard">'
            f'<div class="rank-pin {rk_cls}">#{rank}</div>'
            f'<div class="pimg-wrap">'
            f'<img class="pimg" src="{p["img"]}" alt="" onerror="this.parentNode.innerHTML=\'<div class=\\\'pimg-ph\\\'>{ic_txt}</div>\'">'
            f'{disc_html}'
            f'</div>'
            f'<div class="pcard-body">'
            f'<div class="brand-line">'
            f'<span class="brand-pill" style="background:{cl["light"]};color:{cl["text"]};border:1px solid {cl["mid"]}">{p["brand"]}</span>'
            f'{promo_html}'
            f'</div>'
            f'<div class="ptitle">{t_esc}</div>'
            f'<div class="price-big">{fmt_price(p["price"])}</div>'
            f'<div class="metrics">'
            f'<span class="met star">&#11088; {p["rating"]}</span>'
            f'<span class="met sales">&#128715; {p["sales"]}</span>'
            f'<span class="met">&#128205; {p["location"][:12]}</span>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        pp.append(card)
    pp.append('</div>')
    
    # === TABLE ===
    pp.append(f'<div id="table-{cat}" style="display:none"><div class="tbl-wrap"><table>'
              f'<thead><tr><th>排名</th><th>图片</th><th>品牌</th><th>产品名称（中文）</th>'
              f'<th>售价（泰铢）</th><th>折扣</th><th>评分</th><th>月销量</th><th>发货地</th></tr></thead>'
              f'<tbody>')
    for i, p in enumerate(products):
        rank = i + 1
        tp = 'top' if rank <= 3 else ''
        zh_t = clean_title(translations.get(p['title'], p['title']))
        te = zh_t.replace('<','&lt;').replace('>','&gt;')
        pp.append(
            f'<tr>'
            f'<td class="t-rank {tp}">#{rank}</td>'
            f'<td class="t-thumb"><img src="{p["img"]}" onerror="this.style.display=\'none\'"></td>'
            f'<td><span class="brand-pill" style="background:{cl["light"]};color:{cl["text"]};border:1px solid {cl["mid"]};display:inline-block">{p["brand"]}</span></td>'
            f'<td class="t-title"><div class="tt">{te}</div></td>'
            f'<td class="t-price">{fmt_price(p["price"])}</td>'
            f'<td class="t-disc">{p["discount"]}</td>'
            f'<td class="t-rating">&#11088; {p["rating"]}</td>'
            f'<td class="t-sales">&#128715; {p["sales"]}</td>'
            f'<td>{p["location"][:15]}</td>'
            f'</tr>'
        )
    pp.append('</tbody></table></div></div>')
    pp.append('</div>')
    lines.append(''.join(pp))

lines.append('</div>')  # end .content

lines.append('<div class="footer">数据来源：泰国 Shopee 平台 &nbsp;&bull;&nbsp; 共 6 个美妆品类 &nbsp;&bull;&nbsp; 各品类 Top 20 热销产品 &nbsp;&bull;&nbsp; 按月销量排序</div>')

lines.append("""<script>
function switchTab(id){
  document.querySelectorAll('.tab').forEach(function(t){
    var oc=t.getAttribute('onclick');
    if(oc&&oc.indexOf("'"+id+"'")>-1){t.classList.add('active');}
    else{t.classList.remove('active');}
  });
  document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('active');});
  var panel=document.getElementById('panel-'+id);
  if(panel){panel.classList.add('active');}
  window.scrollTo({top:0,behavior:'smooth'});
}
function setView(cat,view,btn){
  var grid=document.getElementById('grid-'+cat);
  var tbl=document.getElementById('table-'+cat);
  var vt=document.getElementById('vt-'+cat);
  btn.closest('.view-toggle').querySelectorAll('.vbtn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  if(view==='grid'){
    grid.style.display='grid';tbl.style.display='none';
    if(vt)vt.style.display='flex';
  }else{
    grid.style.display='none';tbl.style.display='block';
    if(vt)vt.style.display='none';
  }
}
</script>
</body>
</html>""")

html = '\n'.join(lines)
out = r'E:\泰国市场重点分析\泰国美妆Shopee热销看板.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Done! {len(html):,} chars -> {out}')
