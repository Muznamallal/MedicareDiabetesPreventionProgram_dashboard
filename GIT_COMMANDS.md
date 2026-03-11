# Git Commands to Update Your Repository

## Step 1: Organize Your Files

Make sure your project directory has this structure:

```
MedicareDiabetesPreventionProgram_dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── MDPP_Supplier_Mapping_02_01_26.csv
├── CPS_MDCR_PHYSSUPP_MA_2016_FINAL.xlsx (optional)
└── screenshots/ (create this folder and add your screenshots)
    ├── overview.png
    ├── map.png
    └── data-table.png
```

## Step 2: Navigate to Your Local Repo

```bash
cd /path/to/your/MedicareDiabetesPreventionProgram_dashboard
```

## Step 3: Check Current Status

```bash
git status
```

This shows which files are new, modified, or untracked.

## Step 4: Add Your Files

### Option A: Add specific files
```bash
git add app.py
git add requirements.txt
git add README.md
git add .gitignore
git add MDPP_Supplier_Mapping_02_01_26.csv
git add CPS_MDCR_PHYSSUPP_MA_2016_FINAL.xlsx
```

### Option B: Add all files at once
```bash
git add .
```

## Step 5: Commit Your Changes

```bash
git commit -m "Update dashboard with Q1 2026 data and improved documentation

- Added Streamlit dashboard (app.py) with interactive features
- Updated README with comprehensive documentation
- Added MDPP supplier mapping data (Q1 2026)
- Added CMS Program Statistics Medicare Advantage data
- Included .gitignore for Python projects
- Enhanced with map visualization and filtering capabilities"
```

## Step 6: Push to GitHub

```bash
git push origin main
```

If your default branch is `master` instead of `main`, use:
```bash
git push origin master
```

## Alternative: If You Haven't Set Up Git Yet

If this is your first time pushing to the repo:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: MDPP Streamlit dashboard with Q1 2026 data"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/Muznamallal/MedicareDiabetesPreventionProgram_dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 7: Verify on GitHub

1. Go to https://github.com/Muznamallal/MedicareDiabetesPreventionProgram_dashboard
2. Refresh the page
3. Verify all your files are there

## Creating Screenshots Directory

Before pushing, create a screenshots folder and add your screenshots:

```bash
mkdir screenshots
# Then add your screenshot images to this folder
# For example: screenshots/overview.png, screenshots/map.png, etc.
```

After adding screenshots:
```bash
git add screenshots/
git commit -m "Add dashboard screenshots"
git push origin main
```

## Troubleshooting

### If you get authentication errors:

You may need to use a Personal Access Token (PAT) instead of your password:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` permissions
3. Use the token as your password when pushing

### If you have merge conflicts:

```bash
git pull origin main
# Resolve any conflicts in your text editor
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### To see commit history:

```bash
git log --oneline
```

## Quick Reference

```bash
# Check status
git status

# Add files
git add filename.ext

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest changes
git pull origin main

# View remote URL
git remote -v
```
