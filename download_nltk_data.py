import os
import certifi
import nltk

# Ensure SSL uses certifi's certificate bundle
os.environ['SSL_CERT_FILE'] = certifi.where()

# Verify that SSL is using the correct certificates
print(f"SSL certificate file: {os.environ['SSL_CERT_FILE']}")
print(f"Certifi location: {certifi.where()}")

# Download NLTK data
nltk.download('all')