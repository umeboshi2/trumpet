
def get_regular_users(request):
    users = request.db.query(User).all()
    skey = 'trumpet.admin.admin_username'
    admin_username = request.registry.settings.get(skey, 'admin')
    return [u for u in users if u.username != admin_username]

