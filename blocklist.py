"""
blocklist.py

This file contains a list of blocked JWT tokens. It willbe importyed by 
the app and the logout resource so the token can be added to the blocklist when the user logs out.

Author: Tim Neale
Date: 2020 07 17
"""

BLOCKLIST = set()