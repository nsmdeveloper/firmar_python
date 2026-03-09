import os
from lxml import etree as ET
from signxml import XMLSigner, SignatureConstructionMethod
from cryptography.hazmat.primitives.serialization import pkcs12

# --- CONFIGURACIÓN ---
RUTA_P12 = "certificado.p12"
CONTRASENA_P12 = "c"
ARCHIVO_XML_ENTRADA = '123456789E310000000001.xml'

def firmar_xml_dgii(ruta_p12, password, xml_entrada):
    try:
        # 1. Cargar Credenciales
        with open(ruta_p12, "rb") as f:
            p12_data = f.read()
        
        priv_key, cert, additional_certs = pkcs12.load_key_and_certificates(
            p12_data, password.encode()
        )
        cert_chain = [cert] + (additional_certs if additional_certs else [])

        # 2. Cargar XML Limpio
        parser = ET.XMLParser(remove_blank_text=True, recover=True)
        tree = ET.parse(xml_entrada, parser)
        root = tree.getroot()

        # 3. Configurar el Firmador
        signer = XMLSigner(
            method=SignatureConstructionMethod.enveloped,
            signature_algorithm="rsa-sha256",
            digest_algorithm="sha256",
            c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"
        )

        # 4. Firmar (Solución al error de Reference URI)
        # Usamos None en reference_uri para que firme el nodo raíz actual
        # y definimos explícitamente las transformaciones
        signed_root = signer.sign(
            root, 
            key=priv_key, 
            cert=cert_chain,
            reference_uri=None, # Cambiado de "" a None para evitar el error de resolución
            always_add_key_value=True # Recomendado para compatibilidad DGII
        )

        # 5. Limpieza y Guardado
        ET.cleanup_namespaces(signed_root)
        
        nombre_salida = f"firmado_{xml_entrada}"
        xml_final = ET.tostring(
            signed_root, 
            xml_declaration=True, 
            encoding='UTF-8', 
            pretty_print=False
        )

        with open(nombre_salida, "wb") as f:
            f.write(xml_final)

        print(f"✅ ¡Firmado con éxito! Archivo: {nombre_salida}")
        return nombre_salida

    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        return None

if __name__ == "__main__":
    firmar_xml_dgii(RUTA_P12, CONTRASENA_P12, ARCHIVO_XML_ENTRADA)
