import base64
from lxml import etree as ET
from signxml import XMLSigner
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend

try:
    from signxml import SignatureConstructionMethod
except ImportError:
    try:
        from signxml.util import SignatureConstructionMethod
    except ImportError:
        SignatureConstructionMethod = None

# --- CONFIGURACIÓN ---
RUTA_P12 = "certificado.p12"
CONTRASENA_P12 = "clave1234"
ARCHIVO_XML_ENTRADA = '123456789E310000000092.xml'

def cargar_credenciales(ruta, pwd):
    with open(ruta, "rb") as f:
        p12_data = f.read()
    priv_key, cert, _ = pkcs12.load_key_and_certificates(
        p12_data, pwd.encode(), default_backend()
    )
    return priv_key, cert

def firmar_para_dgii():
    priv_key, cert = cargar_credenciales(RUTA_P12, CONTRASENA_P12)
    
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(ARCHIVO_XML_ENTRADA, parser)
    root = tree.getroot()

    metodo = SignatureConstructionMethod.enveloped if SignatureConstructionMethod else "enveloped"
    
    signer = XMLSigner(
        method=metodo, 
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
    )

    signed_root = signer.sign(
        root, 
        key=priv_key, 
        cert=[cert]
    )

    ET.cleanup_namespaces(signed_root)

    output_name = f"firmado_{ARCHIVO_XML_ENTRADA}"
    xml_output = ET.tostring(signed_root, xml_declaration=True, encoding='UTF-8')
    
    with open(output_name, "wb") as f:
        f.write(xml_output)
    
    print(f"✅ Proceso completado. Archivo generado: {output_name}")

if __name__ == "__main__":
    firmar_para_dgii()
