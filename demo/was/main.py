from http import HTTPStatus

from kubernetes.config import load_incluster_config

from kubernetes import client, config
from fastapi import FastAPI
from sqlalchemy import select, desc, asc, func

from db.session import engineconn
from models.user import User

app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

namespace = 'default'
group = 'hanyang.ac.kr'
plural = 'kiadaservicecounts'
resource_name = 'hanyang-kiada-autoscalar'

MIN_REPLICAS = 2


@app.get("/")
async def health_check():
    return {"message": "health_check"}


# 회원 추가
@app.post("/sign-up", status_code=HTTPStatus.OK)
async def sign_up():
    query = select(User.id).order_by(desc(User.id)).limit(1)
    last_id: int = session.execute(query).scalar()
    if last_id:
        user = User(name=f"user_{last_id + 1}")
    else:
        user = User(name=f"user_1")
    session.add(user)
    session.commit()


# id값이 가장 작으면서 로그아웃 된 사용자의 상태를 로그인으로 변경
@app.post("/login", status_code=HTTPStatus.OK)
async def login():
    query = select(User).where(User.enabled == False).order_by(asc(User.id)).limit(1)
    user = session.execute(query).scalar()
    if user:
        user.enabled = True
    session.commit()

    await __try_change_kiada_autoscalar_spec()


# id값이 가장 크면서 로그인 된 사용자의 상태를 로그아웃으로 변경
@app.post("/logout", status_code=HTTPStatus.OK)
async def logout():
    query = select(User).where(User.enabled == True).order_by(desc(User.id)).limit(1)
    user = session.execute(query).scalar()
    if user:
        user.enabled = False
    session.commit()

    await __try_change_kiada_autoscalar_spec()


async def __try_change_kiada_autoscalar_spec():
    enabled_user_count = await __aggregate_enabled_user_count()
    if enabled_user_count < 1000:
        target_replicas = MIN_REPLICAS
    elif enabled_user_count < 10000:
        target_replicas = 3
    else:
        additional_users = (enabled_user_count - 10000) // 20000
        target_replicas = 3 + additional_users

    # config.load_kube_config()
    load_incluster_config()
    custom_api = client.CustomObjectsApi()
    kiada_service_count_crd = custom_api.get_namespaced_custom_object(group=group, version='v1', namespace=namespace,
                                                                      plural=plural, name=resource_name)

    kiada_service_count_crd['spec']["kiadaServiceCount"] = target_replicas

    custom_api.replace_namespaced_custom_object(group, version='v1', namespace=namespace, plural=plural,
                                                name=resource_name, body=kiada_service_count_crd)


async def __aggregate_enabled_user_count():
    query = select(func.count(User.id)).where(User.enabled == True)
    enabled_user_count = session.execute(query).scalar()
    return enabled_user_count
