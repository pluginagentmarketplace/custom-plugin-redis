<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=Redis+Assistant;8+Agents+%7C+12+Skills;Claude+Code+Plugin" alt="Redis Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-redis/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-8-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-12-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-4-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-redis)

---

### What is this?

> **Redis Assistant** is a Claude Code plugin with **8 agents** and **12 skills** for redis development.

</div>

---

## 📑 Table of Contents

<details>
<summary>Click to expand</summary>

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation (Choose One)

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1️⃣ Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-redis

# Step 2️⃣ Install the plugin
/plugin install redis-development-assistant@redis-assistant-marketplace

# Step 3️⃣ Restart Claude Code
# Close and reopen your terminal/IDE
```

</details>

<details>
<summary><strong>Option 2: Local Installation</strong></summary>

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-redis.git
cd custom-plugin-redis

# Load locally
/plugin load .

# Restart Claude Code
```

</details>

### ✅ Verify Installation

After restart, you should see these agents:

```
redis-development-assistant:06-redis-clustering
redis-development-assistant:01-redis-fundamentals
redis-development-assistant:02-redis-data-structures
redis-development-assistant:04-redis-pubsub
redis-development-assistant:05-redis-persistence
... and 3 more
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **8 Agents** | Specialized AI agents for redis tasks |
| 🛠️ **12 Skills** | Reusable capabilities with Golden Format |
| ⌨️ **4 Commands** | Quick slash commands |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |

---

## 🤖 Agents

### 8 Specialized Agents

| # | Agent | Purpose |
|---|-------|---------|
| 1 | **06-redis-clustering** | Master Redis high availability - replication, Sentinel for a |
| 2 | **01-redis-fundamentals** | Master Redis fundamentals - installation, CLI, core concepts |
| 3 | **02-redis-data-structures** | Expert on Redis data structures - Strings, Lists, Sets, Hash |
| 4 | **04-redis-pubsub** | Master Redis Pub/Sub and Streams - real-time messaging, even |
| 5 | **05-redis-persistence** | Master Redis persistence - RDB snapshots, AOF logging, backu |
| 6 | **03-redis-operations** | Master Redis operations - key management, expiration, pipeli |
| 7 | **07-redis-security** | Master Redis security - authentication, ACL, TLS encryption, |
| 8 | **08-redis-production** | Master Redis production - monitoring, performance tuning, mo |

---

## 🛠️ Skills

### Available Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| `redis-security` | Master Redis security - authentication, ACL, TLS encryption, | `Skill("redis-development-assistant:redis-security")` |
| `redis-persistence` | Master Redis persistence - RDB snapshots, AOF logging, backu | `Skill("redis-development-assistant:redis-persistence")` |
| `redis-strings` | Master Redis Strings - SET, GET, INCR, DECR, atomic counters | `Skill("redis-development-assistant:redis-strings")` |
| `redis-replication` | Master Redis replication - master-replica setup, Sentinel fo | `Skill("redis-development-assistant:redis-replication")` |
| `redis-cluster` | Master Redis Cluster - horizontal scaling, hash slots, resha | `Skill("redis-development-assistant:redis-cluster")` |
| `redis-performance` | Master Redis performance - memory optimization, slow log ana | `Skill("redis-development-assistant:redis-performance")` |
| `redis-hashes-sorted-sets` | Master Redis Hashes and Sorted Sets - object storage, field  | `Skill("redis-development-assistant:redis-hashes-sorted-sets")` |
| `redis-lists-sets` | Master Redis Lists and Sets - queues, stacks, unique collect | `Skill("redis-development-assistant:redis-lists-sets")` |
| `redis-installation` | Complete Redis installation guide for all platforms - Linux, | `Skill("redis-development-assistant:redis-installation")` |
| `redis-modules` | Master Redis modules - RedisJSON, RediSearch, RedisTimeSerie | `Skill("redis-development-assistant:redis-modules")` |
| ... | +2 more | See skills/ directory |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `/redis-debug` | Debug Redis issues - slow queries, memory problems, connecti |
| `/redis-config` | Generate optimized Redis configuration for your use case |
| `/redis-benchmark` | Run Redis performance benchmarks and analyze results |
| `/redis-check` | Check Redis server health, connection status, and key metric |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
custom-plugin-redis/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 8 agents
├── 📁 skills/              # 12 skills (Golden Format)
├── 📁 commands/            # 4 commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

</details>

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2025-12-29 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 8 |
| **Skills** | 12 |
| **Commands** | 4 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains third-party code and dependencies.
>
> - ✅ Always review code before using in production
> - ✅ Check dependencies for known vulnerabilities
> - ✅ Follow security best practices
> - ✅ Report security issues privately via [Issues](../../issues)

---

## 📝 License

Copyright © 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## 👥 Contributors

<table>
<tr>
<td align="center">
<strong>Dr. Umit Kacar</strong><br/>
Senior AI Researcher & Engineer
</td>
<td align="center">
<strong>Muhsin Elcicek</strong><br/>
Senior Software Architect
</td>
</tr>
</table>

---

<div align="center">

**Made with ❤️ for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
