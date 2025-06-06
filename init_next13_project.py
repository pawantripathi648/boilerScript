# Full script here includes:
# - layout.js
# - Docker setup
# - jest.config.cjs
# - eslint.config.js
# - editorconfig
# - static & dynamic metadata export

import os
import subprocess
import json

PROJECT_NAME = "my-next13-app-dummy"
INCLUDE_TAILWIND = False
BASE_DIR = os.path.join(PROJECT_NAME, "src")
REMOTE_URL = ""

folders = {
    "app": ["home", "user/[id]"],
    "components": ["__tests__"],
    "services": [],
}

files = {
    ".vscode/settings.json": """{
  \"editor.formatOnSave\": true,
  \"editor.codeActionsOnSave\": {
    \"source.fixAll\": true,
    \"source.fixAll.eslint\": true
  },
  \"eslint.validate\": [\"javascript\", \"javascriptreact\", \"typescript\", \"typescriptreact\"],
  \"files.autoSave\": \"afterDelay\",
  \"files.autoSaveDelay\": 1000,
  \"[javascript]\": {
    \"editor.defaultFormatter\": \"esbenp.prettier-vscode\"
  }
}
""",

    "app/layout.js": """export default function RootLayout({ children }) {
  return (
    <html lang=\"en\">
      <body>{children}</body>
    </html>
  );
}
""",

    "app/home/page.js": """export const metadata = {
  title: 'Home Page',
  description: 'Welcome to the static home page',
};

export default function HomePage() {
  return <div>Home Page - Static Route</div>;
}
""",

    "app/user/[id]/page.js": """export async function generateMetadata({ params }) {
  return {
    title: `User Profile - ${params.id}`,
    description: `Dynamic page for user ID ${params.id}`,
  };
}

export default function UserPage({ params }) {
  return <div>User ID: {params.id}</div>;
}
""",

    "app/api/hello/route.js": """export async function GET() {
  return new Response(JSON.stringify({ message: 'Hello from API' }), {
    headers: { 'Content-Type': 'application/json' },
    status: 200,
  });
}
""",

    "services/userService.js": """export async function getUser(id) {
  const res = await fetch(`/api/hello`);
  if (!res.ok) throw new Error('API call failed');
  return res.json();
}
""",

    "middleware.js": """import { NextResponse } from 'next/server';

export function middleware(request) {
  const isAuth = request.cookies.get('auth-token')?.value;
  const protectedPaths = ['/home', '/user'];

  if (protectedPaths.some(path => request.nextUrl.pathname.startsWith(path)) && !isAuth) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/home/:path*', '/user/:path*'],
};
""",

    "components/Header.js": """import React from 'react';

export default function Header() {
  return (
    <header>
      <h1>My App Header</h1>
    </header>
  );
}
""",

    "components/__tests__/Header.test.js": """import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from '../Header.js';

describe('Header component', () => {
  test('renders the header title', () => {
    render(<Header />);
    const title = screen.getByText(/my app header/i);
    expect(title).toBeInTheDocument();
  });

  test('uses correct HTML tag', () => {
    render(<Header />);
    const header = screen.getByRole('banner');
    expect(header.tagName).toBe('HEADER');
  });
});
""",

    "jest.config.cjs": """module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.cjs']
};
""",

    "jest.setup.cjs": """require('@testing-library/jest-dom');
""",

    "check-console.js": """import { execSync } from 'child_process';
const changedFiles = execSync('git diff --cached --name-only').toString().split('');

const offending = [];

for (const file of changedFiles) {
  if (file.endsWith('.js') && !file.includes('check-console.js')) {
    const content = require('fs').readFileSync(file, 'utf8');
    if (content.includes('console.log')) {
      offending.push(file);
    }
  }
}

if (offending.length > 0) {
  console.error('Commit rejected: console.log found in the following files:');
  offending.forEach(f => console.error(' -', f));
  process.exit(1);
}
""",

    "babel.config.cjs": """module.exports = {
  presets: ['@babel/preset-env', '@babel/preset-react'],
};
"""
}
files.update({
    ".env.local": "NEXT_PUBLIC_API_BASE=http://localhost:3000",


    ".gitlab-ci.yml": """stages:
  - install
  - lint
  - test

cache:
  paths:
    - node_modules/

install:
  stage: install
  script:
    - npm install

lint:
  stage: lint
  script:
    - npm run lint

test:
  stage: test
  script:
    - npm run test
""",

    ".prettierrc": """{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100
}
""",

    ".eslintrc.json": """{
  "extends": ["next", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error",
    "no-console": "warn"
  }
}
""",

    "Dockerfile": """FROM node:18-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
""",

    ".dockerignore": """node_modules
.next
.env*
.DS_Store
""",

    "docker-compose.yml": """version: '3.9'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/usr/src/app
      - /usr/src/app/node_modules
    command: npm run dev
""",
".editorconfig": """root = true

[*]
charset = utf-8
indent_style = space
indent_size = 2
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
"""
})
# Update babel.config filename used in jest.config.cjs and file creation to be .cjs for CommonJS compatibility.

