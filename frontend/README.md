# Smart File Search (Frontend)

This is the frontend application for the Smart File Search project. It provides an intuitive user interface for uploading files and performing intelligent searches within their contents.

## 📌 Features

- ⚛️ Built with React, TypeScript, Vite, and TailwindCSS.
- 📂 Simple drag-and-drop file uploads (to be implemented).
- 🔍 User-friendly search interface (to be implemented).
- 📦 Ready to be integrated with a FastAPI backend.

---

## 🌟 Why Vite and PostCSS?

### Vite
- Vite is a modern, high-performance build tool that offers fast server startup and lightning-fast HMR (Hot Module Replacement). 
- Its ability to handle TypeScript and support ES Modules out of the box makes it ideal for modern React projects.

### PostCSS
- PostCSS is a tool used for transforming CSS with plugins. In this project, it is mainly used to integrate **TailwindCSS** and process its utility-first styles.
- It's also lightweight and highly configurable, ensuring better build performance compared to traditional methods.

---

## 🔧 Environment Setup

This project uses `nvm` (Node Version Manager) and `yarn` as the package manager. Follow the steps below to configure your environment.

### 1. Installing `nvm` (Node Version Manager)
If you don't have `nvm` installed, you can install it with the following command:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```
Add the following to your .bashrc, .zshrc, or .profile file:
```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```
Then, restart your terminal or source the file:
```bash
source ~/.bashrc   # or source ~/.zshrc
```
### 2. Installing Node.js with `nvm`
Use the following commands to install and use the desired Node.js version:
```bash
nvm install 20
nvm use 20
```
### 3. Installing `yarn`
Yarn is preferred over npm for better dependency resolution and a more predictable install process.

To install Yarn globally:
```bash
npm install -g yarn
```
Verify the installation with:
```bash
yarn --version
```
---
## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<seu_usuario>/smart-file-search.git
cd smart-file-search/frontend
```

### 2. Install dependencies
```bash
yarn
```

### 3. Run the development server
```bash
yarn dev
```
---
## 📝 Build for Production

To create a production build, run:
```bash
yarn dev
```
The optimized files will be generated in the `dist` folder.
---
## 🔍 Linting

To run ESLint for static code analysis:
```bash
yarn lint
```
---
## 📁 Folder Structure

To run ESLint for static code analysis:
```bash
frontend/
├── public/              # Static assets
├── src/                 # Application source code
│   ├── assets/          # Media files (images, etc.)
│   ├── components/      # React components (to be created)
│   ├── pages/           # Application pages (to be created)
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # ReactDOM rendering point
│   └── index.css        # TailwindCSS styles
├── .eslint.config.js
├── index.html           # Main HTML file
├── package.json         # Project dependencies and scripts
├── postcss.config.js     # PostCSS configuration file
├── tailwind.config.js    # TailwindCSS configuration file
├── tsconfig.json         # TypeScript configuration file
├── vite.config.ts        # Vite configuration file
└── yarn.lock             # Yarn lock file
```
