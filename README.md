# Testing UI - ParaBank con Selenium

Este proyecto contiene tests automatizados UI para ParaBank usando Selenium WebDriver.

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar los tests

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con reporte HTML
pytest tests/ --html=report.html --self-contained-html

# Ejecutar un test específico
pytest tests/test_parabank.py::TestParaBank::test_login
```

## Estructura del proyecto

- `pages/` - Page Objects (patrón de diseño)
- `tests/` - Tests automatizados
- `utils/` - Utilidades y helpers
- `requirements.txt` - Dependencias del proyecto
