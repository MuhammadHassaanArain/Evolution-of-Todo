# from fastapi import FastAPI
# from starlette.middleware.security import SecurityMiddleware

# def add_security_headers(app: FastAPI):
#     """
#     Add security headers to the application
#     """
#     # Add security middleware
#     app.add_middleware(
#         SecurityMiddleware,
#         # Add security headers
#         content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;",
#         strict_transport_security="max-age=31536000; includeSubDomains",
#         referrer_policy="no-referrer-when-downgrade",
#         x_content_type_options="nosniff",
#         x_frame_options="DENY",
#         x_xss_protection="1; mode=block",
#     )

#     return app

from fastapi import FastAPI

def add_security_headers(app: FastAPI):
    """
    Security headers are intentionally disabled for Phase II.
    Will be added in Phase III (production hardening).
    """
    return app
