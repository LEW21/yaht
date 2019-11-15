import yaht

Message = yaht.schema_to_type(...)

s = yaht.Session()

try:
    resp = await s.get('https://example.com/')
except yaht.HTTP404_NotFound as e:
    print("Oh no")

post = (await resp.body) | Message.parse

post = (await resp.body) | yaht.auto

await s.post('https://example.com', Message(xyz = 5))







def test_post():
    session_a = Session()
    session_b = Session()

    topic = await session_a['/topics/'].post(Topic(
        title = 'Hello World!',
        text = 'World is cool!',
    )).body | Topic

    post = await session_b[topic.messages_url].post(Message(
        text = 'Nope.',
    )).body | Message

    await session_b[post.url].patch(Message.Patch(
        text = 'Yup.',
    )).body | Message

    post_res = friend_session[post.url]
    await post_res.get()
    await post_res.patch(Message.Patch())
    await post_res.delete()


def test_post():
    session_a = Session()
    session_b = Session()

    topic = await session_a['/topics/'].post(Auto(
        title = 'Hello World!',
        text = 'World is cool!',
    )).body | Auto

    post = await session_b[topic.messages_url].post(Auto(
        text = 'Nope.',
    )).body | Auto

    await session_b[post.url].patch(Auto(
        text = 'Yup.',
    )).body | Auto

    post_res = friend_session[post.url]
    await post_res.get()
    await post_res.patch(Auto())
    await post_res.delete()


def test_post():
    session_a = Session()
    session_b = Session()

    topic = await session_a.post('/topics/', Auto(
        title = 'Hello World!',
        text = 'World is cool!',
    )).body | Auto

    post = await session_b.post(topic.messages_url, Auto(
        text = 'Nope.',
    )).body | Auto

    await session_b.patch(post.url, Auto(
        text = 'Yup.',
    )).body | Auto

    post_res = friend_session[post.url]
    await post_res.get()
    await post_res.patch(Auto())
    await post_res.delete()


def test_post():
    session = Session()

    topic = await session['/topics/'].post(Auto(
        title = 'Hello World!',
        text = 'World is cool!',
    )).body | Auto

    post = await topic.messages_url.post(Auto(
        text = 'Nope.',
    )).body | Auto

    await post.url.patch(Auto(
        text = 'Yup.',
    ))

    await topic.url.delete()


def test_post():
    session = Session()

    topic = await session['/topics/'].post(Topic(
        title = 'Hello World!',
        text = 'World is cool!',
    )).body | Topic

    message = await topic.messages_url.post(Message(
        text = 'Nope.',
    )).body | Message

    await message.url.patch(Message.Patch(
        text = 'Yup.',
    ))

    await topic.url.delete()
