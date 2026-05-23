import sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\泰国市场重点分析\tiktok销量数据\tiktok_data.json','r',encoding='utf-8') as f:
    tt_data = json.load(f)
with open(r'E:\泰国市场重点分析\tiktok销量数据\tiktok_translations.json','r',encoding='utf-8') as f:
    tt_trans = json.load(f)
with open(r'E:\泰国市场重点分析\processed_data.json','r',encoding='utf-8') as f:
    sp_data = json.load(f)
with open(r'E:\泰国市场重点分析\translations.json','r',encoding='utf-8') as f:
    sp_trans = json.load(f)

def clean_title(zh):
    if not zh: return '美妆产品'
    zh = re.sub(r'[\u0e00-\u0e7f]+','',zh)
    zh = re.sub(r'[\U00010000-\U0010ffff]','',zh,flags=re.UNICODE)
    zh = re.sub(r'[❗️💓✨🔥🌸⚡【】\[\]]+','',zh)
    for pat in [r'公司购物篮','直播','LIVE','品牌主\d*']:
        zh = re.sub(pat,'',zh)
    for sep in ['|','｜']:
        if sep in zh and len(zh.split(sep)[0].strip())>4:
            zh = zh.split(sep)[0].strip(); break
    if '。' in zh: zh = zh.split('。')[0]
    zh = re.sub(r'\s{2,}',' ',zh).strip()
    zh = zh.strip(' ,，、！!。.·-—')
    if len(zh)>48: zh=zh[:46]+'…'
    return zh if len(zh)>1 else '美妆产品'

def parse_sales(s):
    try:
        s2 = str(s).replace('k+ sold/month','000').replace('k+','000').replace('+','').replace(' sold/month','').strip()
        return int(float(s2))
    except: return 0

