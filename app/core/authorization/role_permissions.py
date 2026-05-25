ROLE_PERMISSIONS = {
    "admin": [
        "users:create",
        "users:read",
        "users:update",
        "users:delete",
        "roles:assigndashboard:view",
    ],
    "profesor": ["students:read", "students:updatedashboard:view"],
    "estudiante": ["profile:view"],
}
