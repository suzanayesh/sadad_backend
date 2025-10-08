from apps.root_users.models import RootUser


class _RootUserWrapper:
    """Lightweight wrapper around RootUser to satisfy Django/DRF
    expectations (notably the is_authenticated property).

    We delegate attribute access to the underlying RootUser instance
    so views can use fields like id, username, etc.
    """


    def __init__(self, root_user: RootUser):
        self._root = root_user

    def __getattr__(self, name):
        return getattr(self._root, name)

    @property
    def is_authenticated(self):
        return True


def _get_jwt_auth_base():
    try:
        from rest_framework_simplejwt.authentication import \
            JWTAuthentication as _base
        return _base
    except Exception:
        return None

# fmfkfld
# dml,ld,l
class RootJWTAuthentication:
    """Authenticate JWT tokens and resolve a `root_id` claim to RootUser.

    Returns (root_user, validated_token) tuple on success, or None on failure.
    """

    def __init__(self):
        _base = _get_jwt_auth_base()
        if not _base:
            raise RuntimeError('rest_framework_simplejwt is required for JWT auth')
        self._base = _base()

    def authenticate(self, request):
        # First, try to authenticate as a JWT (simplejwt). If that fails
        # (invalid token or token missing the custom `root_id` claim),
        # fall back to the legacy DB-backed RootUserToken.
        try:
            result = self._base.authenticate(request)
        except Exception:
            result = None

        if result:
            _, validated_token = result
            root_id = validated_token.get('root_id')
            if root_id:
                try:
                    root = RootUser.objects.get(id=root_id)
                except RootUser.DoesNotExist:
                    return None
                # Wrap the model instance so DRF and Django attribute checks
                # such as request.user.is_authenticated work without error.
                return (_RootUserWrapper(root), validated_token)

        # Fallback: try legacy DB token (RootUserToken). Support headers like
        # 'Token <key>' and 'Bearer <key>' where the key is a legacy token.
        auth_header = request.META.get('HTTP_AUTHORIZATION', '') or ''
        token_key = None
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ', 1)[1].strip()
        elif auth_header.startswith('Bearer '):
            token_key = auth_header.split(' ', 1)[1].strip()
        else:
            # allow plain token in header (best-effort)
            token_key = auth_header.strip() or None

        if token_key:
            try:
                # import lazily to avoid circular imports at module load time
                from apps.admin_users.models import RootUserToken

                rt = RootUserToken.objects.select_related('root_user').filter(key=token_key).first()
                if rt:
                    return (_RootUserWrapper(rt.root_user), None)
            except Exception:
                # If anything goes wrong in fallback, return None so DRF continues
                # to treat the request as unauthenticated.
                return None

        return None

    def authenticate_header(self, request):
        """Return the value for the WWW-Authenticate header.

        DRF calls authenticate_header() when constructing error responses
        for authentication failures. Delegate to the underlying simplejwt
        authenticator if available; otherwise return a sensible default.
        """
        if hasattr(self._base, 'authenticate_header'):
            try:
                return self._base.authenticate_header(request)
            except Exception:
                pass
        return 'Bearer'
