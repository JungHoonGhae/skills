# README Templates Reference

Common README templates for different project types.

## Node.js / JavaScript

```markdown
# project-name

Brief description of what this project does.

## Installation

\`\`\`bash
npm install project-name
\`\`\`

## Usage

\`\`\`javascript
const module = require('project-name');
// or
import module from 'project-name';
\`\`\`

## API

### functionOne(param)

Description of function.

**Parameters:**
- `param` (Type) - Description

**Returns:** Type - Description

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

## Python

```markdown
# project-name

Brief description.

## Installation

\`\`\`bash
pip install project-name
\`\`\`

## Quick Start

\`\`\`python
from package import main_function

result = main_function()
\`\`\`

## Requirements

- Python >= 3.8
- dependency1
- dependency2

## Development

\`\`\`bash
pip install -e ".[dev]"
pytest
\`\`\`

## License

MIT
```

## Rust

```markdown
# project-name

Brief description.

## Installation

\`\`\`bash
cargo add project-name
\`\`\`

Or add to `Cargo.toml`:

\`\`\`toml
[dependencies]
project-name = "0.1.0"
\`\`\`

## Usage

\`\`\`rust
use crate_name::function;

fn main() {
    function();
}
\`\`\`

## License

MIT OR Apache-2.0
```

## Go

```markdown
# project-name

Brief description.

## Installation

\`\`\`bash
go get github.com/owner/project-name
\`\`\`

## Usage

\`\`\`go
import "github.com/owner/project-name"

func main() {
    // usage example
}
\`\`\`

## License

MIT
```

## Common Badge Patterns

### npm
```markdown
[![npm version](https://badge.fury.io/js/package-name.svg)](https://badge.fury.io/js/package-name)
[![npm downloads](https://img.shields.io/npm/dm/package-name.svg)](https://npmjs.com/package/package-name)
```

### PyPI
```markdown
[![PyPI version](https://badge.fury.io/py/package-name.svg)](https://badge.fury.io/py/package-name)
[![PyPI downloads](https://img.shields.io/pypi/dm/package-name.svg)](https://pypi.org/project/package-name/)
```

### CI/CD
```markdown
[![CI](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/owner/repo/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/owner/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/owner/repo)
```

### License
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
```

## Section Order Recommendations

Most common order (by frequency):

1. Title + Description
2. Badges
3. Installation
4. Usage / Quick Start
5. Features
6. Configuration / Options
7. API Reference
8. Examples
9. Contributing
10. License

## Emoji Usage Examples

```markdown
# 🚀 Project Name

## ✨ Features

- 🎯 Feature 1
- ⚡ Feature 2
- 🛠️ Feature 3

## 📦 Installation

## 🚀 Quick Start

## 📖 Documentation

## 🤝 Contributing

## 📄 License
```
