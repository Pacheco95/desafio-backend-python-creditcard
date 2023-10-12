#!/usr/bin/env bash

die () {
    echo >&2 "$@"
    exit 1
}

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
MIGRATION_NAME="$1"
MIGRATION_NAME_REGEX='^[a-zA-Z][a-zA-Z0-9_]+$'

[ "$#" -eq 1 ] || die "Expected 1 argument but got $#"

echo "$MIGRATION_NAME" | grep -E -q "$MIGRATION_NAME_REGEX" \
  || die "The migration's name should match this expression '$MIGRATION_NAME_REGEX'"

MIGRATIONS_PATH="$SCRIPT_DIR/../migrations"
DATE_TIME="$( date +"%Y%m%d%H%M" )" # YearMonthDayHour(24h)Minutes
MIGRATION_FILENAME="$DATE_TIME"_"$MIGRATION_NAME"
MIGRATION_TEMPLATE_FILE_DIR="$SCRIPT_DIR/migration_template.hbs"

cat "$MIGRATION_TEMPLATE_FILE_DIR" > "$MIGRATIONS_PATH"/"$MIGRATION_FILENAME".py
