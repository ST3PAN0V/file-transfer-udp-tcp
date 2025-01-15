#!/bin/bash

PY_SERVER_PATH="./../src/server.py"
PY_CLIENT_PATH="./../src/client.py"
ORIGINAL_TEST_FILE_PATH="./../test/original_test_file.txt"
RECEIVED_TEST_FILE_PATH="./../test/received_test_file.txt"
LOG_DIR="./logs"
SERVER_LOG_FILE="${LOG_DIR}/server.log"
CLIENT_LOG_FILE="${LOG_DIR}/client.log"

# Чистка файлов и каталогов
clean_up() {
  if [[ -d "${LOG_DIR}" ]]; then
      rm -rf "${LOG_DIR}"
  fi
  rm -f "${ORIGINAL_TEST_FILE_PATH}" "${RECEIVED_TEST_FILE_PATH}"
}

# убить сервер, чтобы освободить порт(на всякий пожарный)
kill_server() {
   if [ -n "$SERVER_PID" ]; then
     kill -9 "$SERVER_PID"
   fi
}

# Подготовка к тесту
prepare_to_testing() {
  # Чистка лога
  clean_up
  mkdir -p "${LOG_DIR}"
  touch "${SERVER_LOG_FILE}"
  touch "${CLIENT_LOG_FILE}"

  kill_server
}


# Создание тестового файла
create_test_file() {
  local test_size=$(( (RANDOM % 10) + 1 )) # рандом от 1МБ до 10МБ
  echo "Создание тестового файла (Размер: ${test_size} Мб)..."
  local random_data=$(tr -dc A-Za-z0-9 </dev/urandom | head -c $((test_size * 1024 * 1024)))
  echo "$random_data" > "${ORIGINAL_TEST_FILE_PATH}"
}


# Запуск сервера
start_server() {
  echo "Запуск сервера..."
  python "${PY_SERVER_PATH}" "${ORIGINAL_TEST_FILE_PATH}" &> "${SERVER_LOG_FILE}" &
  local server_pid=$!
  wait_for_server_ready "$server_pid" || exit 1
  echo "Сервер готов..."
  return $?
}


# Ожидание готовности сервера
wait_for_server_ready() {
  local pid="$1"
  until grep -q "serving" "${SERVER_LOG_FILE}"; do
    if ! kill -0 "$pid"; then
      echo "Сервер завершился с ошибкой!"
      exit 1
    fi
  done
}


# Запуск клиента
start_client() {
  echo "Запуск клиента..."
  python "${PY_CLIENT_PATH}" "${RECEIVED_TEST_FILE_PATH}" &> "${CLIENT_LOG_FILE}" &
  local client_pid=$!
  wait_for_client_finished "$client_pid" || exit 1
  echo "Клиент завершил работу..."
  return $?
}

# Ожидания полного получения файла клиентом
wait_for_client_finished() {
  local pid="$1"
  until grep -q "downloaded as" "${CLIENT_LOG_FILE}"; do
      if ! kill -0 "$pid"; then
        echo "Клиент завершился с ошибкой!"
        exit 1
      fi
  done
}


# Сравнение файлов
compare_files() {
  echo "Сравнение файлов..."
  if cmp -s "${RECEIVED_TEST_FILE_PATH}" "${ORIGINAL_TEST_FILE_PATH}"; then
    echo "Файлы одинаковые!"
  else
    echo "Файлы не одинаковые. Что-то пошло не так!"
    diff "${RECEIVED_TEST_FILE_PATH}" "${ORIGINAL_TEST_FILE_PATH}"
  fi
}

# Основная функция
main() {
  prepare_to_testing
  create_test_file
  start_server
  start_client
  compare_files
  echo "Тестирование завершено успешно!"
}

# чистка артефактов. Запускает только отчистку, без теста. Usage: path/to/test_script.sh --clean
if [[ "$1" == "--clean" ]]; then
  clean_up
  echo -e "Артефакты были отчищены.\nДля запуска тестирования запустите скрипт без аргументов."
  exit 0
fi

main