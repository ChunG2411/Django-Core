APIKey_preload = {
    'fields' : [
        'order',
        'id',
        'expires',
    ],
    'translations_fields': [
        'name'
    ],
    'search': [
        'name'
    ],
    'filter': [
    ]
}

User_preload = {
    'fields' : [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'avatar',
        'is_active',
        'is_staff',
        'is_superuser'
    ],
    'translations_fields': [
    ],
    'search': [
        'username'
    ],
    'filter': [
    ]
}