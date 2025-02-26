# block-escape-solver

## UI

https://block-escape-solver-ui.vercel.app

Run locally:

```shell
cd block-escape-solver-ui
npm run dev
```

Deploy to vercel

```shell
cd block-escape-solver-ui
vercel --prod
```

## API

api (local)

```shell
rye run uvicorn api.main:app --reload
```

check api in local

```shell
$ curl -X POST "http://127.0.0.1:8000/solve" \
     -H "Content-Type: application/json" \
     -d @dev/aaaa.json
```

deploy api

```shell
vercel --prod
```

check api in prod

```shell
$ curl -X POST "https://block-escape-solver.vercel.app/solve" \
     -H "Content-Type: application/json" \
     -d @dev/aaaa.json
```
