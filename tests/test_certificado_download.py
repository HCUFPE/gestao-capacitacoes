"""Tests for the certificate download endpoint in main.py.

Validates correct Content-Type and Content-Disposition: inline for different file types.
"""
import pytest
import os


@pytest.mark.asyncio
async def test_download_certificado_nao_encontrado(async_client):
    """Requesting a non-existent certificate should return 404."""
    response = await async_client.get("/api/certificados/download/inexistente.pdf")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_download_certificado_pdf(async_client):
    """PDF certificate should return Content-Type application/pdf and Content-Disposition inline."""
    uploads_dir = os.getenv("UPLOADS_DIR", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    test_file = os.path.join(uploads_dir, "test_cert.pdf")
    with open(test_file, "wb") as f:
        f.write(b"%PDF-fake")

    try:
        response = await async_client.get("/api/certificados/download/test_cert.pdf")
        assert response.status_code == 200
        assert b"%PDF-fake" in response.content
        assert response.headers["content-type"] == "application/pdf"
        assert "inline" in response.headers["content-disposition"]
        assert "attachment" not in response.headers["content-disposition"]
    finally:
        os.remove(test_file)


@pytest.mark.asyncio
async def test_download_certificado_png(async_client):
    """PNG image certificate should return Content-Type image/png and Content-Disposition inline."""
    uploads_dir = os.getenv("UPLOADS_DIR", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Minimal PNG header (8 bytes)
    png_header = b"\x89PNG\r\n\x1a\n"
    test_file = os.path.join(uploads_dir, "test_cert.png")
    with open(test_file, "wb") as f:
        f.write(png_header)

    try:
        response = await async_client.get("/api/certificados/download/test_cert.png")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert "inline" in response.headers["content-disposition"]
        assert "attachment" not in response.headers["content-disposition"]
    finally:
        os.remove(test_file)


@pytest.mark.asyncio
async def test_download_certificado_jpg(async_client):
    """JPEG image certificate should return Content-Type image/jpeg and Content-Disposition inline."""
    uploads_dir = os.getenv("UPLOADS_DIR", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)

    # Minimal JPEG header
    jpg_header = b"\xff\xd8\xff\xe0"
    test_file = os.path.join(uploads_dir, "test_cert.jpg")
    with open(test_file, "wb") as f:
        f.write(jpg_header)

    try:
        response = await async_client.get("/api/certificados/download/test_cert.jpg")
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"
        assert "inline" in response.headers["content-disposition"]
        assert "attachment" not in response.headers["content-disposition"]
    finally:
        os.remove(test_file)
