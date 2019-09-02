#!/usr/bin/env bats

JUMEAUX="pipenv run python jumeaux/executor.py"

teardown() {
  rm -rf requests \
         config.yml \
         api \
         responses
}

assert_exists() {
  [[ $(ls "$1") ]]
}

assert_not_exists() {
  [[ ! $(ls "$1") ]]
}

assert_number_property() {
  local path=$1
  local expected=$2
  [[ $(jq $path responses/latest/report.json) -eq $expected ]]
}

assert_not_number_property() {
  local path=$1
  local expected=$2
  # Distinguish between numbers and character strings
  [[ $(jq -r $path responses/latest/report.json) == "$expected" ]]
}

assert_null_property() {
  local path=$1
  [[ $(jq $path responses/latest/report.json) == null ]]
}

#--------------------------
# jumeaux usage
#--------------------------

@test "Usage" {
  $JUMEAUX -h
}


#--------------------------
# jumeaux init
#--------------------------

@test "Init with no args" {
  run $JUMEAUX init
  [ "$status" -eq 1 ]

  assert_not_exists config.yml
  assert_not_exists requests
  assert_not_exists api
}

@test "Init with invalid args" {
  run $JUMEAUX init hogehoge
  [ "$status" -eq 1 ]

  assert_not_exists config.yml
  assert_not_exists requests
  assert_not_exists api
}

@test "Init" {
  $JUMEAUX init simple

  assert_exists config.yml
  assert_exists requests
  assert_exists api
}


#--------------------------
# jumeaux run
#--------------------------

@test "Run simple" {
  $JUMEAUX init simple
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 1
  assert_number_property '.summary.status.different' 1

  assert_not_number_property '.trials[0].method' 'GET'
}

@test "Run path_custom" {
  $JUMEAUX init path_custom
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 0
  assert_number_property '.summary.status.different' 2
  assert_not_number_property '.summary.one.path.before' 'json'
  assert_not_number_property '.summary.one.path.after' 'xml'
  assert_not_number_property '.summary.other.path.before' '([^-]+)-(\d).json'
  assert_not_number_property '.summary.other.path.after' '\1/case-\2.json'

  assert_not_number_property '.trials[0].one.url' 'http://localhost:8000/api/one/same-1.xml'
  assert_not_number_property '.trials[0].other.url' 'http://localhost:8000/api/other/same/case-1.json'
  assert_not_number_property '.trials[1].one.url' 'http://localhost:8000/api/one/diff-1.xml?param=123'
  assert_not_number_property '.trials[1].other.url' 'http://localhost:8000/api/other/diff/case-1.json?param=123'
}

@test "Run query_custom" {
  $JUMEAUX init query_custom
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 1
  assert_number_property '.summary.status.different' 1
  assert_null_property '.summary.one.query'
  assert_not_number_property '.summary.other.query.overwrite.additional[0]' hoge
  assert_not_number_property '.summary.other.query.remove[0]' param

  assert_not_number_property '.trials[0].one.url' 'http://localhost:8000/api/one/same-1.json'
  assert_not_number_property '.trials[0].other.url' 'http://localhost:8000/api/other/same-1.json?additional=hoge'
  assert_not_number_property '.trials[1].one.url' 'http://localhost:8000/api/one/diff-1.json?param=123'
  assert_not_number_property '.trials[1].other.url' 'http://localhost:8000/api/other/diff-1.json?additional=hoge'
}

@test "Run all_same" {
  $JUMEAUX init all_same
  $JUMEAUX run requests

  assert_exists responses
  assert_not_exists responses/latest/one/*
  assert_not_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 1
  assert_number_property '.summary.status.different' 0
}


@test "Run xml" {
  $JUMEAUX init xml
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.different' 1
  assert_not_number_property '.trials[0].tags[0]' 'over $10 (id=bk101)'
  assert_number_property '.trials[0].tags[1]'
}


@test "Run html" {
  $JUMEAUX init html
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 0
  assert_number_property '.summary.status.different' 1
}


@test "Run ignore_order" {
  $JUMEAUX init ignore_order
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 1
  assert_number_property '.summary.status.different' 2
}

@test "Run ignore" {
  $JUMEAUX init ignore
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 2
  assert_number_property '.summary.status.different' 1
}

@test "Run force_json" {
  $JUMEAUX init force_json
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_not_number_property '.trials[0].one.type' plain
  assert_not_number_property '.trials[0].other.type' plain
  assert_not_number_property '.trials[1].one.type' json
  assert_not_number_property '.trials[1].other.type' json
}

@test "Run request_headers" {
  $JUMEAUX init request_headers
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_not_number_property '.summary.one.headers["XXX-Header-Key"]' xxx-header-key-one
  assert_not_number_property '.summary.one.headers["User-Agent"]' jumeaux-test
  assert_not_number_property '.summary.other.headers["XXX-Header-Key"]' xxx-header-key-other
  assert_not_number_property '.trials[0].headers' "{}"
  assert_not_number_property '.trials[1].headers["User-Agent"]' "Hack by requests!"
  assert_not_number_property '.trials[2].headers' "{}"
  assert_not_number_property '.trials[3].headers["User-Agent"]' "Hack by requests!"
}

@test "Run with log level options" {
  $JUMEAUX init simple
  $JUMEAUX run requests -v
  $JUMEAUX run requests -vv
  $JUMEAUX run requests -vvv

  assert_exists responses
}


@test "Run with threads" {
  $JUMEAUX init simple
  $JUMEAUX run requests --threads 2

  assert_exists responses

  assert_number_property '.summary.concurrency.threads' 2
  assert_number_property '.summary.concurrency.processes' 1
}


@test "Run with processes" {
  $JUMEAUX init simple
  $JUMEAUX run requests --processes 2

  assert_exists responses

  assert_number_property '.summary.concurrency.threads' 1
  assert_number_property '.summary.concurrency.processes' 2
}

@test "Run root_array" {
  $JUMEAUX init root_array
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/one-props/*
  assert_exists responses/latest/other-props/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html

  assert_number_property '.summary.status.same' 1
  assert_number_property '.summary.status.different' 1
}


#--------------------------
# jumeaux retry
#--------------------------

@test "Retry with empty path" {
  $JUMEAUX init path_empty
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/report.json
  assert_exists api

  cp responses/latest/report.json .
  rm -rf requests responses

  $JUMEAUX retry report.json
  rm report.json

  assert_exists responses
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  assert_exists api

  assert_number_property '.summary.status.same' 0
  assert_number_property '.summary.status.different' 1
}

