vimdiff \
  <(ansible-vault view --vault-password-file=.vault_password \
    <(git show HEAD:secrets/app-env.yml)) \
  <(ansible-vault view --vault-password-file=.vault_password \
    <(git show HEAD~2:secrets/app-env.yml))
