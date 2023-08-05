import os
import pickle
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

FILENAME = 'db_path.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


def load() -> str:
    default_addr = f"mongodb://localhost:27017"
    try:
        with open(FULL_PATH, "rb") as fr:
            s = pickle.load(fr)
            logger.debug(s)
            return s
    except (EOFError, FileNotFoundError) as e:
        print(f"File not found: {FILENAME} => Create file with default path: {default_addr}")
        with open(FULL_PATH, "wb") as fw:
            pickle.dump(default_addr, fw)
            return default_addr


def save(new_addr: str, port="27017"):
    """

    Args:
        new_addr: 몽고 db 서버주소 mongodb://를 붙여도 되고 않붙여도 됨
        port: 기본 포트 번호 27017

    Returns:
        None
    """
    before = load()
    if not new_addr.startswith("mongodb://"):
        new_addr = "".join(["mongodb://", new_addr])
    new_addr = "".join([new_addr, f":{port}"])
    print(f'Change mongo setting : {before} -> {new_addr}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(new_addr, fw)

