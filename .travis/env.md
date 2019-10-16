## Environment Variables for Travis Job

```bash
API_NODE        # the Steem API Node URL, e.g. https://api.steemit.com
BLOG_REPO       # the repository path for storing the generated htmls, e.g. steemblog/steemblog.github.io
DEBUG           # set to TRUE for printing debug info in log
DURATION        # how many days of post to query in incremental build, e.g. 7 (days)
GIT_EMAIL       # the Git account's email for pushing the generated htmls to GitHub
GIT_USERNAME    # the Git account's username for pushing the generated htmls to GitHub
GITHUB_PAT      # the GitHub token that you generated from https://github.com/settings/tokens
STEEM_ACCOUNTS  # the Steem accounts you'd like to sync the blogs, separate by comma, e.g. ned,dan
```
