import os
import pytest


def test_health(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_products_books_public(client):
    resp = client.get('/products', query_string={'category': 'books'})
    data = resp.get_json()
    # Should contain only public books
    names = [item['name'] for item in data]
    assert 'Python Basics' in names
    assert 'Flask Cookbook' in names
    assert 'INTERNAL Prototype X' not in names
    assert 'INTERNAL Supplier List' not in names


def test_login_success(client):
    resp = client.post('/login', json={'username': 'demo', 'password': 'demo123'})
    assert resp.status_code == 200
    assert resp.get_json()['ok'] is True


def test_login_failure(client):
    resp = client.post('/login', json={'username': 'demo', 'password': 'wrong'})
    assert resp.status_code == 401
    assert resp.get_json()['ok'] is False