# ===================== 品牌数据定义 =====================
# 每个品牌: name, origin, channels, cats, products(list), consumer, strategy, color
BRANDS = [
    {
        'name': 'OUKEYA',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['唇部','腮红','眼线','眉部','高光修容'],
        'tt_sales': 344488,
        'sp_sales': 0,
        'color': '#FF2D55',
        'products': [
            {'name':'HOT KISS哑光液体唇膏（买一送一）','cat':'唇部','platform':'TikTok','sales':105400,'price':'฿79','tag':'爆款'},
            {'name':'BLINK BLINK闪光腮红','cat':'腮红','platform':'TikTok','sales':101608,'price':'฿94','tag':'热销'},
            {'name':'超细眼线笔防水防汗','cat':'眼线','platform':'TikTok','sales':63000,'price':'฿43','tag':''},
        ],
        'consumer': '18-30岁泰国年轻女性，追求高性价比与社交媒体潮流，喜欢彩妆叠涂和多用途产品',
        'strategy': '买一送一高折扣引流 + TikTok达人佣金15%驱动，多品类矩阵铺量',
        'tags': ['平价爆款','买一送一','TikTok霸榜','本土品牌'],
    },
    {
        'name': 'JMCY Beauty',
        'origin': '国产（中国品牌出海）',
        'origin_en': 'CN Brand',
        'channels': ['TikTok Shop'],
        'cats': ['眼线','眉部','睫毛膏','定妆喷雾','高光修容'],
        'tt_sales': 308500,
        'sp_sales': 0,
        'color': '#2D2D5A',
        'products': [
            {'name':'Ultra Fine 0.01mm防水眼线笔','cat':'眼线','platform':'TikTok','sales':131505,'price':'฿43-65','tag':'爆款'},
            {'name':'丝绒哑光眉胶12h持久','cat':'眉部','platform':'TikTok','sales':108454,'price':'฿86-162','tag':'热销'},
            {'name':'高光修容棒','cat':'高光修容','platform':'TikTok','sales':18000,'price':'฿55','tag':''},
        ],
        'consumer': '18-28岁精致妆容追求者，注重技术卖点（0.01mm细度/12h持久），接受中等价位',
        'strategy': '技术卖点差异化 + 中低佣金(8%)精选优质达人，眼妆品类深度聚焦',
        'tags': ['技术卖点','眼妆专家','中国出海','精准客群'],
    },
    {
        'name': 'Music Flower',
        'origin': '国产（中国品牌出海）',
        'origin_en': 'CN Brand',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['粉底遮瑕','眼线'],
        'tt_sales': 319072,
        'sp_sales': 0,
        'color': '#E07B3A',
        'products': [
            {'name':'Photo Genic轻薄防水粉底液SPF50 30ml','cat':'粉底遮瑕','platform':'TikTok','sales':126129,'price':'฿109-119','tag':'爆款'},
            {'name':'超细防水眼线笔','cat':'眼线','platform':'TikTok','sales':18000,'price':'฿49','tag':''},
        ],
        'consumer': '20-35岁追求轻薄底妆的都市女性，注重防水控油，适合泰国热带气候，价格敏感型',
        'strategy': '极致性价比（฿109）+ 轻薄防水功效精准切需，10%佣金稳定达人合作',
        'tags': ['极致性价比','底妆专家','中国出海','防水卖点'],
    },
    {
        'name': 'Kathy Amrez / Kathy Cosmetics',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['腮红','唇部','粉底遮瑕'],
        'tt_sales': 286126,
        'sp_sales': 0,
        'color': '#E91E8C',
        'products': [
            {'name':'GOLDEN HYA TINT玻尿酸腮红','cat':'腮红','platform':'TikTok','sales':83068,'price':'฿236','tag':'爆款'},
            {'name':'Mini Matte Stick迷你哑光唇棒','cat':'唇部','platform':'TikTok','sales':70873,'price':'฿134','tag':'热销'},
            {'name':'GOLDEN HYA TINT腮红（Shopee）','cat':'腮红','platform':'Shopee','sales':10000,'price':'฿24','tag':''},
        ],
        'consumer': '20-32岁注重护肤成分的彩妆用户，接受中高价位，追求"保湿+显色"双重功效',
        'strategy': '玻尿酸功效概念 + 中高价定位 + 15%高佣金激励达人，颜值包装吸引年轻群体',
        'tags': ['护肤成分','中高端定价','腮红领军','双平台布局'],
    },
    {
        'name': 'PALA',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop'],
        'cats': ['粉底遮瑕','腮红','眼线','散粉','定妆喷雾','睫毛膏','眉部'],
        'tt_sales': 242510,
        'sp_sales': 0,
        'color': '#5BAF8A',
        'products': [
            {'name':'轻质防水粉底SPF50+PA++++ 软雾持妆','cat':'粉底遮瑕','platform':'TikTok','sales':88579,'price':'฿119-125','tag':'爆款'},
            {'name':'腮红','cat':'腮红','platform':'TikTok','sales':30000,'price':'฿94','tag':''},
            {'name':'散粉','cat':'散粉','platform':'TikTok','sales':20000,'price':'฿99','tag':''},
        ],
        'consumer': '18-30岁全妆需求女性，注重日常彩妆一站式采购，对本土品牌有信任感',
        'strategy': '多品类全矩阵覆盖 + 20%超高佣金激励，SPF50+防晒底妆主打泰国刚需场景',
        'tags': ['全品类矩阵','高佣金驱动','本土信赖','SPF防晒'],
    },
    {
        'name': 'BEAUTILAB',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['粉底遮瑕','遮瑕'],
        'tt_sales': 231090,
        'sp_sales': 60000,
        'color': '#7B4FD4',
        'products': [
            {'name':'A2P美白遮瑕膏+桃色+蓝色色彩矫正套组','cat':'粉底遮瑕','platform':'TikTok','sales':97312,'price':'฿191-230','tag':'爆款'},
            {'name':'A2P色彩矫正遮瑕（Shopee）','cat':'遮瑕','platform':'Shopee','sales':60000,'price':'฿79','tag':'热销'},
        ],
        'consumer': '20-35岁有遮瑕需求的女性，关注黑眼圈/泛红问题，愿意为专业色彩矫正技术付溢价',
        'strategy': '"桃色+蓝色校色"功效概念引爆两平台，Shopee低价引流+TikTok中高价转化',
        'tags': ['色彩矫正爆款','双平台联动','专业功效','遮瑕领军'],
    },
    {
        'name': 'DAZZLE ME',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['定妆喷雾','睫毛膏','唇部'],
        'tt_sales': 120999,
        'sp_sales': 0,
        'color': '#00B4D8',
        'products': [
            {'name':'Get a Grip控油锁妆定妆喷雾','cat':'定妆喷雾','platform':'TikTok','sales':59539,'price':'฿94-221','tag':'爆款'},
            {'name':'Barbie×DAZZLE ME联名睫毛膏','cat':'睫毛膏','platform':'TikTok','sales':18145,'price':'฿92-184','tag':'热销'},
            {'name':'定妆喷雾（Shopee）','cat':'定妆喷雾','platform':'Shopee','sales':4000,'price':'฿215','tag':''},
        ],
        'consumer': '18-28岁喜爱IP联名和潮流彩妆的年轻女性，对品牌故事和颜值包装有较强吸引力',
        'strategy': 'Barbie IP联名制造话题 + 明星/KOL背书，高颜值产品线+定妆刚需稳固复购',
        'tags': ['IP联名','话题营销','TH本土','定妆刚需'],
    },
    {
        'name': 'Luminee Beauty',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop'],
        'cats': ['眼线','睫毛膏','高光修容'],
        'tt_sales': 119706,
        'sp_sales': 0,
        'color': '#D4A017',
        'products': [
            {'name':'修容高光二合一棒（V脸塑形）','cat':'高光修容','platform':'TikTok','sales':37153,'price':'฿38','tag':'爆款'},
            {'name':'买一送五超细眼线笔0.01mm','cat':'眼线','platform':'TikTok','sales':30781,'price':'฿32','tag':'热销'},
            {'name':'防水睫毛膏','cat':'睫毛膏','platform':'TikTok','sales':20000,'price':'฿69','tag':''},
        ],
        'consumer': '18-26岁追求高性价比的学生及年轻白领，喜欢买一送多捆绑促销，入门级彩妆用户',
        'strategy': '极低价+买一送多捆绑引流，快速冲GMV，10%佣金广铺达人渠道',
        'tags': ['超低价引流','买一送多','学生群体','TikTok专属'],
    },
    {
        'name': 'LUCKGO',
        'origin': '国产（泰国本土/东南亚）',
        'origin_en': 'TH/SEA',
        'channels': ['TikTok Shop'],
        'cats': ['唇部'],
        'tt_sales': 118536,
        'sp_sales': 0,
        'color': '#FF6B2B',
        'products': [
            {'name':'镜面光泽唇彩（多色可选）','cat':'唇部','platform':'TikTok','sales':97689,'price':'฿67','tag':'爆款'},
            {'name':'蜜罐唇彩买1送1','cat':'唇部','platform':'TikTok','sales':20847,'price':'฿106','tag':'热销'},
        ],
        'consumer': '16-25岁喜爱镜面感和玻璃唇妆效的年轻女生，强社交属性，TikTok原住民用户',
        'strategy': '多色选择+镜面光泽差异化视觉效果，TikTok上妆效展示视频强引流',
        'tags': ['镜面光泽','多色选择','Z世代','TikTok专属'],
    },
    {
        'name': 'MAYBELLINE（美宝莲）',
        'origin': '国际（欧莱雅集团）',
        'origin_en': 'International',
        'channels': ['TikTok Shop','Shopee'],
        'cats': ['唇部'],
        'tt_sales': 105491,
        'sp_sales': 30000,
        'color': '#C62828',
        'products': [
            {'name':'SuperStay Vinyl Ink乙烯基唇膏（100万销量社会证明）','cat':'唇部','platform':'TikTok','sales':60599,'price':'฿279','tag':'爆款'},
            {'name':'SuperStay哑光墨水液体唇膏','cat':'唇部','platform':'TikTok','sales':44892,'price':'฿249','tag':'热销'},
            {'name':'SuperStay乙烯基唇膏（Shopee）','cat':'唇部','platform':'Shopee','sales':30000,'price':'฿309','tag':''},
        ],
        'consumer': '22-35岁有品牌意识、追求持妆质量的都市女性，信任国际品牌技术背书，消费力中等偏上',
        'strategy': '"100万销量"社会证明+16h持久技术卖点，双平台稳定布局，品牌溢价策略',
        'tags': ['国际品牌','社会证明','持妆技术','中高价位'],
    },
    {
        'name': 'AURA RICH',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['TikTok Shop'],
        'cats': ['散粉'],
        'tt_sales': 94393,
        'sp_sales': 0,
        'color': '#D48BBB',
        'products': [
            {'name':'PERFECT POWDER PUFF散粉蜜粉饼','cat':'散粉','platform':'TikTok','sales':45991,'price':'฿159-589','tag':'爆款'},
            {'name':'POWDER FOUNDATION SPF50 PA++++','cat':'散粉','platform':'TikTok','sales':27861,'price':'฿168-565','tag':'热销'},
        ],
        'consumer': '22-38岁注重护肤底妆品质的成熟女性，接受较高客单价，品牌主播模式培养忠实用户群',
        'strategy': '品牌主账号自播+高佣金(20%)双驱动，套盒策略提高客单价，主打SPF防晒专业感',
        'tags': ['品牌自播','高客单价','专业散粉','成熟客群'],
    },
    {
        'name': 'LAMEILA',
        'origin': '国产（中国品牌出海）',
        'origin_en': 'CN Brand',
        'channels': ['TikTok Shop'],
        'cats': ['散粉','BB/CC霜'],
        'tt_sales': 85008,
        'sp_sales': 0,
        'color': '#9C7BB5',
        'products': [
            {'name':'NO.5048泡芙散粉哑光控油毛孔隐形','cat':'散粉','platform':'TikTok','sales':60614,'price':'฿15','tag':'爆款'},
            {'name':'NO.3019 BB霜美白遮瑕','cat':'BB/CC霜','platform':'TikTok','sales':12197,'price':'฿27','tag':'热销'},
        ],
        'consumer': '16-24岁价格极度敏感的学生群体，入门彩妆用户，通过TikTok发现产品，首次尝试彩妆',
        'strategy': '极致低价（฿15/฿27）快速积累GMV和用户口碑，中国供应链成本优势明显',
        'tags': ['极致低价','中国出海','入门彩妆','学生群体'],
    },
    {
        'name': 'SUPERMOM',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['Shopee','TikTok Shop'],
        'cats': ['粉底','睫毛膏'],
        'tt_sales': 15000,
        'sp_sales': 60000,
        'color': '#FF8C42',
        'products': [
            {'name':'哑光粉底液SPF控油持妆（Shopee）','cat':'粉底','platform':'Shopee','sales':60000,'price':'฿165','tag':'爆款'},
            {'name':'防水睫毛膏','cat':'睫毛膏','platform':'Shopee','sales':10000,'price':'฿89','tag':''},
        ],
        'consumer': '25-40岁有一定消费力的职场女性及妈妈群体，注重实用性和品质，Shopee忠实用户',
        'strategy': 'Shopee平台深耕+口碑积累，哑光粉底主打职场场景，性价比与品质兼顾',
        'tags': ['Shopee强势','职场女性','本土口碑','粉底专家'],
    },
    {
        'name': 'hince',
        'origin': '国际（韩国品牌）',
        'origin_en': 'Korean Brand',
        'channels': ['Shopee'],
        'cats': ['唇部'],
        'tt_sales': 0,
        'sp_sales': 30000,
        'color': '#9B59B6',
        'products': [
            {'name':'Raw Glow Gel Tint Mini果冻染色唇膏（Shopee）','cat':'唇部','platform':'Shopee','sales':30000,'price':'฿235','tag':'爆款'},
        ],
        'consumer': '22-32岁追求韩系精致妆容的美妆爱好者，有一定消费能力，关注韩国美妆博主推荐',
        'strategy': 'Shopee精品定位+韩系小众调性，果冻质感差异化，KOL种草内容营销',
        'tags': ['韩国品牌','小众精品','果冻质感','Shopee专属'],
    },
    {
        'name': 'CANMAKE',
        'origin': '国际（日本品牌）',
        'origin_en': 'Japanese Brand',
        'channels': ['Shopee','TikTok Shop'],
        'cats': ['腮红','睫毛膏'],
        'tt_sales': 10000,
        'sp_sales': 20000,
        'color': '#E84393',
        'products': [
            {'name':'Cream Cheek腮红（Shopee）','cat':'腮红','platform':'Shopee','sales':20000,'price':'฿189','tag':'热销'},
            {'name':'Quick Lash Curler防水睫毛膏','cat':'睫毛膏','platform':'TikTok','sales':10000,'price':'฿219','tag':''},
        ],
        'consumer': '20-30岁喜爱日系可爱妆容的女生，信任日本品牌品质，对腮红颜色选择有较高要求',
        'strategy': '日系品牌口碑+可爱包装颜值营销，双平台自然流量+内容种草双驱',
        'tags': ['日本品牌','可爱日系','双平台','品质信赖'],
    },
    {
        'name': 'MizuMi',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['Shopee'],
        'cats': ['腮红'],
        'tt_sales': 0,
        'sp_sales': 30000,
        'color': '#27AE60',
        'products': [
            {'name':'防晒腮红SPF50+ PA++++ (Shopee)','cat':'腮红','platform':'Shopee','sales':30000,'price':'฿159','tag':'爆款'},
        ],
        'consumer': '22-35岁注重防晒护肤的户外活跃女性，彩妆护肤双重需求，泰国阳光强烈场景驱动',
        'strategy': 'SPF50+防晒腮红开创新品类赛道，"彩妆+防晒"二合一功能卖点精准切中泰国气候痛点',
        'tags': ['防晒腮红','功能创新','Shopee专属','泰国本土'],
    },
    {
        'name': 'KATE（日本）',
        'origin': '国际（日本花王集团）',
        'origin_en': 'Japanese Brand',
        'channels': ['Shopee'],
        'cats': ['睫毛膏'],
        'tt_sales': 0,
        'sp_sales': 20000,
        'color': '#2C3E50',
        'products': [
            {'name':'3D眉毛膏（精准仿真发丝）(Shopee)','cat':'睫毛膏','platform':'Shopee','sales':20000,'price':'฿289','tag':'热销'},
        ],
        'consumer': '25-38岁注重精致眉妆的成熟彩妆用户，认可日系专业技术，接受较高价位，重复购买率高',
        'strategy': '日系专业定位+精准眉形技术溢价，高评分积累 Shopee 站内自然流量',
        'tags': ['日本品牌','专业技术','高端定价','眉眼专家'],
    },
    {
        'name': 'ROM&ND',
        'origin': '国际（韩国品牌）',
        'origin_en': 'Korean Brand',
        'channels': ['Shopee','TikTok Shop'],
        'cats': ['腮红','唇部','睫毛膏'],
        'tt_sales': 10000,
        'sp_sales': 20000,
        'color': '#FF6B9D',
        'products': [
            {'name':'Better Than Cheek腮红（Shopee）','cat':'腮红','platform':'Shopee','sales':20000,'price':'฿1（直播特价）','tag':'热销'},
            {'name':'Juicy Lasting Tint唇彩','cat':'唇部','platform':'TikTok','sales':10000,'price':'฿259','tag':''},
        ],
        'consumer': '20-30岁韩系美妆爱好者，跟随韩国美妆博主潮流，对韩妆趋势敏感，Shopee重度用户',
        'strategy': '直播限时折扣冲量+TikTok内容种草双驱，韩系氛围感包装强化品牌调性',
        'tags': ['韩国品牌','直播冲量','氛围感包装','双平台'],
    },
    {
        'name': 'Flortte（花洛莉亚）',
        'origin': '国产（中国品牌出海）',
        'origin_en': 'CN Brand',
        'channels': ['TikTok Shop'],
        'cats': ['腮红','眼影','高光修容'],
        'tt_sales': 40000,
        'sp_sales': 0,
        'color': '#FF8FAB',
        'products': [
            {'name':'×Esther Bunny联名高光盘','cat':'高光修容','platform':'TikTok','sales':20000,'price':'฿174','tag':'热销'},
            {'name':'眼影盘','cat':'眼影','platform':'TikTok','sales':15000,'price':'฿124','tag':''},
        ],
        'consumer': '18-28岁二次元/潮玩爱好者女生，对IP联名和可爱包装高度敏感，愿意为限定款付溢价',
        'strategy': 'IP联名限定款制造稀缺感+TikTok开箱/试色内容病毒传播，颜值经济驱动',
        'tags': ['IP联名','颜值经济','Z世代','中国出海'],
    },
    {
        'name': 'CUTE PRESS',
        'origin': '国产（泰国本土）',
        'origin_en': 'TH Local',
        'channels': ['Shopee','TikTok Shop'],
        'cats': ['定妆喷雾'],
        'tt_sales': 4000,
        'sp_sales': 4000,
        'color': '#FF85A2',
        'products': [
            {'name':'1-2-BEAUTIFUL定妆喷雾60ML（Shopee）','cat':'定妆喷雾','platform':'Shopee','sales':4000,'price':'฿215','tag':''},
            {'name':'定妆喷雾（TikTok）','cat':'定妆喷雾','platform':'TikTok','sales':4000,'price':'฿215','tag':''},
        ],
        'consumer': '20-35岁重视彩妆持久度的泰国本土女性，对本土品牌忠诚度较高，日常通勤场景驱动购买',
        'strategy': '泰国本土老品牌信任背书 + 双平台稳健布局，性价比定妆功能维持忠实用户群',
        'tags': ['本土老牌','双平台','定妆刚需','稳定复购'],
    },
]

