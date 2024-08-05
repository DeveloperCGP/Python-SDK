class HexUtils:

    @staticmethod
    def bytes_to_hex(byte_array) -> str:
        return ''.join(f'{byte:02x}' for byte in byte_array)

    @staticmethod
    def hex_to_bytes(hex_string: str) -> bytes:
        return bytes.fromhex(hex_string)
