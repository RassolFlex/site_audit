// Экспресс-аудит сайта

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('auditForm');
    const loading = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const urlInput = document.getElementById('url').value;
        
        if (!urlInput.startsWith('http')) {
            alert('Пожалуйста, введите полный URL с протоколом (https:// или http://)');
            return;
        }
        
        resultsDiv.style.display = 'none';
        loading.style.display = 'block';
        
        const url = urlInput;
        
        try {
            await runAudit(url);
            
        } catch (err) {
            resultsDiv.style.display = 'block';
            resultsDiv.className = 'error';
            resultsDiv.innerHTML = `<strong>Ошибка:</strong> ${err.message}`;
        } finally {
            loading.style.display = 'none';
        }
    });
});

async function runAudit(url) {
    const formData = new FormData();
    formData.append('url', url);
    
    try {
        // AJAX POST запрос без CSRF (отключено в middleware для локального тестирования)
        const response = await fetch('/audit/', {
            method: 'POST',
            body: formData,
            headers: {}
        });
        
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        // Отображаем реальные результаты из API
        displayResults(url, data.checks);
        
    } catch (err) { 
        console.error(err);
        alert('Ошибка аудита: ' + err.message);
    }
}

function displayResults(url, results) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    resultsDiv.className = 'info';
    
    // Правильный парсинг массива объектов [{domain_info: "..."}, {cms: "..."}]
    let html = `<h2 style="margin-bottom:15px;">📋 Результаты аудита сайта: <a href="${url}" target="_blank">${url}</a></h2>`;
    
    // Преобразуем массив объектов в читаемый формат
    const checksMap = {};
    if (Array.isArray(results)) {
        results.forEach(item => {
            for (const key in item) {
                if (item.hasOwnProperty(key)) {
                    checksMap[key] = item[key];
                }
            }
        });
    }
    
    html += '<div class="checklist">';
    
    // 0. Домен
    html += createCheckItem('📌 Домен', checksMap.domain_info || 'Недоступно');
    
    // 1. CMS
    html += createCheckItem('🖥️ CMS / Система управления', checksMap.cms || 'Не определена');
    
    // 2. Индексация
    html += createCheckItem('🔍 Индексация в поисковых системах', checksMap.indexing || 'Не проверено');
    
    // 3. Редирект WWW/non-WWW
    html += createCheckItem('🔀 Редирект (WWW/не WWW)', checksMap.redirect || 'Не проверено');
    
    // 4. SSL
    html += createCheckItem('🔒 SSL-сертификат (HTTPS)', checksMap.ssl || 'Критично важно для SEO');
    
    // 5. Скорость загрузки
    html += createCheckItem('⚡ Скорость загрузки', checksMap.speed || 'Не проверено');
    
    // 6. Кодировка/структура
    html += createCheckItem('📄 Кодировка / Микроразметка', checksMap.structure || 'Не проверено');
    
    // 7. Метатеги
    html += createCheckItem('📝 Метатеги (title/description)', checksMap.metatags || 'Не проверены');
    
    // 8. Изображения
    html += createCheckItem('🖼️ Графический контент', checksMap.images || 'Не проверено');
    
    // 9. robots.txt
    html += createCheckItem('🤖 robots.txt', checksMap.robots || 'Не найдено');
    
    // 10+. Дополнительные проверки
    html += createCheckItem('📦 Дубли страниц', checksMap.duplicates || 'Требуется дополнительная проверка (sitemap + crawl)');
    html += createCheckItem('📱 Социальные сигналы', checksMap.social_signals || '⚠️ Возможны социальные сигналы');
    html += createCheckItem('🏆 Конкуренты в ТОП', checksMap.competitors || 'Требуется расширенный анализ SERP');
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}

function createCheckItem(title, text) {
    return `<div class="check-item">${title}: ${text}</div>`;
}