#!/usr/bin/env python3
"""
Push a file to a GitHub repository via the Contents API.

Usage:
    python3 push_to_github.py <filepath> <repo> <repo_path> <token> [commit_message]

Arguments:
    filepath        Local file path to push
    repo            GitHub repo in "owner/repo" format
    repo_path       Destination path in the repo (e.g. "chapters/ch3-notes.html")
    token           GitHub personal access token
    commit_message  Optional commit message (default: "Update {repo_path}")

The script automatically handles:
- Base64 encoding the file content
- Fetching the current file SHA (required for updates, skipped for new files)
- Creating or updating the file via PUT request

Examples:
    python3 push_to_github.py ch3-notes.html user/repo chapters/ch3-notes.html ghp_xxxxx
    python3 push_to_github.py progress.md user/repo progress.md ghp_xxxxx "Add Ch3 to concepts index"
"""

import sys
import json
import base64
import urllib.request
import urllib.error


def get_file_sha(repo, repo_path, token):
    """Fetch the SHA of an existing file (needed for updates). Returns None for new files."""
    url = f"https://api.github.com/repos/{repo}/contents/{repo_path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data.get("sha")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # New file
        raise


def push_file(filepath, repo, repo_path, token, commit_message=None):
    """Push a local file to GitHub via the Contents API."""
    if not commit_message:
        commit_message = f"Update {repo_path}"

    # Read and encode
    with open(filepath, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    # Get SHA if file exists (required for updates)
    sha = get_file_sha(repo, repo_path, token)

    # Build payload
    payload = {
        "message": commit_message,
        "content": content_b64,
    }
    if sha:
        payload["sha"] = sha

    # Push
    url = f"https://api.github.com/repos/{repo}/contents/{repo_path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json",
    })

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            action = "Updated" if sha else "Created"
            print(f"{action}: {result['content']['html_url']}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Error {e.code}: {error_body}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    repo = sys.argv[2]
    repo_path = sys.argv[3]
    token = sys.argv[4]
    message = sys.argv[5] if len(sys.argv) > 5 else None

    success = push_file(filepath, repo, repo_path, token, message)
    sys.exit(0 if success else 1)
