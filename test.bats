#!/usr/bin/env bats

JUMEAUX="pipenv run python jumeaux/executor.py"

teardown() {
  rm -rf requests \
         config.yml \
         api \
         responses \
         report.json
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
  [[ ! -a config.yml ]]
  [[ ! -a requests ]]
  [[ ! -a api ]]
}

@test "Init with invalid args" {
  run $JUMEAUX init hogehoge
  [ "$status" -eq 1 ]
  [[ ! -a config.yml ]]
  [[ ! -a requests ]]
  [[ ! -a api ]]
}

@test "Init" {
  $JUMEAUX init simple
  [[ -a config.yml ]]
  [[ -a requests ]]
  [[ -a api ]]
}


#--------------------------
# jumeaux run
#--------------------------

@test "Run simple" {
  $JUMEAUX init simple
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ $(jq '.summary.status.same' report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' report.json) -eq 1 ]]
}


@test "Run xml" {
  $JUMEAUX init xml
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ $(jq '.summary.status.same' report.json) -eq 0 ]]
  [[ $(jq '.summary.status.different' report.json) -eq 1 ]]
}


@test "Run ignore_order" {
  $JUMEAUX init ignore_order
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ $(jq '.summary.status.same' report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' report.json) -eq 2 ]]
}


@test "Run ignore_properties" {
  $JUMEAUX init ignore_properties
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ $(jq '.summary.status.same' report.json) -eq 1 ]]
  [[ $(jq '.summary.status.different' report.json) -eq 1 ]]
}


@test "Run with log level options" {
  $JUMEAUX init simple
  $JUMEAUX run requests -v
  $JUMEAUX run requests -vv
  $JUMEAUX run requests -vvv
  [[ -a responses ]]
}


@test "Run with threads" {
  $JUMEAUX init simple
  $JUMEAUX run requests --threads 2 > report.json
  [[ -a responses ]]
  [[ $(jq '.summary.concurrency.threads' report.json) -eq 2 ]]
  [[ $(jq '.summary.concurrency.processes' report.json) -eq 1 ]]
}


@test "Run with processes" {
  $JUMEAUX init simple
  $JUMEAUX run requests --processes 2 > report.json
  [[ -a responses ]]
  [[ $(jq '.summary.concurrency.threads' report.json) -eq 1 ]]
  [[ $(jq '.summary.concurrency.processes' report.json) -eq 2 ]]
}


#--------------------------
# jumeaux retry
#--------------------------

@test "Retry" {
  $JUMEAUX init simple
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ -a api ]]
  rm -rf requests config.yml responses

  $JUMEAUX retry report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  [[ -a api ]]
}

