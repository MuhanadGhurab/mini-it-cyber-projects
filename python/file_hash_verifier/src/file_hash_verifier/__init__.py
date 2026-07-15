"""File Hash Verifier package."""

from file_hash_verifier.hasher import hash_file, normalize_algo, verify_file

__all__ = ["hash_file", "normalize_algo", "verify_file"]
