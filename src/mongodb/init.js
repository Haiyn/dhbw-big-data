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

db = new Mongo().getDB("dhbw-big-data-mongodb");

db.createCollection('Cards', { capped: false });