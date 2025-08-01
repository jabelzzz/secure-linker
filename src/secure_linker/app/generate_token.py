import secrets

def generate_secure_link(request):
    token = str(secrets.token_urlsafe())
    # Construye el enlace usando la información del request
    link = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/secure/{token}"
    return token, link
