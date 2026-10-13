# Release Checklist

Before publishing a GitHub update or deploying a Hugging Face Space:

- [ ] Confirm the README and links reflect the current implementation.
- [ ] Check `git status` and review the staged file list for tokens, private
  data, model weights, local files, and planning notes.
- [ ] Confirm that no day-plan files are included in the public commit.
- [ ] Review data, model, and audio provenance and applicable use terms.
- [ ] Check Hugging Face model access and Space secrets without exposing token
  values in source or logs.
- [ ] For a Space deployment, verify the selected GPU can load all models in the
  Model Arena.
- [ ] Review the Space build/runtime logs and test both app tabs.
- [ ] Describe evaluation metrics and diagnostic limitations accurately.
- [ ] Preserve important evaluation output before rerunning scripts that
  overwrite result files.
