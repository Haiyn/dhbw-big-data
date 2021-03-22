db.createUser({
    user: 'dev',
    pwd: 'dev',
    roles: [
        {
            role: 'readWrite',
            db: 'dhbw-big-data-mongodb'
        }
    ]
});