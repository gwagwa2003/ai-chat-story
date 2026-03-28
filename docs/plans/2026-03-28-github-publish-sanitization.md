# GitHub Publish Sanitization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Prepare the project for a safe first push to GitHub by removing secrets from code, excluding local-only assets, and initializing git with a clean tracked file set.

**Architecture:** Add a small configuration module that loads `.env` values without extra dependencies, route existing server scripts through that module, and ignore model weights, training assets, generated audio, and editor noise. Keep runtime behavior close to the current project so local usage remains familiar.

**Tech Stack:** Python, git, unittest

---

### Task 1: Add configuration test coverage

**Files:**
- Create: `tests/test_config.py`
- Create: `server/__init__.py`
- Create: `server/config.py`

**Step 1: Write the failing test**

Add tests for dotenv parsing, required env lookup, and project-relative path resolution.

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_config -v`
Expected: FAIL because `server.config` does not exist yet.

**Step 3: Write minimal implementation**

Create `server/config.py` with dotenv loading and path helpers.

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_config -v`
Expected: PASS

### Task 2: Route runtime scripts through config

**Files:**
- Modify: `server/server.py`
- Modify: `server/stt.py`
- Modify: `server/gs_tts.py`
- Modify: `server/change_gpt.py`
- Modify: `server/change_sovits.py`

**Step 1: Replace hardcoded secrets and absolute paths**

Use config helpers for API keys, model defaults, GPT-SoVITS endpoint, weights, and reference audio paths.

**Step 2: Smoke-check imports**

Run: `python3 -m py_compile server/*.py`
Expected: PASS

### Task 3: Add publish hygiene files

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Modify: `Readme.md`

**Step 1: Ignore local-only and large binary assets**

Exclude training materials, weights, generated audio, `.env`, and editor cache files.

**Step 2: Document setup**

Explain that API keys live in `.env` and local model assets stay untracked.

### Task 4: Initialize git and verify safe scope

**Files:**
- Create: `.git/`

**Step 1: Initialize the repository**

Run: `git init`

**Step 2: Verify tracked set**

Run: `git status --short`
Expected: only source files, docs, and config examples appear as untracked.

**Step 3: Prepare GitHub publish next step**

Confirm local git identity and whether `gh` is installed; if not, provide install/login commands before remote creation and push.

