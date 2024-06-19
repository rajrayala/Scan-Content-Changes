import os
from github import Github, InputGitAuthor, InputGitTreeElement

def update_repo(files, commit_message):
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    workspace = os.getenv('GITHUB_WORKSPACE')

    g = Github(token)
    repo = g.get_repo(repo_name)

    ref = repo.get_git_ref("heads/main")
    main_sha = ref.object.sha
    commit = repo.get_commit(main_sha)

    base_tree = repo.get_git_tree(commit.commit.tree.sha)

    elements = []
    for file_path in files:
        with open(file_path, 'r') as file:
            content = file.read()
        element = repo.create_git_blob(content, 'utf-8')
        tree_element = InputGitTreeElement(
            path=os.path.relpath(file_path, workspace),
            mode='100644',
            type='blob',
            sha=element.sha
        )
        elements.append(tree_element)

    tree = repo.create_git_tree(elements, base_tree=base_tree)

    author = InputGitAuthor(
        name=os.getenv('GITHUB_ACTOR'),
        email=f"{os.getenv('GITHUB_ACTOR')}@users.noreply.github.com"
    )
    new_commit = repo.create_git_commit(commit_message, tree, [commit.commit], author=author)

    ref.edit(new_commit.sha)
