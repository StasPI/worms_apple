from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


class AsymmetricRsa():
    def encrypt_rsa(msg):
        msg = msg.encode()
        # Private key generation
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # Private key serialization
        seri_private_kay = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        print('Private kay: ', seri_private_kay)

        public_key = private_key.public_key()
        seri_public_kay = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print('Public_key: ', seri_public_kay)

        encrypted_data = public_key.encrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None))
        print('Encrypted message: ', encrypted_data)

    def decrypt_rsa(seri_private_kay, ciphertext):
        private_key = serialization.load_pem_private_key(
            seri_private_kay,
            password=None,
            backend=default_backend()
        )

        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        plaintext = plaintext.decode()
        print(plaintext)
