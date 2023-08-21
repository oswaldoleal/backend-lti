from Crypto.PublicKey import RSA


class KeyGenerator:

    @classmethod
    def generate_keys(cls):
        key = RSA.generate(4096)
        private_key = key.exportKey()
        public_key = key.publickey().exportKey()
        return private_key, public_key
