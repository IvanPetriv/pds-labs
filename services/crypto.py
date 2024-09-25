import ctypes
from ctypes import wintypes

# Load the Windows CryptoAPI DLL
advapi32 = ctypes.WinDLL('advapi32')

# Constants used in CryptoAPI
PROV_RSA_FULL = 1
CRYPT_NEWKEYSET = 0x00000008
AT_KEYEXCHANGE = 1
CRYPT_EXPORTABLE = 0x00000001
CALG_RSA_KEYX = 0x0000a400

# Define some required types
HCRYPTPROV = wintypes.HANDLE
HCRYPTKEY = wintypes.HANDLE
LPBYTE = ctypes.POINTER(ctypes.c_ubyte)

# Define the necessary function prototypes
advapi32.CryptAcquireContextW.argtypes = [
    ctypes.POINTER(HCRYPTPROV),  # phProv
    wintypes.LPCWSTR,            # pszContainer
    wintypes.LPCWSTR,            # pszProvider
    wintypes.DWORD,              # dwProvType
    wintypes.DWORD               # dwFlags
]

advapi32.CryptGenKey.argtypes = [
    HCRYPTPROV,                  # hProv
    wintypes.DWORD,              # Algid
    wintypes.DWORD,              # dwFlags
    ctypes.POINTER(HCRYPTKEY)    # phKey
]

advapi32.CryptExportKey.argtypes = [
    HCRYPTKEY,                   # hKey
    HCRYPTKEY,                   # hExpKey
    wintypes.DWORD,              # dwBlobType
    wintypes.DWORD,              # dwFlags
    LPBYTE,                      # pbData
    ctypes.POINTER(wintypes.DWORD)  # pdwDataLen
]

advapi32.CryptReleaseContext.argtypes = [
    HCRYPTPROV,                  # hProv
    wintypes.DWORD               # dwFlags
]

# 1. Acquire a cryptographic context
hProv = HCRYPTPROV()
if not advapi32.CryptAcquireContextW(ctypes.byref(hProv), None, None, PROV_RSA_FULL, CRYPT_NEWKEYSET):
    raise ctypes.WinError()

# 2. Generate an RSA key pair
hKey = HCRYPTKEY()
if not advapi32.CryptGenKey(hProv, CALG_RSA_KEYX, 0x08000000 | CRYPT_EXPORTABLE, ctypes.byref(hKey)):
    raise ctypes.WinError()

# 3. Export the public key
public_key_size = wintypes.DWORD(0)
advapi32.CryptExportKey(hKey, 0, 0x06, 0, None, ctypes.byref(public_key_size))  # 0x06 stands for PUBLICKEYBLOB
public_key_blob = (ctypes.c_ubyte * public_key_size.value)()
if not advapi32.CryptExportKey(hKey, 0, 0x06, 0, public_key_blob, ctypes.byref(public_key_size)):
    raise ctypes.WinError()

print("Public Key Blob:", bytes(public_key_blob))

# 4. Release the cryptographic context and key
advapi32.CryptReleaseContext(hProv, 0)
