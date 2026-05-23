# -*- coding: utf-8 -*-
"""泰国美妆热门品牌分析看板 v2 - 30品牌 + 产品图片"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\泰国市场重点分析\tiktok销量数据\tiktok_data.json','r',encoding='utf-8') as f:
    tt_data = json.load(f)
with open(r'E:\泰国市场重点分析\processed_data.json','r',encoding='utf-8') as f:
    sp_data = json.load(f)
with open(r'E:\泰国市场重点分析\tiktok销量数据\tiktok_translations.json','r',encoding='utf-8') as f:
    tt_trans = json.load(f)
with open(r'E:\泰国市场重点分析\translations.json','r',encoding='utf-8') as f:
    sp_trans = json.load(f)

tt_shop = {}
for cat, prods in tt_data.items():
    for p in prods:
        shop = p['shop'].strip()
        if not shop: continue
        if shop not in tt_shop: tt_shop[shop] = []
        tt_shop[shop].append({**p,'cat':cat})

sp_brand_idx = {}
for cat, prods in sp_data.items():
    for p in prods:
        brand = p.get('brand','').strip()
        if not brand or brand=='Unknown': continue
        if brand not in sp_brand_idx: sp_brand_idx[brand] = []
        sp_brand_idx[brand].append({**p,'cat':cat})

def tt_prods(shop_name, top=3):
    prods = sorted(tt_shop.get(shop_name,[]), key=lambda x: -x['sales'])[:top]
    result = []
    for p in prods:
        zh = tt_trans.get(p['name'], p['name'])[:38]
        result.append({'zh': zh, 'price': p['price'], 'sales': p['sales'], 'cat': p['cat'], 'img': p['img']})
    return result

def sp_prods(brand_name, top=3):
    prods = sp_brand_idx.get(brand_name,[])[:top]
    result = []
    for p in prods:
        zh = sp_trans.get(p['title'], p['title'])[:38]
        result.append({'zh': zh, 'price': str(p.get('price','')), 'sales': str(p['sales']), 'cat': p['cat'], 'img': p.get('img','')})
    return result

def merge_prods(tt_list, sp_list):
    """合并TT和SP产品，最多取3条"""
    merged = []
    for p in tt_list:
        merged.append({**p, 'platform': 'TikTok'})
    for p in sp_list:
        merged.append({**p, 'platform': 'Shopee'})
    return merged[:3]

# 30个品牌数据
BRANDS = [
    {
        "name": "OUKEYA",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok", "Shopee"],
        "cats": ["唇部","腮红","眼线","眉部","高光修容"],
        "tags": ["平价爆款","买一送一","TikTok密集","本土品牌"],
        "tt_shop": "Oukeya Thailand Shop",
        "sp_brand": None,
        "tt_sales": "344k+",
        "sp_sales": "少量",
        "audience": "18-30岁泰国年轻女性，追求高性价比与社交媒体潮流，喜欢彩妆叠涂和多用途产品",
        "strategy": "买一送一高折扣引流 + TikTok达人佣金15%驱动，多品类矩阵铺量",
    },
    {
        "name": "Music Flower",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok", "Shopee"],
        "cats": ["粉底遮瑕","眼线"],
        "tags": ["极致性价比","彩妆专家","中国出海","防水卖点"],
        "tt_shop": "Music Flower Thailand",
        "sp_brand": None,
        "tt_sales": "319k+",
        "sp_sales": "少量",
        "audience": "20-35岁追求轻薄底妆的都市女性，注重防水控油，适合泰国热带气候，价格敏感型",
        "strategy": "极致性价比(฿109) + 轻薄防水功效精准切需，10%佣金稳定达人合作",
    },
    {
        "name": "JMCY Beauty",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok"],
        "cats": ["眼线","眉部","睫毛膏","高光修容"],
        "tags": ["技术卖点","眼妆专家","中国出海","精准客群"],
        "tt_shop": "JMCY Beauty.TH",
        "sp_brand": None,
        "tt_sales": "308k+",
        "sp_sales": "-",
        "audience": "18-28岁精致妆容追求者，注重技术卖点（0.01mm细度/12h持久），接受中等价位",
        "strategy": "技术卖点差异化 + 中低佣金(8%)精选优质达人，眼妆品类深度聚焦",
    },
    {
        "name": "Kathy Amrez",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok", "Shopee"],
        "cats": ["腮红","唇部","高光修容"],
        "tags": ["亮泽系","腮红王","本土网红","平价好色"],
        "tt_shop": "Kathy Cosmetics",
        "sp_brand": None,
        "tt_sales": "286k+",
        "sp_sales": "少量",
        "audience": "18-28岁喜爱亮泽妆容的年轻女性，关注KOL推荐，购买决策受达人种草驱动",
        "strategy": "KOL深度绑定 + 单品爆款策略，腮红棒系列为核心引流款",
    },
    {
        "name": "NOWNOW (Mermaid Eye)",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["眉部","睫毛膏","散粉"],
        "tags": ["眉笔爆款","精准功效","TikTok密集","高佣金"],
        "tt_shop": "Nownow shop 000",
        "sp_brand": None,
        "tt_sales": "241k+",
        "sp_sales": "-",
        "audience": "18-30岁注重眉形管理的泰国女性，偏好防水持久型眉妆，日常妆容用户",
        "strategy": "眉笔单品爆款突破，高佣金达人矩阵，低SKU高转化策略",
    },
    {
        "name": "BEAUTILAB",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok", "Shopee"],
        "cats": ["遮瑕","定妆喷雾"],
        "tags": ["遮瑕专家","美白卖点","双平台","高复购"],
        "tt_shop": "drpongshop",
        "sp_brand": "BEAUTILAB",
        "tt_sales": "231k+",
        "sp_sales": "60k+",
        "audience": "20-35岁注重遮瑕美白效果的泰国女性，有瑕疵肌肤困扰，对医美背书品牌信任度高",
        "strategy": "A2P亮白技术背书 + 双平台布局，Shopee店铺评分驱动复购",
    },
    {
        "name": "Global Future Mall",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["眉部","睫毛膏"],
        "tags": ["眉妆达人","高销量","TikTok主攻"],
        "tt_shop": "Global future mall",
        "sp_brand": None,
        "tt_sales": "118k+",
        "sp_sales": "-",
        "audience": "18-30岁关注眉妆的泰国年轻女性，日常妆感需求，性价比导向",
        "strategy": "高佣金达人合作，眉部专项品类集中突破",
    },
    {
        "name": "DAZZLE ME",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok", "Shopee"],
        "cats": ["定妆喷雾","睫毛膏","唇部"],
        "tags": ["联名款","时尚定位","本土中高端","内容营销"],
        "tt_shop": "DAZZLE ME_TH",
        "sp_brand": None,
        "tt_sales": "121k+",
        "sp_sales": "少量",
        "audience": "22-35岁追求时尚感的都市女性，关注联名限定款，愿意为设计和品牌溢价付费",
        "strategy": "IP联名(Barbie等)制造话题 + 社交媒体内容营销，走中高端品牌路线",
    },
    {
        "name": "Luminee Beauty",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["高光修容","眼线","睫毛膏"],
        "tags": ["高光专家","买一送多","入门友好","高佣金"],
        "tt_shop": "LumineeBeauty TH",
        "sp_brand": None,
        "tt_sales": "120k+",
        "sp_sales": "-",
        "audience": "16-28岁彩妆初学者，喜欢简单易上手的修容产品，对买赠活动响应度高",
        "strategy": "买一送五策略拉高性价比感知 + 低门槛产品设计吸引新手用户",
    },
    {
        "name": "LUCKGO",
        "origin": "泰国/东南亚",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["眉部","睫毛膏","散粉"],
        "tags": ["东南亚布局","平价多品","TikTok主力"],
        "tt_shop": "LUCKGO Thailand Shop",
        "sp_brand": None,
        "tt_sales": "119k+",
        "sp_sales": "-",
        "audience": "18-30岁泰国年轻女性，追求高性价比彩妆，线上购物主力用户",
        "strategy": "平价多SKU策略，TikTok达人矩阵密集投放",
    },
    {
        "name": "MAYBELLINE",
        "origin": "国际",
        "origin_class": "intl",
        "channels": ["TikTok", "Shopee"],
        "cats": ["粉底遮瑕","唇部","睫毛膏"],
        "tags": ["国际大牌","技术背书","双平台","稳定复购"],
        "tt_shop": "Maybelline TH",
        "sp_brand": "MAYBELLINE",
        "tt_sales": "105k+",
        "sp_sales": "30k+",
        "audience": "22-40岁有品牌意识的泰国女性，信任国际专业品牌，重视产品稳定性和口碑",
        "strategy": "国际品牌背书 + 双平台全渠道覆盖，专柜同款线上平价版策略",
    },
    {
        "name": "AURA RICH",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["眉部","眼线","唇部"],
        "tags": ["泰国网红品牌","CEO亲自带货","高复购","达人绑定"],
        "tt_shop": "CEO Aura Rich",
        "sp_brand": None,
        "tt_sales": "94k+",
        "sp_sales": "-",
        "audience": "18-28岁跟随网红妆容的泰国年轻女性，KOL推荐转化率高",
        "strategy": "创始人/CEO亲自出镜带货，形成强人设IP，达人矩阵二次扩散",
    },
    {
        "name": "LAMEILA (via UFHKO)",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok"],
        "cats": ["散粉","BB/CC霜","粉底遮瑕"],
        "tags": ["超平价","中国制造","底妆专攻","高性价比"],
        "tt_shop": "UFHKO",
        "sp_brand": None,
        "tt_sales": "85k+",
        "sp_sales": "-",
        "audience": "18-30岁价格极度敏感的年轻用户，首次彩妆尝试者，对品牌忠诚度低",
        "strategy": "极低定价策略(฿29-59)，以散粉/BB霜超高性价比快速获量",
    },
    {
        "name": "MERMAID CARE",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["眉部","眼线"],
        "tags": ["眉妆爆款","防水卖点","泰国本土","高佣金"],
        "tt_shop": "MERMAID CARE",
        "sp_brand": None,
        "tt_sales": "107k+",
        "sp_sales": "-",
        "audience": "18-30岁注重防水眉妆的泰国女性，热带气候场景驱动购买决策",
        "strategy": "聚焦防水场景卖点，眉笔单品高转化，达人体验视频驱动种草",
    },
    {
        "name": "Flortte",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok"],
        "cats": ["唇部","腮红","眼影"],
        "tags": ["中国出海新锐","少女感","甜系设计","品牌调性强"],
        "tt_shop": "FlortteBeauty",
        "sp_brand": None,
        "tt_sales": "41k+",
        "sp_sales": "-",
        "audience": "16-25岁喜欢甜美少女感妆容的年轻用户，对颜值经济敏感，愿意尝试新中国品牌",
        "strategy": "甜系包装设计吸引年轻用户，TikTok种草内容为主，平价高颜值定位",
    },
    {
        "name": "SUPERMOM",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee", "TikTok"],
        "cats": ["粉底","BB/CC霜"],
        "tags": ["Shopee主力","孕产妇友好","温和配方","本土品牌"],
        "tt_shop": "SUPERMOM COSMETICS",
        "sp_brand": "SUPERMOM",
        "tt_sales": "少量",
        "sp_sales": "60k+",
        "audience": "25-40岁泰国妈妈群体及注重温和配方的女性，在Shopee上活跃购物，偏好安全成分",
        "strategy": "温和/孕期可用卖点，Shopee深耕，口碑评价驱动，促销节日集中爆发",
    },
    {
        "name": "hince",
        "origin": "韩国",
        "origin_class": "kr",
        "channels": ["Shopee"],
        "cats": ["唇部","腮红"],
        "tags": ["韩国小众","高端定位","哑光质地","设计感强"],
        "tt_shop": None,
        "sp_brand": "hince",
        "tt_sales": "-",
        "sp_sales": "30k+",
        "audience": "22-35岁有韩妆偏好的泰国都市女性，关注小众高端品牌，有一定消费能力",
        "strategy": "韩国小众品牌高溢价，Shopee旗舰店官方背书，质感营销为主",
    },
    {
        "name": "CANMAKE",
        "origin": "日本",
        "origin_class": "jp",
        "channels": ["Shopee", "TikTok"],
        "cats": ["腮红","眉部","睫毛膏"],
        "tags": ["日系可爱","平价日妆","Shopee主力","高复购"],
        "tt_shop": None,
        "sp_brand": "CANMAKE",
        "tt_sales": "少量",
        "sp_sales": "20k+",
        "audience": "18-30岁喜爱日系妆容风格的泰国女性，注重产品品质与日本品牌信任感",
        "strategy": "日系可爱包装+平价策略，Shopee粉丝沉淀，系列化产品促进复购",
    },
    {
        "name": "MizuMi",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee"],
        "cats": ["唇部","腮红"],
        "tags": ["泰国中高端","精致定位","Shopee主力","唇妆专家"],
        "tt_shop": None,
        "sp_brand": "MizuMi",
        "tt_sales": "-",
        "sp_sales": "30k+",
        "audience": "25-38岁注重品质感的泰国都市女性，愿意为好设计和好品质支付溢价",
        "strategy": "泰国本土中高端定位，精致包装+高口碑评分，Shopee官方旗舰深耕",
    },
    {
        "name": "KATE",
        "origin": "日本",
        "origin_class": "jp",
        "channels": ["Shopee"],
        "cats": ["眉部","眼线","粉底"],
        "tags": ["日妆经典","眉妆专家","专业定位","长效持妆"],
        "tt_shop": None,
        "sp_brand": "KATE",
        "tt_sales": "-",
        "sp_sales": "20k+",
        "audience": "22-40岁注重眉妆精准的职业泰国女性，有日妆消费习惯，重视专业产品效果",
        "strategy": "日本专业品牌定位，眉部产品为王牌，Shopee旗舰保证正品信任",
    },
    {
        "name": "ROM&ND",
        "origin": "韩国",
        "origin_class": "kr",
        "channels": ["Shopee", "TikTok"],
        "cats": ["唇部","腮红","眉部"],
        "tags": ["韩妆热门","Juicy系列","高颜值","双平台"],
        "tt_shop": None,
        "sp_brand": "Rom&nd",
        "tt_sales": "少量",
        "sp_sales": "20k+",
        "audience": "18-30岁韩妆爱好者，追求韩系清透妆容，对韩国明星同款高度关注",
        "strategy": "明星同款/剧同款营销，唇釉产品为流量入口，双平台官方店保障正品",
    },
    {
        "name": "LA GLACE",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee", "TikTok"],
        "cats": ["腮红","睫毛膏","遮瑕"],
        "tags": ["泰国本土","多品类","性价比","Shopee活跃"],
        "tt_shop": "LA GLACE",
        "sp_brand": "LA GLACE",
        "tt_sales": "31k+",
        "sp_sales": "30k+",
        "audience": "18-32岁注重性价比的泰国女性，喜欢一站式购买多品类彩妆",
        "strategy": "多品类平铺 + Shopee大促爆发，腮红/睫毛膏为核心引流品",
    },
    {
        "name": "4U2",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee"],
        "cats": ["唇部","眼线","眉部"],
        "tags": ["泰国老牌","药妆渠道","稳健经营","高口碑"],
        "tt_shop": None,
        "sp_brand": "4U2",
        "tt_sales": "-",
        "sp_sales": "20k+",
        "audience": "25-45岁对泰国老牌彩妆有信任感的女性，药妆店忠实用户，注重品质稳定",
        "strategy": "药妆渠道+线上双驱动，品牌历史背书+口碑积累，稳价策略维护品牌形象",
    },
    {
        "name": "Cathy Doll",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee", "TikTok"],
        "cats": ["唇部","粉底","BB/CC霜"],
        "tags": ["泰国知名","BB霜经典","双平台","大众市场"],
        "tt_shop": None,
        "sp_brand": "Cathy Doll",
        "tt_sales": "少量",
        "sp_sales": "20k+",
        "audience": "18-35岁追求懒人妆的泰国女性，偏好BB霜/气垫等一步到位底妆产品",
        "strategy": "BB霜/气垫一步妆核心单品策略，大众渠道广泛铺货，促销节点集中爆发",
    },
    {
        "name": "SHIHAN Beauty",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok"],
        "cats": ["腮红","眼影","眼线"],
        "tags": ["腮红棒爆款","中国出海","彩妆组合","高性价比"],
        "tt_shop": "shihan",
        "sp_brand": None,
        "tt_sales": "83k+",
        "sp_sales": "-",
        "audience": "18-28岁喜欢彩色腮红和创意眼妆的年轻用户，TikTok种草驱动购买",
        "strategy": "腮红棒单品爆款切入，眼影联动销售，TikTok达人色彩演示效果强",
    },
    {
        "name": "LIGHT YOU",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["高光修容","粉底"],
        "tags": ["高光专家","提亮卖点","TikTok爆款","本土新锐"],
        "tt_shop": "LIGHT YOU OFFICIAL",
        "sp_brand": None,
        "tt_sales": "65k+",
        "sp_sales": "-",
        "audience": "18-30岁追求发光肌底妆效果的泰国年轻女性，TikTok高光视频驱动购买欲",
        "strategy": "高光提亮效果可视化展示，TikTok前后对比视频为核心转化内容",
    },
    {
        "name": "MAKNE Cosmetics",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["腮红","唇部","高光修容"],
        "tags": ["泰国新锐","高性价比","彩妆多品","达人合作"],
        "tt_shop": "makne cosmetics",
        "sp_brand": None,
        "tt_sales": "62k+",
        "sp_sales": "-",
        "audience": "16-28岁尝试丰富彩妆品类的泰国年轻用户，价格敏感，追求彩妆新鲜感",
        "strategy": "多品类低价策略，TikTok达人体验型内容，持续推出新品保持用户新鲜感",
    },
    {
        "name": "WANNASA",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["TikTok"],
        "cats": ["粉底","腮红","唇部"],
        "tags": ["泰国本土","底妆专注","高销速","达人矩阵"],
        "tt_shop": "WANNASA COSMETICS11",
        "sp_brand": None,
        "tt_sales": "54k+",
        "sp_sales": "-",
        "audience": "20-35岁注重底妆效果的泰国女性，TikTok妆容教程受众，日常妆容需求",
        "strategy": "底妆系列为主打，TikTok达人教程型内容种草，注重效果展示",
    },
    {
        "name": "PINKFLASH",
        "origin": "中国出海",
        "origin_class": "china",
        "channels": ["TikTok", "Shopee"],
        "cats": ["唇部","腮红","眼影","粉底"],
        "tags": ["超低价","中国出海","全品类","高量低价"],
        "tt_shop": "PINKFLASH.TH",
        "sp_brand": None,
        "tt_sales": "30k+",
        "sp_sales": "少量",
        "audience": "16-25岁极致价格敏感的年轻用户，初次彩妆尝试者，追求低成本高颜值",
        "strategy": "全品类超低价(฿29起)策略，快速获量，以量取胜的中国出海平价路线",
    },
    {
        "name": "CUTE PRESS",
        "origin": "泰国本土",
        "origin_class": "local",
        "channels": ["Shopee", "TikTok"],
        "cats": ["定妆喷雾","粉底","唇部"],
        "tags": ["泰国老牌","全渠道","药妆经典","稳健品牌"],
        "tt_shop": "Cute Press",
        "sp_brand": "CUTE PRESS",
        "tt_sales": "少量",
        "sp_sales": "少量",
        "audience": "20-45岁对泰国本土老牌有信任感的女性，线上线下双渠道用户，品牌忠诚度高",
        "strategy": "泰国本土老牌情怀背书，全渠道铺货，大促节点集中冲量，稳定价格维护品牌",
    },
]

def make_product_card(prod, rank):
    platform = prod.get('platform', 'TikTok')
    pt_color = '#ff6b35' if platform == 'TikTok' else '#f97316'
    pt_bg = '#fff4f0' if platform == 'TikTok' else '#fff8f0'
    pt_icon = '&#9654;' if platform == 'TikTok' else '&#127873;'
    
    sales_str = prod.get('sales', '')
    if isinstance(sales_str, int):
        sales_str = f'{sales_str:,}'
    else:
        sales_str = str(sales_str)
    
    price_str = prod.get('price', '')
    if price_str and not str(price_str).startswith('฿') and not str(price_str).startswith('&#3647;'):
        price_str = f'&#3647;{price_str}'
    
    img_url = prod.get('img', '')
    cat = prod.get('cat', '')
    zh_name = prod.get('zh', '')
    
    rank_badge = ''
    if rank == 1:
        rank_badge = '<span style="background:#ff6b35;color:#fff;font-size:10px;padding:1px 6px;border-radius:8px;font-weight:700;margin-right:6px">#1</span>'
    elif rank == 2:
        rank_badge = '<span style="background:#f97316;color:#fff;font-size:10px;padding:1px 6px;border-radius:8px;font-weight:700;margin-right:6px">#2</span>'
    elif rank == 3:
        rank_badge = '<span style="background:#94a3b8;color:#fff;font-size:10px;padding:1px 6px;border-radius:8px;font-weight:700;margin-right:6px">#3</span>'
    
    img_html = ''
    if img_url:
        img_html = f'<img src="{img_url}" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'" style="width:52px;height:52px;object-fit:cover;border-radius:8px;flex-shrink:0" />'
        img_html += f'<div style="display:none;width:52px;height:52px;background:#f1f5f9;border-radius:8px;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">&#127777;</div>'
    else:
        img_html = f'<div style="width:52px;height:52px;background:#f1f5f9;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0">&#127777;</div>'

    return f'''
        <div style="display:flex;align-items:center;gap:10px;padding:8px 10px;background:#f8fafc;border-radius:10px;margin-bottom:6px;border:1px solid #e2e8f0">
          {img_html}
          <div style="flex:1;min-width:0">
            <div style="display:flex;align-items:center;margin-bottom:3px">
              {rank_badge}
              <span style="background:{pt_bg};color:{pt_color};font-size:10px;padding:1px 5px;border-radius:4px;margin-right:5px">{pt_icon} {platform}</span>
              <span style="background:#f0fdf4;color:#16a34a;font-size:10px;padding:1px 5px;border-radius:4px">{cat}</span>
            </div>
            <div style="font-size:12px;color:#374151;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="{zh_name}">{zh_name}</div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:3px">
              <span style="color:#f97316;font-weight:700;font-size:12px">{price_str}</span>
              <span style="color:#64748b;font-size:11px">&#128200; {sales_str}</span>
            </div>
          </div>
        </div>'''

def make_brand_card(b, idx):
    # 获取产品列表
    prods = []
    if b.get('tt_shop'):
        tt_list = tt_prods(b['tt_shop'])
        for p in tt_list:
            prods.append({**p, 'platform': 'TikTok'})
    if b.get('sp_brand'):
        sp_list = sp_prods(b['sp_brand'])
        for p in sp_list:
            prods.append({**p, 'platform': 'Shopee'})
    prods = prods[:3]
    
    # 颜色配置
    origin_configs = {
        'local': ('泰国本土', '#10b981', '#ecfdf5'),
        'china': ('中国出海', '#f97316', '#fff7ed'),
        'kr':    ('韩国品牌', '#6366f1', '#eef2ff'),
        'jp':    ('日本品牌', '#ec4899', '#fdf2f8'),
        'intl':  ('国际品牌', '#8b5cf6', '#f5f3ff'),
    }
    origin_class = b.get('origin_class', 'local')
    origin_label, origin_color, origin_bg = origin_configs.get(origin_class, ('本土', '#10b981', '#ecfdf5'))
    
    channels = b.get('channels', [])
    has_tt = 'TikTok' in channels
    has_sp = 'Shopee' in channels
    
    tt_sales = b.get('tt_sales', '-')
    sp_sales = b.get('sp_sales', '-')
    
    # 销量条
    def parse_sales(s):
        if not s or s in ['-', '少量']: return 0
        s = s.replace('k+','').replace('k','').replace('+','').strip()
        try: return float(s)
        except: return 0
    
    max_sales = 344
    tt_val = parse_sales(tt_sales)
    sp_val = parse_sales(sp_sales)
    tt_pct = min(100, int(tt_val / max_sales * 100))
    sp_pct = min(100, int(sp_val / max_sales * 100))
    
    channel_html = ''
    if has_tt:
        channel_html += f'<span style="background:#fff4f0;color:#ff6b35;font-size:11px;padding:2px 8px;border-radius:6px;font-weight:600">&#9654; TikTok</span> '
    if has_sp:
        channel_html += f'<span style="background:#fff8f0;color:#f97316;font-size:11px;padding:2px 8px;border-radius:6px;font-weight:600">&#127873; Shopee</span> '
    
    cats_html = ''.join([f'<span style="background:#f0f9ff;color:#0369a1;font-size:10px;padding:2px 6px;border-radius:5px;margin:2px">{c}</span>' for c in b.get('cats',[])])
    tags_html = ''.join([f'<span style="background:#faf5ff;color:#7c3aed;font-size:10px;padding:2px 6px;border-radius:5px;margin:2px">{t}</span>' for t in b.get('tags',[])])
    
    products_html = ''.join([make_product_card(p, i+1) for i, p in enumerate(prods)])
    if not products_html:
        products_html = '<div style="text-align:center;color:#94a3b8;font-size:12px;padding:16px">暂无产品数据</div>'
    
    # 渠道筛选数据属性
    filter_attrs = 'data-filter="all'
    if has_tt and has_sp: filter_attrs += ' dual'
    elif has_tt: filter_attrs += ' tiktok'
    elif has_sp: filter_attrs += ' shopee'
    if has_tt and has_sp: filter_attrs += ' tiktok shopee'
    filter_attrs += f' {origin_class}"'
    
    return f'''
    <div class="brand-card" {filter_attrs} style="background:#fff;border-radius:16px;padding:20px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.06);transition:all 0.2s" onmouseover="this.style.boxShadow='0 8px 24px rgba(0,0,0,0.12)';this.style.transform='translateY(-2px)'" onmouseout="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.06)';this.style.transform='none'">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
        <div>
          <div style="font-size:16px;font-weight:700;color:#1e293b;margin-bottom:4px">{b['name']}</div>
          <span style="background:{origin_bg};color:{origin_color};font-size:11px;padding:2px 8px;border-radius:10px;font-weight:600">{b['origin']}</span>
        </div>
        <div style="background:#f1f5f9;color:#64748b;font-size:12px;font-weight:700;padding:4px 10px;border-radius:8px">#{idx} 综合榜</div>
      </div>
      
      <div style="margin-bottom:10px">{channel_html}</div>
      <div style="margin-bottom:10px">{cats_html}</div>
      <div style="margin-bottom:12px">{tags_html}</div>
      
      <div style="margin-bottom:12px">
        <div style="font-size:12px;font-weight:600;color:#374151;margin-bottom:8px">&#128293; 热销产品</div>
        {products_html}
      </div>
      
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px">
        <div style="background:#fff4f0;border-radius:8px;padding:8px">
          <div style="font-size:10px;color:#ff6b35;margin-bottom:4px">&#9654; TikTok月销</div>
          <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:4px">{tt_sales}</div>
          <div style="background:#ffe4d6;border-radius:4px;height:4px"><div style="background:#ff6b35;border-radius:4px;height:4px;width:{tt_pct}%"></div></div>
        </div>
        <div style="background:#fff8f0;border-radius:8px;padding:8px">
          <div style="font-size:10px;color:#f97316;margin-bottom:4px">&#127873; Shopee月销</div>
          <div style="font-size:13px;font-weight:700;color:#1e293b;margin-bottom:4px">{sp_sales}</div>
          <div style="background:#fed7aa;border-radius:4px;height:4px"><div style="background:#f97316;border-radius:4px;height:4px;width:{sp_pct}%"></div></div>
        </div>
      </div>
      
      <div style="background:#f8fafc;border-radius:8px;padding:10px;margin-bottom:8px">
        <div style="font-size:11px;color:#64748b;margin-bottom:3px">&#128101; 消费人群</div>
        <div style="font-size:12px;color:#374151;line-height:1.5">{b.get('audience','')}</div>
      </div>
      <div style="background:#fefce8;border-radius:8px;padding:10px">
        <div style="font-size:11px;color:#a16207;margin-bottom:3px">&#128161; 运营策略</div>
        <div style="font-size:12px;color:#374151;line-height:1.5">{b.get('strategy','')}</div>
      </div>
    </div>'''

# 生成所有卡片
cards_html = ''
for i, b in enumerate(BRANDS):
    cards_html += make_brand_card(b, i+1)

# 统计
n_local = sum(1 for b in BRANDS if b['origin_class']=='local')
n_china = sum(1 for b in BRANDS if b['origin_class']=='china')
n_kr    = sum(1 for b in BRANDS if b['origin_class']=='kr')
n_jp    = sum(1 for b in BRANDS if b['origin_class']=='jp')
n_intl  = sum(1 for b in BRANDS if b['origin_class']=='intl')
n_tt    = sum(1 for b in BRANDS if 'TikTok' in b['channels'])
n_sp    = sum(1 for b in BRANDS if 'Shopee' in b['channels'])
n_dual  = sum(1 for b in BRANDS if 'TikTok' in b['channels'] and 'Shopee' in b['channels'])

HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>泰国美妆热门品牌全景分析 - 30品牌版</title>
<style>
  * {{ box-sizing:border-box; margin:0; padding:0 }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif; background:#f8fafc; color:#1e293b }}
  .brand-card {{ break-inside:avoid }}
  .filter-btn {{ cursor:pointer; border:none; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600; transition:all 0.2s; background:#f1f5f9; color:#64748b }}
  .filter-btn.active {{ background:#ff6b35; color:#fff }}
  .filter-btn:hover {{ background:#e2e8f0 }}
  .filter-btn.active:hover {{ background:#ea5a28 }}
  #brand-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:20px }}
  .hidden {{ display:none !important }}
</style>
</head>
<body>
<div style="background:linear-gradient(135deg,#fff5f0 0%,#fff8f5 50%,#fff 100%);border-bottom:1px solid #ffe4d6;padding:24px 32px">
  <div style="max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between">
    <div>
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px">
        <div style="width:40px;height:40px;background:linear-gradient(135deg,#ff6b35,#f97316);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">&#127775;</div>
        <h1 style="font-size:24px;font-weight:800;color:#1e293b">泰国美妆热门品牌全景分析</h1>
      </div>
      <div style="color:#64748b;font-size:13px">Thailand Beauty Brand Intelligence &nbsp;&#8226;&nbsp; Shopee &#215; TikTok 双平台数据 &nbsp;&#8226;&nbsp; 2026年4月 &nbsp;&#8226;&nbsp; 共 <strong>30</strong> 个品牌</div>
    </div>
    <div style="display:flex;gap:16px">
      <div style="background:#fff;border-radius:12px;padding:12px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:22px;font-weight:800;color:#ff6b35">{n_tt}</div>
        <div style="font-size:11px;color:#64748b">TikTok品牌</div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:12px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:22px;font-weight:800;color:#f97316">{n_sp}</div>
        <div style="font-size:11px;color:#64748b">Shopee品牌</div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:12px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:22px;font-weight:800;color:#10b981">{n_local}</div>
        <div style="font-size:11px;color:#64748b">泰国本土</div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:12px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:22px;font-weight:800;color:#f97316">{n_china}</div>
        <div style="font-size:11px;color:#64748b">中国出海</div>
      </div>
      <div style="background:#fff;border-radius:12px;padding:12px 20px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="font-size:22px;font-weight:800;color:#6366f1">{n_kr + n_jp + n_intl}</div>
        <div style="font-size:11px;color:#64748b">国际韩日</div>
      </div>
    </div>
  </div>
</div>

<div style="max-width:1400px;margin:24px auto;padding:0 24px">
  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:24px">
    <span style="font-size:13px;color:#64748b;font-weight:600">筛选：</span>
    <button class="filter-btn active" onclick="filterBrands('all',this)">全部品牌</button>
    <button class="filter-btn" onclick="filterBrands('tiktok',this)">&#9654; TikTok</button>
    <button class="filter-btn" onclick="filterBrands('shopee',this)">&#127873; Shopee</button>
    <button class="filter-btn" onclick="filterBrands('dual',this)">双平台</button>
    <button class="filter-btn" onclick="filterBrands('local',this)">泰国本土品牌</button>
    <button class="filter-btn" onclick="filterBrands('china',this)">中国出海品牌</button>
    <button class="filter-btn" onclick="filterBrands('kr',this)">韩国品牌</button>
    <button class="filter-btn" onclick="filterBrands('jp',this)">日本品牌</button>
    <button class="filter-btn" onclick="filterBrands('intl',this)">国际品牌</button>
    <span id="count-label" style="margin-left:auto;font-size:12px;color:#94a3b8">共 30 个品牌 · 按综合销量排序</span>
  </div>
  
  <div style="margin-bottom:16px">
    <div style="display:inline-flex;align-items:center;gap:8px;background:#fff;border-radius:10px;padding:10px 16px;border:1px solid #e2e8f0">
      <span style="font-size:16px">&#127942;</span>
      <span style="font-size:14px;font-weight:700;color:#1e293b">品牌详细分析卡</span>
    </div>
  </div>

  <div id="brand-grid">
    {cards_html}
  </div>
  
  <div style="text-align:center;padding:32px 0;color:#94a3b8;font-size:12px">
    数据来源：Shopee泰国 & TikTok Shop泰国 &nbsp;&#8226;&nbsp; 统计周期：2026年4月 &nbsp;&#8226;&nbsp; 仅供内部培训参考
  </div>
</div>

<script>
function filterBrands(type, btn) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  
  const cards = document.querySelectorAll('.brand-card');
  let count = 0;
  cards.forEach(card => {{
    const filters = card.getAttribute('data-filter') || '';
    if (type === 'all' || filters.includes(type)) {{
      card.classList.remove('hidden');
      count++;
    }} else {{
      card.classList.add('hidden');
    }}
  }});
  document.getElementById('count-label').textContent = `共 ${{count}} 个品牌 · 按综合销量排序`;
}}
</script>
</body>
</html>"""

out_path = r'E:\泰国市场重点分析\泰国美妆热门品牌分析.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'Done! -> {out_path}')
print(f'Brands: {len(BRANDS)}')
