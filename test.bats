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
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.same' responses/latest/report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 1 ]]
}


@test "Run all_same" {
  $JUMEAUX init all_same
  $JUMEAUX run requests

  assert_exists responses
  assert_not_exists responses/latest/one/*
  assert_not_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.same' responses/latest/report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 0 ]]
}


@test "Run xml" {
  $JUMEAUX init xml
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 1 ]]
}


@test "Run html" {
  $JUMEAUX init html
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.same' responses/latest/report.json) -eq 0 ]]
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 1 ]]
}


@test "Run ignore_order" {
  $JUMEAUX init ignore_order
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.same' responses/latest/report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 2 ]]
}


@test "Run ignore_properties" {
  $JUMEAUX init ignore_properties
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.summary.status.same' responses/latest/report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' responses/latest/report.json) -eq 1 ]]
}

@test "Run force_json" {
  $JUMEAUX init force_json
  $JUMEAUX run requests

  assert_exists responses
  assert_exists responses/latest/one/*
  assert_exists responses/latest/other/*
  assert_exists responses/latest/report.json
  assert_exists responses/latest/index.html
  [[ $(jq '.trials[0].one.type' responses/latest/report.json) == '"plain"' ]]
  [[ $(jq '.trials[0].other.type' responses/latest/report.json) == '"plain"' ]]
  [[ $(jq '.trials[1].one.type' responses/latest/report.json) == '"json"' ]]
  [[ $(jq '.trials[1].other.type' responses/latest/report.json) == '"json"' ]]
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
  [[ $(jq '.summary.concurrency.threads' responses/latest/report.json) -eq 2 ]]
  [[ $(jq '.summary.concurrency.processes' responses/latest/report.json) -eq 1 ]]
}


@test "Run with processes" {
  $JUMEAUX init simple
  $JUMEAUX run requests --processes 2

  assert_exists responses
  [[ $(jq '.summary.concurrency.threads' responses/latest/report.json) -eq 1 ]]
  [[ $(jq '.summary.concurrency.processes' responses/latest/report.json) -eq 2 ]]
}


#--------------------------
# jumeaux retry
#--------------------------

@test "Retry" {
  $JUMEAUX init simple
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
}

