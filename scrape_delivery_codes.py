import requests
from bs4 import BeautifulSoup
import re
import os
import urllib.parse
from jinja2 import Template

def scrape_ubereats_codes():
    url = "https://www.callingtaiwan.com.tw/%e5%a4%96%e9%80%81%e5%84%aa%e6%83%a0%e7%b8%bd%e6%95%b4%e7%90%86-foodpanda-ubereats/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        codes = []
        
        # 找到指定的連結
        link = soup.find('a', string="UberEats 首購優惠碼/折扣碼/信用卡優惠")
        if link:
            # 找到連結後面的第一個表格
            table = link.find_next('table')
            if table:
                rows = table.find_all('tr')[1:]  # 跳過表頭
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        expiry = cols[0].text.strip()
                        content = cols[1].text.strip()
                        code = cols[2].text.strip()
                        
                        code = re.sub(r'\s*\(.*?\)\s*', '', code)
                        
                        deep_link = f"ubereats://promo/apply?client_id=eats&promoCode={urllib.parse.quote(code)}"
                        
                        codes.append({
                            "expiry": expiry,
                            "content": content,
                            "code": code,
                            "deep_link": deep_link
                        })
        
        print(f"找到 {len(codes)} 個 UberEats 優惠碼")
        return codes
    except Exception as e:
        print(f"爬取 UberEats 優惠碼過程中出現錯誤: {e}")
        return []

def scrape_foodpanda_codes():
    url = "https://www.callingtaiwan.com.tw/%e5%a4%96%e9%80%81%e5%84%aa%e6%83%a0%e7%b8%bd%e6%95%b4%e7%90%86-foodpanda-ubereats/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        codes = []
        
        # 找到指定的連結
        link = soup.find('a', string="foodpanda 首購優惠碼/折扣碼/信用卡優惠")
        if link:
            # 找到連結後面的第一個表格
            table = link.find_next('table')
            if table:
                rows = table.find_all('tr')[1:]  # 跳過表頭
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        expiry_date = cols[0].text.strip()
                        content = cols[1].text.strip()
                        code = cols[2].text.strip()
                        code = re.sub(r'\s*\(.*?\)\s*', '', code)
                        deep_link = f"foodpanda://coupon?code={urllib.parse.quote(code)}"
                        
                        codes.append({
                            "expiry_date": expiry_date,
                            "content": content,
                            "code": code,
                            "deep_link": deep_link
                        })
        
        print(f"找到 {len(codes)} 個 Foodpanda 優惠碼")
        return codes
    except Exception as e:
        print(f"爬取 Foodpanda 優惠碼過程中出現錯誤: {e}")
        return []

def scrape_uber_codes():
    url = "https://www.callingtaiwan.com.tw/uber-promo-code/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        codes = []
        
        # 找到指定的連結
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # 跳過表頭
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    expiry = cols[0].text.strip()
                    country = cols[1].text.strip()
                    content = cols[2].text.strip()
                    code_cell = cols[3]
                    
                    # 找到所有的優惠碼連結
                    code_links = code_cell.find_all('a', class_='rdc_box_button')
                    
                    for code_link in code_links:
                        code = code_link.text.strip()
                        code = re.sub(r'\s*\(.*?\)\s*', '', code)
                        
                        deep_link = f"uber://?action=applyPromo&client_id=&code={urllib.parse.quote(code)}"
                        
                        codes.append({
                            "expiry": expiry,
                            "country": country,
                            "content": content,
                            "code": code,
                            "deep_link": deep_link
                        })
        
        print(f"找到 {len(codes)} 個 Uber 優惠碼")
        return codes
    except Exception as e:
        print(f"爬取 Uber 優惠碼過程中出現錯誤: {e}")
        return []

