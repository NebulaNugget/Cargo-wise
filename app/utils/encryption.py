import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional, Union, Dict, Any

logger = logging.getLogger(__name__)

class EncryptionService:
    """Service for encrypting and decrypting sensitive data"""
    
    def __init__(self, key: Optional[str] = None):
        """Initialize with optional key or generate from environment"""
        if key:
            self.key = key
        else:
            # Get key from environment or generate a new one
            self.key = os.environ.get("ENCRYPTION_KEY")
            if not self.key:
                self.key = self._generate_key()
                logger.warning("Generated new encryption key. This should be stored securely.")
        
        # Convert key to bytes if it's a string
        if isinstance(self.key, str):
            self.key = self.key.encode()
            
        # Initialize Fernet cipher
        self.cipher = Fernet(self.key)
    
    def _generate_key(self) -> bytes:
        """Generate a new Fernet key"""
        key = Fernet.generate_key()
        return base64.urlsafe_b64encode(key).decode()
    
    def encrypt(self, data: Union[str, bytes, Dict[str, Any]]) -> str:
        """Encrypt data and return as base64 string"""
        try:
            # Convert data to bytes if it's not already
            if isinstance(data, dict):
                import json
                data = json.dumps(data).encode()
            elif isinstance(data, str):
                data = data.encode()
                
            # Encrypt the data
            encrypted = self.cipher.encrypt(data)
            
            # Return as base64 string
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            raise
    
    def decrypt(self, encrypted_data: Union[str, bytes]) -> bytes:
        """Decrypt data from base64 string or bytes"""
        try:
            # Convert to bytes if it's a string
            if isinstance(encrypted_data, str):
                encrypted_data = base64.urlsafe_b64decode(encrypted_data)
                
            # Decrypt the data
            return self.cipher.decrypt(encrypted_data)
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            raise
    
    def decrypt_to_string(self, encrypted_data: Union[str, bytes]) -> str:
        """Decrypt data and return as string"""
        return self.decrypt(encrypted_data).decode()
    
    def decrypt_to_dict(self, encrypted_data: Union[str, bytes]) -> Dict[str, Any]:
        """Decrypt data and parse as JSON dictionary"""
        import json
        return json.loads(self.decrypt(encrypted_data))
    
    def derive_key_from_password(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """Derive a key from a password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

# Singleton instance
_encryption_service = None

def get_encryption_service() -> EncryptionService:
    """Get the encryption service singleton"""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service