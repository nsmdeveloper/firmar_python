# Firmador de Comprobantes Fiscales Electrónicos (e-CF) - DGII RD 🇩🇴

Este repositorio proporciona una solución robusta en Python para la **firma digital de Comprobantes Fiscales Electrónicos (e-CF)**, cumpliendo con los estándares técnicos y de seguridad exigidos por la **Dirección General de Impuestos Internos (DGII)** de la República Dominicana.

El script implementa la firma de tipo **Enveloped Signature** (XML-DSig) utilizando criptografía RSA y hashing SHA-256, asegurando que el XML generado sea válido para los servicios web de recepción de la DGII.

---

## 🚀 Características

*   **Firma Enveloped:** Inserta el nodo `<Signature>` dentro del documento XML original.
*   **Compatibilidad Criptográfica:** Soporte completo para certificados digitales en formato `.p12` (PKCS#12).
*   **Estándar DGII:** Configurado con los algoritmos específicos requeridos (`rsa-sha256`, `sha256` y `xml-exc-c14n#`).
*   **Limpieza Automática:** Elimina espacios en blanco y gestiona namespaces para evitar errores de validación del Digest.

---

## 🛠️ Requisitos del Sistema

Para procesar XML y criptografía en Python, se requieren algunas librerías de sistema. 

### En Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y libxml2-dev libxslt-dev python3-dev