files["README.md"] = """# My Next.js 13+ Starter

This is a boilerplate project generated using a Python script. It includes structured folders, linting, testing, Docker, and GitLab CI.

## 🚀 Features

- ✅ App Router (Next.js 13+)
- ✅ Static & dynamic routes
- ✅ API route example
- ✅ Middleware for route protection
- ✅ Reusable components and services
- ✅ ESLint + Prettier on save
- ✅ Jest + Testing Library
- ✅ Husky pre-commit hook (lint + test + console.log block)
- ✅ GitLab CI
- ✅ Docker + Docker Compose
- ✅ .editorconfig

## 📁 Folder Structure

```
my-next13-app/
├── .env.local
├── .gitignore
├── .gitlab-ci.yml
├── .editorconfig
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .husky/
│   └── pre-commit
├── check-console.js
├── jest.config.cjs
├── jest.setup.cjs
├── eslint.config.js
├── .eslintrc.json
├── .prettierrc
├── README.md
├── babel.config.cjs
├── .vscode/settings.json
├── package.json
├── src/
│   ├── app/
│   │   ├── api/hello/route.js
│   │   ├── home/page.js
│   │   ├── user/[id]/page.js
│   │   └── layout.js
│   ├── components/
│   │   ├── Header.js
│   │   └── __tests__/Header.test.js
│   ├── services/userService.js
│   └── middleware.js
```
## Steps to Use
Clone the Boilerplate
Remove the Old Git History
Reinitialize Git

```bash
git init
git remote add origin <your-new-project-git-url>
git add .
git commit -m "Initial commit from Next.js boilerplate"git push -u origin main
bashCopyEditrm -rf .git
bashCopyEditgit clone https://gitlab.com/your-username/next13-boilerplate.git my-new-appcd my-new-app
```
## 🧪 Commands

```bash
npm run dev       # Start dev server
npm run lint      # Run ESLint
npm run test      # Run unit tests
```

## 🐳 Docker

```bash
docker-compose up --build
```
"""
def create_next_app():
    print("📦 Creating Next.js 13+ App Router project...")
    cmd = f"npx create-next-app@latest {PROJECT_NAME} --js --app --eslint --src-dir --import-alias '@/*'"
    if INCLUDE_TAILWIND:
        cmd += " --tailwind"
    subprocess.run(cmd, shell=True, check=True)

def setup_structure():
    print("📁 Setting up folders and boilerplate...")
    os.makedirs(BASE_DIR, exist_ok=True)

    for parent, subs in folders.items():
        base_path = os.path.join(BASE_DIR, parent)
        os.makedirs(base_path, exist_ok=True)
        for sub in subs:
            os.makedirs(os.path.join(base_path, sub), exist_ok=True)

    for path, content in files.items():
        is_root = (
            path.startswith(".")
            or path in [
                "Dockerfile", "docker-compose.yml", "check-console.js",
                "eslint.config.js", "jest.config.cjs", "jest.setup.cjs", "README.md","babel.config.cjs"
            ]
        )
        full_path = os.path.join(PROJECT_NAME, path) if is_root else os.path.join(BASE_DIR, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    print("🔧 Updating package.json scripts...")
    pkg_json_path = os.path.join(PROJECT_NAME, "package.json")

    with open(pkg_json_path, "r", encoding="utf-8") as f:
      data = json.load(f)

      # Add or update script entries
      data["scripts"]["test"] = "jest"
      data["type"] = "module"
      data["scripts"]["lint"] = "next lint"

    with open(pkg_json_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)
    print("📦 Installing dependencies...")
    subprocess.run(
        "npm install --save-dev husky jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom eslint prettier eslint-config-prettier eslint-plugin-prettier eslint-plugin-react @babel/preset-env @babel/preset-react babel-jest",
        cwd=PROJECT_NAME, shell=True, check=True
    )

    subprocess.run("node node_modules/husky/bin.js install", cwd=PROJECT_NAME, shell=True, check=True)

      # Add pre-commit hook manually
    husky_dir = os.path.join(PROJECT_NAME, ".husky")
    os.makedirs(husky_dir, exist_ok=True)

    precommit_path = os.path.join(husky_dir, "pre-commit")
    with open(precommit_path, "w", encoding="utf-8") as f:
      f.write("""

npm run lint
npm run test
node check-console.js
""")
# Make sure it's executable on Unix-like systems



    if REMOTE_URL.strip():  # If REMOTE_URL is not empty
      subprocess.run(["git", "remote", "add", "origin", REMOTE_URL], cwd=PROJECT_NAME)
      subprocess.run("git add .", cwd=PROJECT_NAME, shell=True)
      subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=PROJECT_NAME)
      subprocess.run(["git", "branch", "-M", "main"], cwd=PROJECT_NAME)
      subprocess.run(["git", "push", "-u", "origin", "main"], cwd=PROJECT_NAME)
    else:
      print("REMOTE_URL is empty. Skipping Git setup and push.")


    print("✅ All setup done!")

if __name__ == "__main__":
    create_next_app()
    setup_structure()