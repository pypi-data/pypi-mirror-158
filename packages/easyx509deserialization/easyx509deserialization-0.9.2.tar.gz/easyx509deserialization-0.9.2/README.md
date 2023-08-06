This is a front end to the cryptography module x509 read functions.  It will allow you to quickly pull most information from an x509 certificate.  All of the read functions will take one parameter that can be either a base 64 string, (a .cer file) a binary object (a .der file) or a cryptography x509 certificate.

Usage:
from easyx509deserialization import read_certificate\
certificate_file = "duckduckgo-com.pem"\
f = open(certificate_file, "r")\
certificate_text = f.read()\
f.close()\
subject_name = read_certificate.get_subject_name(certificate_text)

Additionally, a p7b/p7c file can be passed in, and return a list of cryptography certificate objects.\
certificate_list = read_certificate.get_certs_from_pkcs7(pkcs7_file.p7b)