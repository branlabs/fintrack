# Contributing to FinTrack

Thanks for your interest in improving FinTrack! This guide explains how to propose changes, how we name branches and commits, what we expect in pull requests, how to run tests locally, and how to report bugs or request features.

> Tip: GitHub will automatically suggest this document when you open an Issue or Pull Request.

---

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Project Setup](#project-setup)
- [Branch Strategy](#branch-strategy)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Running Tests](#running-tests)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)
- [Documentation](#documentation)
- [Release Process](#release-process)
- [Contact](#contact)

---

## Code of Conduct
By participating, you agree to abide by our Code of Conduct (`CODE_OF_CONDUCT.md`). Be respectful and constructive.

---

## Project Setup
1. **Fork** the repo and **clone** your fork.
2. Create a working branch (see [Branch Strategy](#branch-strategy)).
3. Install dependencies and set up environment:

   ```bash
   # Node tooling example; adjust to your stack
   pnpm install
   cp .env.example .env
