import os
import datetime
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID

# Function to generate RSA key pair
def generate_rsa_key_pair():
    # Generate a private key with public exponent 65537 and key size 2048 bits
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key

# Function to save the private key to a text file
def save_private_key_to_text_file(private_key, filename):
    # Open the file in binary write mode
    with open(filename, "wb") as f:
        # Write the private key in PEM format to the file
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

# Function to save RSA public key to a .crt file
def save_public_key_to_crt_file(public_key, filename):
    # Create a certificate builder
    cert_builder = x509.CertificateBuilder()

    # Define subject and issuer information for the certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "FRANCE"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Colombes"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ESIEA"),
        x509.NameAttribute(NameOID.COMMON_NAME, f"KeyPair_{filename}")
    ])
    
    # Set various attributes for the certificate builder
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
    cert_builder = cert_builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    cert_builder = cert_builder.serial_number(x509.random_serial_number())
    cert_builder = cert_builder.public_key(public_key)

    # Sign the certificate with the private key
    cert = cert_builder.sign(
        private_key,
        hashes.SHA256(),
    )

    # Write the certificate to the specified file in PEM format
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(encoding=serialization.Encoding.PEM))

# Create folders to store keys and certificates
private_key_folder = "Generated_private_keys_8000"
public_key_folder = "Generated_public_keys8000"
nm_cert = 1000
os.makedirs(private_key_folder, exist_ok=True)
os.makedirs(public_key_folder, exist_ok=True)

# Record start time
start_time = time.time()

# Generate and save 400 RSA key pairs with private keys in one folder and public keys in another folder
for i in range(1, nm_cert+1):
    private_key = generate_rsa_key_pair()
    public_key = private_key.public_key()

    # Save private key to a text file in the private_keys folder
    private_key_filename = f"{private_key_folder}/private_key_{i}.txt"
    save_private_key_to_text_file(private_key, private_key_filename)

    # Save public key to a .crt file in the public_keys folder
    public_key_filename = f"{public_key_folder}/public_key_{i}.crt"
    save_public_key_to_crt_file(public_key, public_key_filename)
    
# Record end time
end_time = time.time()

# Calculate and print the total execution time
execution_time = end_time - start_time
print(f"RSA private keys and public keys with {nm_cert} certificates generated and saved in {private_key_folder} and {public_key_folder} in {execution_time:.2f} seconds.")