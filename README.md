# 🚀 My Next.js 13+ Boilerplate

This is a high-quality, opinionated starter kit for building robust **Next.js 13+** applications. It is designed for scalability, maintainability, and efficient team collaboration.

---

## 🎯 Key Features

✅ Next.js 13+ with App Router (including static & dynamic routes)  
✅ API routes and Middleware for route protection  
✅ Reusable components and services  
✅ ESLint + Prettier for consistent code style  
✅ Unit testing with Jest & React Testing Library  
✅ Husky pre-commit hook (enforcing lint, tests, and no `console.log`)  
✅ GitLab CI for seamless CI/CD integration  
✅ Docker & Docker Compose support  
✅ EditorConfig for consistent editor behavior  
✅ Clean and modular structure for rapid development  

---

## 📁 Project Structure

my-next13-app/
├── .env.local
├── .gitlab-ci.yml
├── .editorconfig
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .husky/
│ └── pre-commit
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
│ ├── app/
│ │ ├── api/hello/route.js
│ │ ├── home/page.js
│ │ ├── user/[id]/page.js
│ │ └── layout.js
│ ├── components/
│ │ ├── Header.js
│ │ └── tests/Header.test.js
│ ├── services/userService.js
│ └── middleware.js

---

