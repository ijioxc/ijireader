#!/bin/bash
cd "$(dirname "$0")"
uvicorn tts_server:app --reload --port 8000