def fmt_sales(n):
    if n >= 100000: return f'{n//1000}k+'
    if n >= 1000: return f'{n//1000}k+'
    return str(n)

def channel_badge(ch):
    styles = {
        'TikTok Shop': ('background:rgba(255,0,80,0.1);color:#CC0040;border:1px solid rgba(255,0,80,0.25)','&#127381; TikTok'),
        'Shopee': ('background:rgba(238,77,45,0.1);color:#C04010;border:1px solid rgba(238,77,45,0.25)','&#128722; Shopee'),
    }
    s, label = styles.get(ch, ('background:#f0f0f0;color:#666',''))
    return f'<span style="display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;padding:3px 9px;border-radius:12px;{s}">{label}</span>'

def origin_badge(o, oe):
    color_map = {
        'TH Local': '#27AE60','CN Brand': '#E07B3A','International': '#2980B9','Korean Brand': '#9B59B6','Japanese Brand': '#2C3E50','TH/SEA': '#16A085'
    }
    c = color_map.get(oe,'#888')
    return f'<span style="font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px;background:{c}15;color:{c};border:1px solid {c}40">{o}</span>'

def platform_dot(p):
    if p == 'TikTok': return '<span style="font-size:10px;font-weight:700;color:#FF0050;background:rgba(255,0,80,0.08);padding:1px 6px;border-radius:8px;border:1px solid rgba(255,0,80,0.2)">&#127381;</span>'
    return '<span style="font-size:10px;font-weight:700;color:#EE4D2D;background:rgba(238,77,45,0.08);padding:1px 6px;border-radius:8px;border:1px solid rgba(238,77,45,0.2)">&#128722;</span>'

