response_headers = {
    "X-XSS-Protection"          : "1; mode=block",
    "X-Content-Type-Options"    : "nosniff",
    "Content-Security-Policy"   : "script-src 'self'",
    "Strict-Transport-Security" : "max-age=31536000; includeSubDomains"
}