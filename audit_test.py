"""Тестирование audit/main.py (УЛУЧШЕННАЯ ВЕРСИЯ с AGE - Года/Месяцы/Дни)"""
import sys
import os

# Правильный путь к проекту (из root)
ROOT = r'D:\Python\site_audit'
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from audit.main import check_domain_info, check_ssl, check_cms

print('=' * 60)
print('📌 TEST: AUDIT MODULE (Возраст домена в годах/месяцах/днях!)')
print('=' * 60)

# Тест 1: Проверка SSL
print('\n[Test 1] ✓ SSL:')
result = check_ssl('https://example.com')
print(result)

# Тест 2: Определение CMS
print('\n[Test 2] ✓ CMS:')
result = check_cms('https://wordpress.org')
print(result)

# Тест 3: Информация о домене (AGE - возраст в годах/месяцах/днях!)
print('\n[Test 3] 📌 DOMAIN AGE (Года/Месяцы/Дни):')
try:
    result = check_domain_info('https://example.com')
    print(result)
except Exception as e:
    print(f'❌ Error: {e}')

# Тест 4: Пример с тестовым доменом (google.com - ~30 лет!)
print('\n[Test 4] 📌 Domain Age Test:')
result = check_domain_info('https://google.com')
print(result)

print('\n✅ Все тесты завершены!')