def generate_html(ubereats_codes, foodpanda_codes, uber_codes):
    categories = {"Uber": {}, "UberEats": {}, "Foodpanda": {}}
    
    # 處理 Uber 代碼
    for code in uber_codes:
        category = re.search(r'【(.*?)】', code['content'])
        if category:
            category = category.group(1)
        else:
            category = '其他'
        
        if category not in categories["Uber"]:
            categories["Uber"][category] = []
        categories["Uber"][category].append(code)
    
    # 處理 UberEats 代碼
    for code in ubereats_codes:
        category = re.search(r'【(.*?)】', code['content'])
        if category:
            category = category.group(1)
        else:
            category = '其他'
        
        if category not in categories["UberEats"]:
            categories["UberEats"][category] = []
        categories["UberEats"][category].append(code)
    
    # 處理 Foodpanda 代碼
    for code in foodpanda_codes:
        category = re.search(r'【(.*?)】', code['content'])
        if category:
            category = category.group(1)
        else:
            category = '其他'
        
        if category not in categories["Foodpanda"]:
            categories["Foodpanda"][category] = []
        categories["Foodpanda"][category].append(code)
    
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Uber、UberEats、Foodpanda 優惠碼</title>
        <link rel="icon" type="image/png" href="coupon.PNG">
        <!-- ADSENSE_SCRIPT_PLACEHOLDER -->
        <style>
            body { 
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                padding: 10px; 
                margin: 0;
                background-color: #f0f0f0;
                color: #333;
                transition: background-color 0.3s, color 0.3s;
            }
            h1 { 
                text-align: center; 
                color: inherit;
            }
            .sidebar {
                width: 250px;
                background-color: #333;
                padding: 15px;
                color: white;
                height: 100vh;
                position: fixed;
                top: 0;
                left: 0;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                overflow-y: auto;
                z-index: 1000;
            }
            .sidebar a {
                color: white;
                text-decoration: none;
                display: block;
                padding: 10px 0;
            }
            .sidebar a:hover {
                background-color: #575757;
            }
            .content {
                margin-left: 0;
                padding: 20px;
                transition: margin-left 0.3s ease;
            }
            .content.shifted {
                margin-left: 250px;
            }
            .code-card {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 15px;
                padding: 15px;
            }
            .code-card h2 {
                margin-top: 0;
                font-size: 1.2em;
                color: #444;
            }
            .code-card p {
                margin: 5px 0;
                font-size: 0.9em;
                color: #666;
            }
            .code {
                font-weight: bold;
                color: #e44d26;
            }
            .button {
                display: block;
                width: calc(100% - 30px); 
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 1em;
                cursor: pointer;
                text-align: center;
                text-decoration: none;
                background-color: #4CAF50;
                color: white;
                margin-top: 10px;
                margin: 0 auto;
            }
            .copied {
                background-color: #45a049;
            }
            .toggle-button {
                display: block;
                background-color: #333;
                color: white;
                padding: 10px;
                text-align: center;
                cursor: pointer;
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 1001;
                border-radius: 5px;
            }
            .divider {
                height: 1px;
                background-color: #575757;
                margin: 15px 0;
            }

            @media (max-width: 768px) {
                .content.shifted {
                    margin-left: 0;
                }
            }

            /* 深色模式 */
            @media (prefers-color-scheme: dark) {
                body {
                    background-color: #121212;
                    color: #ffffff;
                }
                h1, h2, h3, p {
                    color: #ffffff;
                }
                .code-card {
                    background-color: #1e1e1e;
                }
                .code-card h2 {
                    color: #ffffff;
                }
                .code-card p {
                    color: #dddddd;
                }
                .code {
                    color: #ff7b7b;
                }
                .button {
                    color: #ffffff;
                    background-color: #4CAF50;
                }
                .sidebar {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                .sidebar a {
                    color: #ffffff;
                }
            }
        </style>
        <script>
        // 添加新的 JavaScript 函數
        function saveScrollPosition() {
            sessionStorage.setItem('scrollPosition', window.pageYOffset);
        }

        function restoreScrollPosition() {
            var scrollPosition = sessionStorage.getItem('scrollPosition');
            if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                sessionStorage.removeItem('scrollPosition');
            }
        }

        // 頁面加載時恢復滾動位置
        window.addEventListener('load', restoreScrollPosition);
        </script>
    </head>
    <body>
        <div class="toggle-button" onclick="toggleSidebar()">
            ☰ 菜單
        </div>
        <div class="sidebar" id="sidebar">
            <h2>優惠碼</h2>
            <div class="divider"></div>
            <h3>Uber</h3>
            {% for category in categories["Uber"] %}
                <a href="#Uber-{{ category|replace(' ', '_') }}" onclick="scrollToSection('Uber-{{ category|replace(' ', '_') }}')">{{ category }}</a>
            {% endfor %}
            <div class="divider"></div>
            <h3>UberEats</h3>
            {% for category in categories["UberEats"] %}
                <a href="#UberEats-{{ category|replace(' ', '_') }}" onclick="scrollToSection('UberEats-{{ category|replace(' ', '_') }}')">{{ category }}</a>
            {% endfor %}
            <div class="divider"></div>
            <h3>Foodpanda</h3>
            {% for category in categories["Foodpanda"] %}
                <a href="#Foodpanda-{{ category|replace(' ', '_') }}" onclick="scrollToSection('Foodpanda-{{ category|replace(' ', '_') }}')">{{ category }}</a>
            {% endfor %}
        </div>
        <div class="content" id="content">
            <h1>優惠碼</h1>
            <h2 id="Uber">Uber</h2>
            {% for category, codes in categories["Uber"].items() %}
                <h3 id="Uber-{{ category }}">{{ category }}</h3>
                {% for code in codes %}
                    <div class="code-card">
                        <h2>{{ code.content }}</h2>
                        <p class="country">{{ code.country }}</p>
                        <p>優惠碼: <span class="code">{{ code.code }}</span></p>
                        <p>有效期限: {{ code.expiry }}</p>
                        <a href="{{ code.deep_link }}" class="button" onclick="copyCode('{{ code.code }}', this); return false;">複製優惠碼並開啟APP</a>
                    </div>
                {% endfor %}
            {% endfor %}
            <h2 id="UberEats">UberEats</h2>
            {% for category, codes in categories["UberEats"].items() %}
                <h3 id="UberEats-{{ category }}">{{ category }}</h3>
                {% for code in codes %}
                    <div class="code-card">
                        <h2>{{ code.content }}</h2>
                        <p>優惠碼: <span class="code">{{ code.code }}</span></p>
                        <p>有效期限: {{ code.expiry }}</p>
                        <a href="{{ code.deep_link }}" class="button" onclick="copyCode('{{ code.code }}', this); return false;">複製優惠碼並開啟APP</a>
                    </div>
                {% endfor %}
            {% endfor %}
            <h2 id="Foodpanda">Foodpanda</h2>
            {% for category, codes in categories["Foodpanda"].items() %}
                <h3 id="Foodpanda-{{ category }}">{{ category }}</h3>
                {% for code in codes %}
                    <div class="code-card">
                        <h2>{{ code.content }}</h2>
                        <p>優惠碼: <span class="code">{{ code.code }}</span></p>
                        <p>有效期限: {{ code.expiry_date }}</p>
                        <a href="{{ code.deep_link }}" class="button" onclick="copyCode('{{ code.code }}', this); return false;">複製優惠碼並開啟APP</a>
                    </div>
                {% endfor %}
            {% endfor %}
        </div>
        <script>
            function toggleSidebar() {
                var sidebar = document.getElementById('sidebar');
                var content = document.getElementById('content');
                if (sidebar.style.transform === 'translateX(0%)') {
                    sidebar.style.transform = 'translateX(-100%)';
                    content.classList.remove('shifted');
                } else {
                    sidebar.style.transform = 'translateX(0%)';
                    if (window.innerWidth > 768) {
                        content.classList.add('shifted');
                    }
                }
            }

            function scrollToSection(sectionId) {
                var section = document.getElementById(sectionId);
                if (section) {
                    section.scrollIntoView({behavior: "smooth"});
                }
                if (window.innerWidth <= 768) {
                    toggleSidebar();
                }
            }

            window.addEventListener('resize', function() {
                var sidebar = document.getElementById('sidebar');
                var content = document.getElementById('content');
                if (window.innerWidth <= 768) {
                    content.classList.remove('shifted');
                } else if (sidebar.style.transform === 'translateX(0%)') {
                    content.classList.add('shifted');
                }
            });

            function copyCode(code, button) {
                navigator.clipboard.writeText(code).then(function() {
                    button.textContent = '已複製';
                    button.classList.add('copied');
                    setTimeout(function() {
                        button.textContent = '複製優惠碼並開啟APP';
                        button.classList.remove('copied');
                        
                        // 記錄當前滾動位置
                        var scrollPosition = window.pageYOffset;
                        
                        // 更新網址
                        var newUrl = window.location.href.split('#')[0] + '#' + scrollPosition;
                        history.replaceState(null, '', newUrl);
                        
                        // 保存滾動位置到 sessionStorage
                        sessionStorage.setItem('scrollPosition', scrollPosition);
                        
                        // 跳轉到 APP
                        window.location.href = button.href;
                    }, 500);
                }, function(err) {
                    console.error('無法複製文字: ', err);
                    
                    // 記錄當前滾動位置
                    var scrollPosition = window.pageYOffset;
                    
                    // 更新網址
                    var newUrl = window.location.href.split('#')[0] + '#' + scrollPosition;
                    history.replaceState(null, '', newUrl);
                    
                    // 保存滾動位置到 sessionStorage
                    sessionStorage.setItem('scrollPosition', scrollPosition);
                    
                    // 跳轉到 APP
                    window.location.href = button.href;
                });
                return false;
            }
        </script>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(categories=categories)
    
    # 為 DeliveryCodes.html 寫入原始內容
    filename = 'DeliveryCodes.html'
    content_without_adsense = html_content.replace('<!-- ADSENSE_SCRIPT_PLACEHOLDER -->', '')
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content_without_adsense)
        print(f"HTML 檔案已保存至: {os.path.join(os.getcwd(), filename)}")
    except Exception as e:
        print(f"寫入檔案時發生錯誤: {e}")

    # 為 deliverycoupon.html 添加 Google AdSense 腳本
    adsense_script = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9625730094952985" crossorigin="anonymous"></script>'
    content_with_adsense = html_content.replace('<!-- ADSENSE_SCRIPT_PLACEHOLDER -->', adsense_script)

    filename = 'index.html'
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content_with_adsense)
        print(f"HTML 檔案（含 AdSense）已保存至: {os.path.join(os.getcwd(), filename)}")
    except Exception as e:
        print(f"寫入檔案時發生錯誤: {e}")

if __name__ == "__main__":
    ubereats_codes = scrape_ubereats_codes()
    foodpanda_codes = scrape_foodpanda_codes()
    uber_codes = scrape_uber_codes()
    if ubereats_codes or foodpanda_codes or uber_codes:
        generate_html(ubereats_codes, foodpanda_codes, uber_codes)
    else:
        print("沒有找到優惠碼，不創建 HTML 檔案")

