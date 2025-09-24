from fastapi import APIRouter
from databases import Database
from datetime import datetime


router = APIRouter()
db = Database("postgresql://user123:password123@db:5432/db123")


@router.get("/last_messages")
async def last_messages():

    query = """
    select m.user_id, u.username, m.text, m.created_at
    from messages m join users u on u.id = m.user_id
    where (m.created_at, m.id) = (select created_at, id from messages where user_id = m.user_id order by created_at desc, id desc limit 1);
    """

    await db.connect()
    res = await db.fetch_all(query)
    await db.disconnect()

    return res


@router.post("/create_tables_raw")
async def create_tables_raw():

    await db.connect()

    create_users = """
    create table if not exists users (
        id serial primary key, username varchar(255) not null, created_at timestamp default current_timestamp
    );
    """

    create_messages = """
    create table if not exists messages (
        id serial primary key, user_id integer not null references users(id) on delete cascade,
        text text not null, created_at timestamp default current_timestamp
    );
    """

    await db.execute(create_users)
    await db.execute(create_messages)

    await db.disconnect()

    return {"status": "tables created"}


@router.post("/seed_database")
async def seed_database():

    users = [
        {"username": "tim"},
        {"username": "john"},
        {"username": "rose"},
        {"username": "jim"},
        {"username": "tom"},
    ]

    await db.connect()

    for user in users:

        query = "insert into users (username) values (:username) returning id;"
        user_id = await db.execute(query=query, values=user)

        messages = [
            {
                "user_id": user_id,
                "text": f"Hello there!!!",
                "created_at": datetime.now(),
            },
            {
                "user_id": user_id,
                "text": f"Another message of {user['username']}",
                "created_at": datetime.now(),
            },
            {
                "user_id": user_id,
                "text": f"Last message from {user['username']}",
                "created_at": datetime.now(),
            },
        ]

        for msg in messages:

            await db.execute(
                "insert into messages (user_id, text, created_at) values (:user_id, :text, :created_at);",
                values=msg,
            )

    await db.disconnect()

    return {"status": "database seeded"}
