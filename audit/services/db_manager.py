"""Управление базой данных для ручного ввода данных."""
import sqlite3
from datetime import datetime, timezone


def init_db(db_path='audit_data.db'):
    """Инициализация SQLite базы данных."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Таблица для ручного ввода данных о сайтах
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS manual_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT UNIQUE,
        created_at DATETIME,
        updated_at DATETIME,
        registration_date TEXT,
        expires_date TEXT,
        http_to_https_redirect TEXT,
        certificate_valid_until TEXT,
        server_location TEXT,
        custom_notes TEXT
    )
    ''')
    
    conn.commit()
    conn.close()


def add_manual_data(domain, data_dict):
    """Добавить/обновить ручной ввод данных для домена.

    Args:
        domain: Домен сайта
        data_dict: dict с данными (registration_date, expires_date, etc.)
    
    Returns:
        int - количество затронутых записей
    """
    conn = sqlite3.connect('audit_data.db')
    cursor = conn.cursor()
    
    # Подготовка SQL для INSERT/UPDATE
    cursor.execute('''
    INSERT OR REPLACE INTO manual_data 
    (domain, created_at, updated_at, registration_date, expires_date, 
     http_to_https_redirect, certificate_valid_until, server_location, custom_notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        domain,
        datetime.now(timezone.utc).isoformat(),
        datetime.now(timezone.utc).isoformat(),
        data_dict.get('registration_date'),
        data_dict.get('expires_date'),
        str(data_dict.get('http_to_https_redirect')),
        data_dict.get('certificate_valid_until'),
        data_dict.get('server_location'),
        data_dict.get('custom_notes') or None
    ))
    
    conn.commit()
    conn.close()
    return 1


def get_manual_data(domain):
    """Получить ручной ввод данных для домена.

    Args:
        domain: Домен сайта
    
    Returns:
        dict с данными или None если нет
    """
    conn = sqlite3.connect('audit_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM manual_data WHERE domain = ?', (domain,))
    row = cursor.fetchone()
    
    if row:
        # Возвращаем dict без id и timestamps если нужно
        data = {
            'domain': row[1],
            'registration_date': row[4],
            'expires_date': row[5],
            'http_to_https_redirect': row[6],
            'certificate_valid_until': row[7],
            'server_location': row[8],
            'custom_notes': row[9]
        }
    else:
        data = None
    
    conn.close()
    return data


def clear_manual_data(domain):
    """Очистить ручные данные для домена."""
    conn = sqlite3.connect('audit_data.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM manual_data WHERE domain = ?', (domain,))
    conn.commit()
    conn.close()
    return cursor.rowcount


def get_all_domains():
    """Получить список всех доменов с ручными данными."""
    conn = sqlite3.connect('audit_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT domain FROM manual_data')
    domains = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return domains


__all__ = ["init_db", "add_manual_data", "get_manual_data", "clear_manual_data", "get_all_domains"]
