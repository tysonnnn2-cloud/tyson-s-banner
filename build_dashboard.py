import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\泰国市场重点分析\processed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

icons = {
    '唇部': '💄',
    '粉底': '🫙',
    '腮红': '🌸',
    '睫毛膏': '👁️',
    '遮瑕': '✨',
    '定妆喷雾': '💨',
}

lines = []

lines.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泰国Shopee美妆热销产品看板</title>
<style>
:root{--bg:#0f0f1a;--panel:#181828;--card:#1e1e32;--card-hover:#252540;--accent:#ff6b9d;--accent2:#c44dff;--accent3:#4dc9ff;--gold:#ffd700;--text:#f0f0ff;--muted:#8888aa;--border:rgba(255,255,255,0.08);--shopee:#ee4d2d;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Microsoft YaHei','PingFang SC',-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}
.header{background:linear-gradient(135deg,#1a0a2e 0%,#16213e 50%,#0f3460 100%);border-bottom:1px solid rgba(196,77,255,0.3);padding:20px 40px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;}
.header-left{display:flex;align-items:center;gap:16px;}
.shopee-badge{background:var(--shopee);color:white;font-size:12px;font-weight:700;padding:4px 10px;border-radius:4px;letter-spacing:1px;}
.header h1{font-size:22px;font-weight:700;background:linear-gradient(90deg,#ff6b9d,#c44dff,#4dc9ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.header-meta{display:flex;gap:20px;align-items:center;}
.header-stat{text-align:center;}
.header-stat .val{font-size:20px;font-weight:700;color:var(--gold);}
.header-stat .lbl{font-size:11px;color:var(--muted);}
.flag{font-size:28px;}
.tabs-wrapper{background:var(--panel);border-bottom:1px solid var(--border);padding:0 40px;position:sticky;top:73px;z-index:99;}
.tabs{display:flex;gap:0;overflow-x:auto;scrollbar-width:none;}
.tabs::-webkit-scrollbar{display:none;}
.tab{padding:14px 22px;cursor:pointer;font-size:14px;font-weight:600;color:var(--muted);white-space:nowrap;border-bottom:2px solid transparent;transition:all 0.2s;display:flex;align-items:center;gap:8px;}
.tab:hover{color:var(--text);}
.tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.tab-count{background:rgba(255,107,157,0.15);color:var(--accent);font-size:11px;padding:1px 7px;border-radius:10px;}
.content{padding:30px 40px;}
.panel{display:none;}
.panel.active{display:block;}
.stats-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px;}
.stat-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 20px;position:relative;overflow:hidden;}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent2));}
.stat-card .icon{font-size:22px;margin-bottom:8px;}
.stat-card .val{font-size:26px;font-weight:800;color:var(--gold);}
.stat-card .lbl{font-size:12px;color:var(--muted);margin-top:2px;}
.section-title{display:flex;align-items:center;gap:12px;margin-bottom:20px;}
.section-title h2{font-size:18px;font-weight:700;}
.section-title .line{flex:1;height:1px;background:var(--border);}
.section-title .badge{font-size:12px;color:var(--muted);background:var(--card);border:1px solid var(--border);padding:3px 10px;border-radius:20px;}
.product-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;}
.product-card{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;transition:all 0.25s;position:relative;}
.product-card:hover{transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,0.4);border-color:rgba(255,107,157,0.3);background:var(--card-hover);}
.rank-badge{position:absolute;top:10px;left:10px;z-index:10;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:white;}
.rank-1{background:linear-gradient(135deg,#ffd700,#ff8c00);box-shadow:0 2px 8px rgba(255,215,0,0.5);}
.rank-2{background:linear-gradient(135deg,#c0c0c0,#808080);}
.rank-3{background:linear-gradient(135deg,#cd7f32,#8b4513);}
.rank-n{background:rgba(255,255,255,0.1);font-size:10px;}
.product-img-wrap{width:100%;height:200px;background:#111122;overflow:hidden;position:relative;}
.product-img{width:100%;height:100%;object-fit:cover;transition:transform 0.3s;}
.product-card:hover .product-img{transform:scale(1.05);}
.img-placeholder{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:48px;background:linear-gradient(135deg,#1a1a2e,#16213e);}
.discount-tag{position:absolute;top:10px;right:10px;background:var(--shopee);color:white;font-size:11px;font-weight:700;padding:3px 7px;border-radius:4px;}
.product-body{padding:14px;}
.brand-row{display:flex;align-items:center;gap:6px;margin-bottom:6px;flex-wrap:wrap;}
.brand-tag{font-size:11px;font-weight:700;color:var(--accent2);background:rgba(196,77,255,0.1);border:1px solid rgba(196,77,255,0.2);padding:2px 8px;border-radius:4px;white-space:nowrap;max-width:140px;overflow:hidden;text-overflow:ellipsis;}
.promo-tag{font-size:10px;color:var(--gold);background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.2);padding:2px 6px;border-radius:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90px;}
.product-title{font-size:12px;color:#ccccee;line-height:1.45;margin-bottom:10px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.price{font-size:18px;font-weight:800;color:var(--shopee);}
.metrics-row{display:flex;gap:10px;align-items:center;margin-top:6px;flex-wrap:wrap;}
.metric{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--muted);}
.metric.rating{color:var(--gold);font-weight:600;}
.metric.sales{color:var(--accent3);font-weight:600;}
.view-toggle{display:flex;gap:8px;margin-bottom:20px;justify-content:flex-end;}
.view-btn{padding:6px 14px;border-radius:6px;border:1px solid var(--border);background:var(--card);color:var(--muted);font-size:12px;cursor:pointer;transition:all 0.2s;}
.view-btn.active,.view-btn:hover{border-color:var(--accent);color:var(--accent);background:rgba(255,107,157,0.08);}
.table-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;font-size:13px;}
thead tr{background:rgba(196,77,255,0.1);border-bottom:1px solid rgba(196,77,255,0.2);}
th{padding:12px 14px;text-align:left;font-size:12px;font-weight:700;color:var(--muted);letter-spacing:0.5px;text-transform:uppercase;white-space:nowrap;}
tbody tr{border-bottom:1px solid var(--border);transition:background 0.15s;}
tbody tr:hover{background:var(--card-hover);}
td{padding:10px 14px;vertical-align:middle;}
td.thumb img{width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid var(--border);}
td.rank-td{font-size:14px;font-weight:800;color:var(--muted);text-align:center;width:40px;}
td.rank-td.top3{color:var(--gold);}
td.title-td{max-width:280px;}
td.title-td .tl{font-size:12px;color:var(--text);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;line-height:1.4;}
td.price-td{color:var(--shopee);font-weight:700;}
td.sales-td{color:var(--accent3);font-weight:600;}
td.rating-td{color:var(--gold);font-weight:600;}
td.disc-td{color:var(--shopee);font-weight:600;}
.overview-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}
.cat-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px;cursor:pointer;transition:all 0.25s;}
.cat-card:hover{border-color:rgba(255,107,157,0.4);transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,0.3);}
.cat-header{display:flex;align-items:center;gap:10px;margin-bottom:16px;}
.cat-emoji{font-size:28px;}
.cat-name{font-size:16px;font-weight:700;}
.cat-count{font-size:12px;color:var(--muted);}
.top-products{display:flex;flex-direction:column;gap:10px;}
.top-item{display:flex;gap:10px;align-items:center;}
.top-item img{width:44px;height:44px;object-fit:cover;border-radius:8px;border:1px solid var(--border);flex-shrink:0;}
.top-item-info{flex:1;overflow:hidden;}
.top-item-brand{font-size:10px;color:var(--accent2);font-weight:600;}
.top-item-title{font-size:11px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.top-item-sales{font-size:11px;color:var(--accent3);font-weight:600;}
.cat-divider{height:1px;background:var(--border);margin:12px 0;}
.cat-footer{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);}
.cat-footer .val{color:var(--gold);font-weight:600;}
.footer{text-align:center;padding:24px;color:var(--muted);font-size:12px;border-top:1px solid var(--border);margin-top:40px;}
@media(max-width:768px){.header{padding:16px 20px;flex-wrap:wrap;gap:12px;}.content{padding:20px;}.tabs-wrapper{padding:0 20px;}.stats-bar{grid-template-columns:repeat(2,1fr);}.overview-grid{grid-template-columns:1fr;}.product-grid{grid-template-columns:repeat(auto-fill,minmax(170px,1fr));}}
</style>
</head>
<body>""")

lines.append("""<div class="header">
<div class="header-left">
<div class="flag">&#127481;&#127469;</div>
<div>
<div style="display:flex;gap:8px;align-items:center;margin-bottom:4px"><span class="shopee-badge">SHOPEE TH</span></div>
<h1>泰国美妆热销产品看板</h1>
</div>
</div>
<div class="header-meta">
<div class="header-stat"><div class="val">6</div><div class="lbl">热销品类</div></div>
<div class="header-stat"><div class="val">120+</div><div class="lbl">热销产品</div></div>
<div class="header-stat"><div class="val">60k+</div><div class="lbl">月最高销量</div></div>
</div>
</div>""")

# Tabs
tab_parts = ['<div class="tabs-wrapper"><div class="tabs" id="tabs">']
tab_parts.append('<div class="tab active" onclick="switchTab(\'overview\')">&#128202; 总览</div>')
for cat, products in data.items():
    icon_map = {'唇部':'&#128132;','粉底':'&#129803;','腮红':'&#127800;','睫毛膏':'&#128065;️','遮瑕':'&#10024;','定妆喷雾':'&#128168;'}
    ic = icon_map.get(cat, '&#128132;')
    tab_parts.append(f'<div class="tab" onclick="switchTab(\'{cat}\')">{ic} {cat} <span class="tab-count">{len(products)}</span></div>')
tab_parts.append('</div></div>')
lines.append(''.join(tab_parts))

lines.append('<div class="content">')

# Overview panel
ov = ['<div class="panel active" id="panel-overview">']
ov.append("""<div class="stats-bar">
<div class="stat-card"><div class="icon">&#127942;</div><div class="val">60k+</div><div class="lbl">月最高销量（遮瑕/粉底）</div></div>
<div class="stat-card"><div class="icon">&#128176;</div><div class="val">&#3647;1~&#3647;560</div><div class="lbl">热销价格区间（泰铢）</div></div>
<div class="stat-card"><div class="icon">&#11088;</div><div class="val">4.8-5.0</div><div class="lbl">热销产品评分区间</div></div>
<div class="stat-card"><div class="icon">&#127991;</div><div class="val">-50%~-99%</div><div class="lbl">折扣力度范围</div></div>
</div>""")
ov.append('<div class="section-title"><h2>各品类概览</h2><div class="line"></div><div class="badge">点击品类卡片查看详情</div></div>')
ov.append('<div class="overview-grid">')

for cat, products in data.items():
    icon_txt = {'唇部':'💄','粉底':'🫙','腮红':'🌸','睫毛膏':'👁️','遮瑕':'✨','定妆喷雾':'💨'}.get(cat,'💄')
    top3 = products[:3]
    sales_vals = [p['sales_num'] for p in products if p['sales_num'] > 0]
    max_sales = max(sales_vals) if sales_vals else 0
    brands = list(dict.fromkeys([p['brand'] for p in products if p['brand'] not in ('其他品牌','')]))[:3]
    max_sales_str = f'{max_sales//1000}k+' if max_sales >= 1000 else str(max_sales)
    
    cc = [f'<div class="cat-card" onclick="switchTab(\'{cat}\')">']
    cc.append(f'<div class="cat-header"><div class="cat-emoji">{icon_txt}</div><div><div class="cat-name">{cat}</div><div class="cat-count">Top {len(products)} 热销</div></div></div>')
    cc.append('<div class="top-products">')
    for p in top3:
        t = p['title'][:45].replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
        cc.append(f'<div class="top-item"><img src="{p["img"]}" onerror="this.style.display=\'none\'"><div class="top-item-info"><div class="top-item-brand">{p["brand"]}</div><div class="top-item-title">{t}</div><div class="top-item-sales">&#128715; {p["sales"]}</div></div><div style="font-size:12px;color:var(--shopee);font-weight:700;flex-shrink:0">{p["price"]}</div></div>')
    cc.append('</div>')
    cc.append('<div class="cat-divider"></div>')
    brands_str = ' &middot; '.join(brands) if brands else '多品牌'
    cc.append(f'<div class="cat-footer"><span>月最高销量: <span class="val">{max_sales_str}</span></span><span>主要品牌: <span class="val">{brands_str}</span></span></div>')
    cc.append('</div>')
    ov.append(''.join(cc))

ov.append('</div>')
ov.append('</div>')
lines.append(''.join(ov))

# Category panels
for cat, products in data.items():
    icon_txt = {'唇部':'💄','粉底':'🫙','腮红':'🌸','睫毛膏':'👁️','遮瑕':'✨','定妆喷雾':'💨'}.get(cat,'💄')
    sales_vals = [p['sales_num'] for p in products if p['sales_num'] > 0]
    max_sales = max(sales_vals) if sales_vals else 0
    price_vals = [p['price_num'] for p in products if p['price_num'] > 0]
    avg_price = sum(price_vals) / len(price_vals) if price_vals else 0
    brands_all = list(dict.fromkeys([p['brand'] for p in products]))
    
    pp = [f'<div class="panel" id="panel-{cat}">']
    pp.append(f'<div class="stats-bar">'
              f'<div class="stat-card"><div class="icon">{icon_txt}</div><div class="val">{len(products)}</div><div class="lbl">热销产品数量</div></div>'
              f'<div class="stat-card"><div class="icon">&#127942;</div><div class="val">{max_sales//1000}k+</div><div class="lbl">月最高销量</div></div>'
              f'<div class="stat-card"><div class="icon">&#128176;</div><div class="val">&#3647;{avg_price:.0f}</div><div class="lbl">平均售价（泰铢）</div></div>'
              f'<div class="stat-card"><div class="icon">&#127970;</div><div class="val">{len(brands_all)}</div><div class="lbl">品牌数量</div></div>'
              f'</div>')
    pp.append(f'<div class="view-toggle">'
              f'<button class="view-btn active" onclick="setView(\'{cat}\',\'grid\',this)">&#8862; 卡片</button>'
              f'<button class="view-btn" onclick="setView(\'{cat}\',\'table\',this)">&#9776; 列表</button>'
              f'</div>')
    pp.append(f'<div id="view-title-{cat}" class="section-title"><h2>{icon_txt} {cat} &middot; 热销 Top {len(products)}</h2><div class="line"></div><div class="badge">按月销量排序</div></div>')
    
    # Grid view
    pp.append(f'<div id="grid-{cat}" class="product-grid">')
    for i, p in enumerate(products):
        rank = i + 1
        rank_cls = f'rank-{rank}' if rank <= 3 else 'rank-n'
        promo_html = f'<span class="promo-tag">{p["promo"][:14]}</span>' if p.get('promo') else ''
        disc_html = f'<div class="discount-tag">{p["discount"]}</div>' if p.get('discount') else ''
        title_esc = p['title'][:120].replace('"','&quot;').replace('<','&lt;').replace('>','&gt;')
        card = (f'<div class="product-card">'
                f'<div class="rank-badge {rank_cls}">#{rank}</div>'
                f'<div class="product-img-wrap">'
                f'<img class="product-img" src="{p["img"]}" alt="" onerror="this.parentNode.innerHTML=\'<div class=\\\'img-placeholder\\\'>{icon_txt}</div>\'">'
                f'{disc_html}'
                f'</div>'
                f'<div class="product-body">'
                f'<div class="brand-row"><span class="brand-tag">{p["brand"]}</span>{promo_html}</div>'
                f'<div class="product-title">{title_esc}</div>'
                f'<div class="price">{p["price"]}</div>'
                f'<div class="metrics-row">'
                f'<span class="metric rating">&#11088; {p["rating"]}</span>'
                f'<span class="metric sales">&#128715; {p["sales"]}</span>'
                f'<span class="metric">&#128205; {p["location"][:12]}</span>'
                f'</div>'
                f'</div>'
                f'</div>')
        pp.append(card)
    pp.append('</div>')
    
    # Table view
    pp.append(f'<div id="table-{cat}" style="display:none"><div class="table-wrap">'
              f'<table><thead><tr>'
              f'<th>排名</th><th>图片</th><th>品牌</th><th>产品标题</th>'
              f'<th>售价（泰铢）</th><th>折扣</th><th>评分</th><th>月销量</th><th>发货地</th>'
              f'</tr></thead><tbody>')
    for i, p in enumerate(products):
        rank = i + 1
        t_cls = 'top3' if rank <= 3 else ''
        te = p['title'][:100].replace('<','&lt;').replace('>','&gt;')
        pp.append(f'<tr>'
                  f'<td class="rank-td {t_cls}">#{rank}</td>'
                  f'<td class="thumb"><img src="{p["img"]}" onerror="this.style.display=\'none\'"></td>'
                  f'<td><span class="brand-tag">{p["brand"]}</span></td>'
                  f'<td class="title-td"><div class="tl">{te}</div></td>'
                  f'<td class="price-td">{p["price"]}</td>'
                  f'<td class="disc-td">{p["discount"]}</td>'
                  f'<td class="rating-td">&#11088; {p["rating"]}</td>'
                  f'<td class="sales-td">&#128715; {p["sales"]}</td>'
                  f'<td>{p["location"][:15]}</td>'
                  f'</tr>')
    pp.append('</tbody></table></div></div>')
    pp.append('</div>')
    lines.append(''.join(pp))

lines.append('</div>')  # end content

lines.append('<div class="footer">数据来源：泰国 Shopee 平台 &nbsp;|&nbsp; 共6个美妆品类 &nbsp;|&nbsp; 各品类 Top 20 热销产品 &nbsp;|&nbsp; 按月销量排序</div>')

lines.append("""<script>
function switchTab(id){
  document.querySelectorAll('.tab').forEach(function(t){
    var oc=t.getAttribute('onclick');
    if(oc&&oc.indexOf("'"+id+"'")>-1){t.classList.add('active');}else{t.classList.remove('active');}
  });
  document.querySelectorAll('.panel').forEach(function(p){p.classList.remove('active');});
  var panel=document.getElementById('panel-'+id);
  if(panel){panel.classList.add('active');}
  window.scrollTo({top:0,behavior:'smooth'});
}
function setView(cat,view,btn){
  var grid=document.getElementById('grid-'+cat);
  var table=document.getElementById('table-'+cat);
  var title=document.getElementById('view-title-'+cat);
  btn.closest('.view-toggle').querySelectorAll('.view-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  if(view==='grid'){grid.style.display='grid';table.style.display='none';if(title)title.style.display='flex';}
  else{grid.style.display='none';table.style.display='block';if(title)title.style.display='none';}
}
</script>
</body>
</html>""")

html_content = '\n'.join(lines)
out_path = r'E:\泰国市场重点分析\泰国美妆Shopee热销看板.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f'Done! Size: {len(html_content):,} chars')
print(f'Saved: {out_path}')