# total
total_brands = len(BRANDS)
tt_only = sum(1 for b in BRANDS if 'TikTok Shop' in b['channels'] and 'Shopee' not in b['channels'])
sp_only = sum(1 for b in BRANDS if 'Shopee' in b['channels'] and 'TikTok Shop' not in b['channels'])
dual = total_brands - tt_only - sp_only

lines = []
lines.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泰国美妆热门品牌分析 · Shopee × TikTok</title>
<style>
:root{
  --bg:#F6F7FA;--white:#FFFFFF;
  --gray1:#F4F5F8;--gray2:#E8E9EF;--gray3:#D0D2DE;
  --text:#1A1A2E;--text2:#4A4A6A;--text3:#9A9ABB;
  --shopee:#EE4D2D;--tt:#FF0050;
  --shadow:0 2px 12px rgba(0,0,0,0.07);
  --shadow-hover:0 8px 32px rgba(0,0,0,0.13);
  --radius:16px;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;}

/* HEADER */
.header{
  background:#fff;border-bottom:1px solid var(--gray2);
  padding:20px 32px;display:flex;align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:100;box-shadow:var(--shadow);
}
.logo-row{display:flex;align-items:center;gap:14px;}
.logo-icons{display:flex;gap:6px;}
.logo-ico{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;}
.logo-ico.tt{background:linear-gradient(135deg,#FF0050,#FF6B9D);}
.logo-ico.sp{background:linear-gradient(135deg,#EE4D2D,#FFB347);}
.header-title h1{font-size:18px;font-weight:800;color:var(--text);}
.header-title p{font-size:12px;color:var(--text3);margin-top:3px;}
.header-stats{display:flex;gap:28px;}
.hstat{text-align:center;}
.hstat .v{font-size:22px;font-weight:800;color:var(--text);}
.hstat .l{font-size:11px;color:var(--text3);margin-top:2px;}
.hstat .v.tt{color:var(--tt);}
.hstat .v.sp{color:var(--shopee);}

/* FILTERS */
.filters{background:#fff;border-bottom:1px solid var(--gray2);padding:12px 32px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.filter-label{font-size:12px;color:var(--text3);font-weight:600;margin-right:4px;}
.fbtn{
  padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;
  border:1px solid var(--gray2);background:#fff;color:var(--text3);cursor:pointer;
  transition:all .2s;
}
.fbtn:hover{border-color:var(--text3);}
.fbtn.active{background:var(--text);color:#fff;border-color:var(--text);}
.fbtn.tt-btn.active{background:var(--tt);border-color:var(--tt);}
.fbtn.sp-btn.active{background:var(--shopee);border-color:var(--shopee);}

/* CONTENT */
.content{max-width:1380px;margin:0 auto;padding:28px 24px;}
.section-title{display:flex;align-items:center;gap:14px;margin-bottom:22px;}
.section-title h2{font-size:16px;font-weight:700;color:var(--text);}
.section-title .line{flex:1;height:1px;background:var(--gray2);}
.section-tag{font-size:11px;color:var(--text3);background:var(--gray1);padding:3px 10px;border-radius:10px;border:1px solid var(--gray2);}

/* BRAND GRID */
.brand-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:20px;}
.brand-card{
  background:#fff;border-radius:var(--radius);border:1px solid var(--gray2);
  box-shadow:var(--shadow);overflow:hidden;
  transition:transform .2s, box-shadow .2s;
}
.brand-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);}
.bc-header{
  padding:16px 18px 14px;
  border-bottom:1px solid var(--gray2);
  position:relative;overflow:hidden;
}
.bc-header::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:var(--bcolor);
}
.bc-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;}
.bc-name{font-size:16px;font-weight:800;color:var(--text);line-height:1.2;}
.bc-origin{margin-top:4px;}
.bc-rank{
  font-size:11px;font-weight:800;padding:3px 10px;border-radius:12px;
  background:var(--bcolor-light);color:var(--bcolor);border:1px solid var(--bcolor-border);
  white-space:nowrap;flex-shrink:0;
}
.bc-channels{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;}
.bc-cats{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px;}
.cat-chip{
  font-size:10px;padding:2px 8px;border-radius:10px;
  background:var(--gray1);color:var(--text3);border:1px solid var(--gray2);
  font-weight:600;
}
.bc-tags{display:flex;gap:5px;flex-wrap:wrap;margin-top:8px;}
.brand-tag{
  font-size:10px;padding:2px 8px;border-radius:10px;
  background:var(--bcolor-light);color:var(--bcolor);
  border:1px solid var(--bcolor-border);font-weight:700;
}

/* SECTIONS INSIDE CARD */
.bc-body{padding:14px 18px;display:flex;flex-direction:column;gap:12px;}
.bc-section-title{font-size:10px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:var(--text3);margin-bottom:6px;}
.products-list{display:flex;flex-direction:column;gap:6px;}
.prod-row{
  display:flex;align-items:center;gap:10px;
  padding:7px 10px;border-radius:10px;background:var(--gray1);
  border:1px solid var(--gray2);
}
.prod-rank{font-size:11px;font-weight:800;color:var(--text3);width:20px;text-align:center;flex-shrink:0;}
.prod-rank.top{color:var(--bcolor);}
.prod-info{flex:1;overflow:hidden;}
.prod-name{font-size:11px;color:var(--text2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.prod-cat{font-size:10px;color:var(--text3);margin-top:1px;}
.prod-meta{display:flex;align-items:center;gap:6px;flex-shrink:0;}
.prod-price{font-size:11px;font-weight:700;color:var(--bcolor);}
.prod-sales{font-size:10px;color:#2E7D32;font-weight:600;background:rgba(46,125,50,0.08);padding:2px 6px;border-radius:6px;border:1px solid rgba(46,125,50,0.15);}
.prod-tag-hot{font-size:9px;font-weight:800;color:#fff;background:var(--tt);padding:1px 5px;border-radius:5px;}

/* CONSUMER & STRATEGY */
.info-box{
  padding:10px 12px;border-radius:10px;
  background:var(--gray1);border:1px solid var(--gray2);
}
.info-box.consumer::before{content:'👥 消费人群  ';font-size:10px;font-weight:800;color:var(--text3);display:block;margin-bottom:4px;}
.info-box.strategy::before{content:'💡 运营策略  ';font-size:10px;font-weight:800;color:var(--text3);display:block;margin-bottom:4px;}
.info-box p{font-size:12px;color:var(--text2);line-height:1.6;}

/* SALES BAR */
.sales-bars{display:flex;flex-direction:column;gap:6px;}
.sbar-row{display:flex;align-items:center;gap:8px;}
.sbar-label{font-size:10px;font-weight:700;color:var(--text3);width:60px;flex-shrink:0;display:flex;align-items:center;gap:4px;}
.sbar-wrap{flex:1;height:8px;background:var(--gray2);border-radius:4px;overflow:hidden;}
.sbar-fill{height:100%;border-radius:4px;transition:width .5s;}
.sbar-val{font-size:10px;font-weight:700;width:48px;text-align:right;flex-shrink:0;}

/* FOOTER */
.footer{text-align:center;padding:20px;color:var(--text3);font-size:12px;border-top:1px solid var(--gray2);margin-top:32px;background:#fff;}

@media(max-width:900px){
  .brand-grid{grid-template-columns:1fr;}
  .header{flex-wrap:wrap;gap:12px;padding:14px 16px;}
  .content{padding:16px;}
  .filters{padding:10px 16px;}
}
</style>
</head>
<body>""")

# HEADER
lines.append(f"""<div class="header">
<div class="logo-row">
  <div class="logo-icons">
    <div class="logo-ico tt">&#127381;</div>
    <div class="logo-ico sp">&#128722;</div>
  </div>
  <div class="header-title">
    <h1>泰国美妆热门品牌全景分析</h1>
    <p>Thailand Beauty Brand Intelligence &nbsp;&bull;&nbsp; Shopee × TikTok 双平台数据 &nbsp;&bull;&nbsp; 2026年4月</p>
  </div>
</div>
<div class="header-stats">
  <div class="hstat"><div class="v">{total_brands}</div><div class="l">热门品牌</div></div>
  <div class="hstat"><div class="v tt">{tt_only+dual}</div><div class="l">TikTok在售</div></div>
  <div class="hstat"><div class="v sp">{sp_only+dual}</div><div class="l">Shopee在售</div></div>
  <div class="hstat"><div class="v">{dual}</div><div class="l">双平台</div></div>
</div>
</div>""")

# FILTERS
lines.append("""<div class="filters">
<span class="filter-label">筛选:</span>
<button class="fbtn active" onclick="filterBrands('all',this)">全部品牌</button>
<button class="fbtn tt-btn" onclick="filterBrands('tt',this)">&#127381; TikTok</button>
<button class="fbtn sp-btn" onclick="filterBrands('sp',this)">&#128722; Shopee</button>
<button class="fbtn" onclick="filterBrands('dual',this)">双平台</button>
<button class="fbtn" onclick="filterBrands('local',this)">泰国本土品牌</button>
<button class="fbtn" onclick="filterBrands('intl',this)">国际/韩日品牌</button>
<button class="fbtn" onclick="filterBrands('cn',this)">中国出海品牌</button>
</div>""")

lines.append('<div class="content">')
lines.append(f'<div class="section-title"><h2>&#127942; 品牌详细分析卡</h2><div class="line"></div><div class="section-tag">共 {total_brands} 个品牌 · 按综合销量排序</div></div>')
lines.append('<div class="brand-grid" id="brandGrid">')

max_sales = max(b['tt_sales'] + b['sp_sales'] for b in BRANDS)

for idx, b in enumerate(BRANDS):
    color = b['color']
    color_light = color + '15'
    color_border = color + '35'
    total_s = b['tt_sales'] + b['sp_sales']

    # channel data attrs
    is_tt = 'TikTok Shop' in b['channels']
    is_sp = 'Shopee' in b['channels']
    is_dual = is_tt and is_sp
    origin_en = b['origin_en']
    data_attrs = f'data-tt="{int(is_tt)}" data-sp="{int(is_sp)}" data-dual="{int(is_dual)}" data-origin="{origin_en}"'

    # rank
    rank_html = f'<div class="bc-rank">#{idx+1} 综合榜</div>'

    # channels
    ch_html = ''.join(channel_badge(c) for c in b['channels'])

    # cats
    cats_html = ''.join(f'<span class="cat-chip">{c}</span>' for c in b['cats'])

    # brand tags
    tags_html = ''.join(f'<span class="brand-tag">{t}</span>' for t in b['tags'])

    # products
    prods_html = ''
    for i, p in enumerate(b['products']):
        rk_cls = 'top' if i < 2 else ''
        tag_html = f'<span class="prod-tag-hot">{p["tag"]}</span>' if p.get('tag') else ''
        plat_dot = platform_dot(p['platform'])
        sales_disp = fmt_sales(p['sales'])
        prods_html += (
            f'<div class="prod-row">'
            f'<div class="prod-rank {rk_cls}">#{i+1}</div>'
            f'<div class="prod-info">'
            f'<div class="prod-name">{p["name"]}</div>'
            f'<div class="prod-cat">{plat_dot} {p["cat"]}</div>'
            f'</div>'
            f'<div class="prod-meta">'
            f'<span class="prod-price">{p["price"]}</span>'
            f'<span class="prod-sales">&#128715; {sales_disp}</span>'
            f'{tag_html}'
            f'</div>'
            f'</div>'
        )

    # sales bars
    tt_pct = int(b['tt_sales'] / max_sales * 100) if max_sales else 0
    sp_pct = int(b['sp_sales'] / max_sales * 100) if max_sales else 0
    bars_html = ''
    if b['tt_sales'] > 0:
        bars_html += (f'<div class="sbar-row">'
                      f'<div class="sbar-label">&#127381; TikTok</div>'
                      f'<div class="sbar-wrap"><div class="sbar-fill" style="width:{tt_pct}%;background:#FF0050"></div></div>'
                      f'<div class="sbar-val" style="color:#FF0050">{fmt_sales(b["tt_sales"])}</div>'
                      f'</div>')
    if b['sp_sales'] > 0:
        bars_html += (f'<div class="sbar-row">'
                      f'<div class="sbar-label">&#128722; Shopee</div>'
                      f'<div class="sbar-wrap"><div class="sbar-fill" style="width:{sp_pct}%;background:#EE4D2D"></div></div>'
                      f'<div class="sbar-val" style="color:#EE4D2D">{fmt_sales(b["sp_sales"])}</div>'
                      f'</div>')

    bars_block = f'<div class="sales-bars">{bars_html}</div>' if bars_html else ''
    lines.append(
        f'<div class="brand-card" {data_attrs} style="--bcolor:{color};--bcolor-light:{color_light};--bcolor-border:{color_border}">'
        f'<div class="bc-header">'
        f'<div class="bc-top">'
        f'<div><div class="bc-name">{b["name"]}</div><div class="bc-origin">{origin_badge(b["origin"], b["origin_en"])}</div></div>'
        f'{rank_html}'
        f'</div>'
        f'<div class="bc-channels">{ch_html}</div>'
        f'<div class="bc-cats">{cats_html}</div>'
        f'<div class="bc-tags">{tags_html}</div>'
        f'</div>'
        f'<div class="bc-body">'
        f'<div><div class="bc-section-title">热销产品</div><div class="products-list">{prods_html}</div></div>'
        f'{bars_block}'
        f'<div class="info-box consumer"><p>{b["consumer"]}</p></div>'
        f'<div class="info-box strategy"><p>{b["strategy"]}</p></div>'
        f'</div>'
        f'</div>'
    )

lines.append('</div>')  # brand-grid
lines.append('</div>')  # content
lines.append('<div class="footer">数据来源：TikTok Thailand（FastMoss 2026年4月）× Shopee Thailand · 共分析 20 个热门品牌 · 11个美妆品类</div>')

lines.append("""<script>
function filterBrands(type, btn) {
  document.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  var cards = document.querySelectorAll('.brand-card');
  cards.forEach(function(c) {
    var show = false;
    if(type==='all') show=true;
    else if(type==='tt') show=c.dataset.tt==='1';
    else if(type==='sp') show=c.dataset.sp==='1';
    else if(type==='dual') show=c.dataset.dual==='1';
    else if(type==='local') show=c.dataset.origin.indexOf('TH')>-1;
    else if(type==='intl') show=['International','Korean Brand','Japanese Brand'].indexOf(c.dataset.origin)>-1;
    else if(type==='cn') show=c.dataset.origin==='CN Brand';
    c.style.display = show ? '' : 'none';
  });
}
</script>
</body>
</html>""")

html = '\n'.join(lines)
out = r'E:\泰国市场重点分析\泰国美妆热门品牌分析.html'
with open(out,'w',encoding='utf-8') as f:
    f.write(html)
print(f'Done! {len(html):,} chars -> {out}')
