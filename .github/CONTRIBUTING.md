# Contributing to NET-Shell 🚀

First off, thank you for considering contributing to **NET-Shell**! It’s contributions like yours that make this tool a powerful resource for the security community.

To maintain the high performance and modularity of the toolkit, please follow these guidelines.

---

## 🛠️ How Can I Contribute?

### 1. Reporting Bugs
* Check the [Issues](https://github.com/SoftBridge-Labs/NET-Shell/issues) tab to see if the bug has already been reported.
* If not, open a new issue using the **Bug Report** template. 
* Include your OS, Python version, and a clear description of the steps to reproduce the error.

### 2. Suggesting Enhancements
* We welcome new modules and performance tweaks! 
* Open an issue with the tag `enhancement` to discuss your idea before writing code.

### 3. Pull Request Process
1. **Fork** the repository and create your branch from `main`.
2. **Setup** the environment using `python setup.py` to ensure all dependencies are met.
3. **Style**: Ensure your code follows PEP 8 standards. We prioritize clear, commented code over "clever" one-liners.
4. **Testing**: Verify your changes don't break existing modules (e.g., ensure the Port Scanner still resolves IPs correctly).
5. **Documentation**: If you add a new feature, update the `README.md` or provide a usage example.
6. **Submit**: Open a Pull Request with a clear description of *what* you changed and *why*.

---

## 💻 Technical Standards
* **Asynchronous First**: New networking modules should use `asyncio` and `aiohttp` to maintain the toolkit's non-blocking performance.
* **UI Consistency**: Use the existing ANSI styling constants from `modules/menu.py` for any new terminal outputs.
* **Error Handling**: Use `try...except KeyboardInterrupt` blocks for any new interactive loops.

Thank you for being part of the NET-Shell mission!