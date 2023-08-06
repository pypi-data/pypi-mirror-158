# Kaldi-Liāu

[![PyPI version](https://badge.fury.io/py/kaldiliau.svg)](https://badge.fury.io/py/kaldiliau)

Kaldi siong-kuan bôo-tsoo, lōo-iōng ū
- Īng Hàn-jī kiám-tsa Lô-má-jī tui-tsê im-tóng.

## Pau
```
KUI=ithuan/boohing:hokbu
KALDISU=ithuan/kaldi-hanlo-tsuliau:hokbu
docker pull ${KUI}
docker pull ${KALDISU}
docker-compose build --build-arg KUI=${KUI} --build-arg KALDISU=${KALDISU}
```

## Ka-tī tiān-náu tsíng-ha̍p tshì-giām
```
tox -e test
```

## Pau pip package
```
rm dist/ -rf
python setup.py sdist
python -m twine upload dist/*
```

### SIL/SPN
因為model無訓練`SPN`，暫時用`SIL`來食掉


