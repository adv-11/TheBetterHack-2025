# Synchronous usage
from gitingest import ingest

# or from URL
def repo_to_text(github_url="https://github.com/neeti-kurulkar/feedback-system"):
    summary, tree, content = ingest(github_url)

    return summary, tree, content

repo_summary, repo_tree, repo_content = repo_to_text()

print(f"Summary: {repo_summary}\n\n")
print(f"Tree: {repo_tree}\n\n")
print(f"Content: {repo_content}\n\n")