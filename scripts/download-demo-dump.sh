#!/usr/bin/env bash
# Скачивает демо-БД Postgres Pro (Airlines) для docker-entrypoint-initdb.d
set -euo pipefail

URL="https://edu.postgrespro.ru/demo-20250901-3m.sql.gz"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT_DIR}/init/01-demo-20250901-3m.sql.gz"

echo "→ ${URL}"
echo "→ ${OUT}"

curl -fL --progress-bar -o "${OUT}.part" "${URL}"
mv "${OUT}.part" "${OUT}"

if ! gzip -t "${OUT}"; then
  echo "Ошибка: скачанный файл не похож на валидный gzip" >&2
  exit 1
fi

echo "OK: $(du -h "${OUT}" | cut -f1)"
