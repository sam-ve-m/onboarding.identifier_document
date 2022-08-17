#!/bin/bash
fission spec init
fission env create --spec --name identifier-document-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name identifier-document-fn --env identifier-document-env --src "./func/*" --entrypoint main.save_document --executortype newdeploy --maxscale 1
fission route create --spec --name identifier-document-rt --method POST --url /onboarding/post_identifier_document --function identifier-document-fn
